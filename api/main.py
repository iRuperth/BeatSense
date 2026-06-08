from __future__ import annotations

import csv
import uuid
from datetime import datetime
from pathlib import Path
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "models" / "modelo_coronario.pkl"
SCALER_PATH = ROOT / "models" / "scaler_coronario.pkl"
HISTORY_PATH = ROOT / "docs" / "historial_pacientes.csv"
HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)

HISTORY_COLUMNS = [
    "Fecha", "Hora", "ID_Paciente", "Edad", "Sexo",
    "FC_Maxima", "Glucosa_Ayunas", "Angina_Ejercicio",
    "Tipo_Dolor", "Pendiente_ST",
    "Probabilidad_%", "Clasificacion", "Riesgo",
]

THRESHOLD = 40.0

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


class PredictRequest(BaseModel):
    patient_id: str | None = Field(default=None, max_length=64)
    age: int = Field(ge=1, le=120)
    sex: Literal["M", "F"]
    chest_pain_type: Literal["ASY", "ATA", "NAP", "TA"]
    max_hr: int = Field(ge=40, le=240)
    fasting_bs: Literal[0, 1]
    exercise_angina: Literal["Y", "N"]
    st_slope: Literal["Up", "Flat", "Down"]
    resting_bp: int | None = Field(default=None, ge=60, le=250)
    cholesterol: int | None = Field(default=None, ge=0, le=700)
    resting_ecg: Literal["Normal", "ST", "LVH"] | None = None
    oldpeak: float | None = Field(default=None, ge=-5, le=10)


class PredictResponse(BaseModel):
    patient_id: str
    timestamp: str
    probability: float
    classification: Literal["HIGH", "LOW"]
    threshold: float
    probabilities: list[float]


class HistoryEntry(BaseModel):
    date: str
    time: str
    patient_id: str
    age: int
    sex: str
    max_hr: int
    fasting_bs: str
    exercise_angina: str
    chest_pain_type: str
    st_slope: str
    probability: float
    classification: str
    risk: str


def build_features(req: PredictRequest) -> pd.DataFrame:
    sex_num = 1 if req.sex == "M" else 0
    exercise_bin = 1 if req.exercise_angina == "Y" else 0

    cp_asy = int(req.chest_pain_type == "ASY")
    cp_ata = int(req.chest_pain_type == "ATA")
    cp_nap = int(req.chest_pain_type == "NAP")
    cp_ta = int(req.chest_pain_type == "TA")

    st_flat = int(req.st_slope == "Flat")
    st_up = int(req.st_slope == "Up")
    st_down = int(req.st_slope == "Down")

    X = pd.DataFrame(
        [[
            req.age, sex_num, req.max_hr, req.fasting_bs,
            exercise_bin, cp_asy, cp_ata, cp_nap, cp_ta,
            st_flat, st_up, st_down,
        ]],
        columns=[
            "Age", "Sex", "MaxHR", "FastingBS", "ExerciseAngina",
            "CP_ASY", "CP_ATA", "CP_NAP", "CP_TA",
            "ST_Slope_Flat", "ST_Slope_Up", "ST_Slope_Down",
        ],
    )
    X[["Age", "MaxHR"]] = scaler.transform(X[["Age", "MaxHR"]])
    return X


def append_history(req: PredictRequest, probability: float, classification: str, patient_id: str) -> None:
    now = datetime.now()
    row = {
        "Fecha": now.strftime("%Y-%m-%d"),
        "Hora": now.strftime("%H:%M:%S"),
        "ID_Paciente": patient_id,
        "Edad": req.age,
        "Sexo": req.sex,
        "FC_Maxima": req.max_hr,
        "Glucosa_Ayunas": "Sí" if req.fasting_bs == 1 else "No",
        "Angina_Ejercicio": "Sí" if req.exercise_angina == "Y" else "No",
        "Tipo_Dolor": req.chest_pain_type,
        "Pendiente_ST": req.st_slope,
        "Probabilidad_%": round(probability, 2),
        "Clasificacion": "Alto Riesgo" if classification == "HIGH" else "Bajo Riesgo",
        "Riesgo": "ALTO" if classification == "HIGH" else "BAJO",
    }
    file_exists = HISTORY_PATH.exists()
    with HISTORY_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HISTORY_COLUMNS)
        if not file_exists or HISTORY_PATH.stat().st_size == 0:
            writer.writeheader()
        writer.writerow(row)


app = FastAPI(title="BeatSense API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model_loaded": True, "threshold": THRESHOLD}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest) -> PredictResponse:
    try:
        X = build_features(req)
        probs = model.predict_proba(X)[0]
        probability = float(probs[1] * 100)
        classification = "HIGH" if probability >= THRESHOLD else "LOW"
        patient_id = req.patient_id or f"P-{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.now().isoformat()
        append_history(req, probability, classification, patient_id)
        return PredictResponse(
            patient_id=patient_id,
            timestamp=timestamp,
            probability=probability,
            classification=classification,
            threshold=THRESHOLD,
            probabilities=[float(probs[0]), float(probs[1])],
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/history", response_model=list[HistoryEntry])
def history() -> list[HistoryEntry]:
    if not HISTORY_PATH.exists():
        return []
    df = pd.read_csv(HISTORY_PATH)
    out: list[HistoryEntry] = []
    for _, row in df.iterrows():
        out.append(HistoryEntry(
            date=str(row["Fecha"]),
            time=str(row["Hora"]),
            patient_id=str(row["ID_Paciente"]),
            age=int(row["Edad"]),
            sex=str(row["Sexo"]),
            max_hr=int(row["FC_Maxima"]),
            fasting_bs=str(row["Glucosa_Ayunas"]),
            exercise_angina=str(row["Angina_Ejercicio"]),
            chest_pain_type=str(row["Tipo_Dolor"]),
            st_slope=str(row["Pendiente_ST"]),
            probability=float(row["Probabilidad_%"]),
            classification=str(row["Clasificacion"]),
            risk=str(row["Riesgo"]),
        ))
    return out


@app.get("/stats")
def stats() -> dict:
    if not HISTORY_PATH.exists():
        return {"total": 0, "high_risk": 0, "low_risk": 0, "high_risk_pct": 0, "today": 0}
    df = pd.read_csv(HISTORY_PATH)
    total = len(df)
    high = int((df["Riesgo"] == "ALTO").sum())
    low = total - high
    today = datetime.now().strftime("%Y-%m-%d")
    today_count = int((df["Fecha"] == today).sum())
    return {
        "total": total,
        "high_risk": high,
        "low_risk": low,
        "high_risk_pct": round(100 * high / total, 1) if total else 0,
        "today": today_count,
    }


@app.get("/eda")
def eda() -> dict:
    csv_path = ROOT / "data" / "heart.csv"
    if not csv_path.exists():
        return {}
    df = pd.read_csv(csv_path)
    # Age histogram (bins of 5)
    age_bins = list(range(20, 90, 5))
    df["age_bin"] = pd.cut(df["Age"], bins=age_bins, right=False)
    age_hist = (
        df.groupby("age_bin", observed=True)["HeartDisease"]
        .agg(["count", "mean"])
        .reset_index()
    )
    age_dist = [
        {"bin": f"{int(row['age_bin'].left)}-{int(row['age_bin'].right)}", "count": int(row["count"]), "risk_rate": round(float(row["mean"]) * 100, 1)}
        for _, row in age_hist.iterrows()
    ]
    sex_dist = [
        {"sex": s, "count": int((df["Sex"] == s).sum()), "risk_rate": round(float(df[df["Sex"] == s]["HeartDisease"].mean()) * 100, 1)}
        for s in ["M", "F"]
    ]
    cp_dist = [
        {"type": c, "count": int((df["ChestPainType"] == c).sum()), "risk_rate": round(float(df[df["ChestPainType"] == c]["HeartDisease"].mean()) * 100, 1)}
        for c in ["ASY", "ATA", "NAP", "TA"]
    ]
    scatter = (
        df.sample(min(300, len(df)), random_state=42)[["Age", "MaxHR", "HeartDisease"]]
        .to_dict(orient="records")
    )
    return {
        "age_dist": age_dist,
        "sex_dist": sex_dist,
        "chest_pain_dist": cp_dist,
        "scatter": scatter,
        "total": int(len(df)),
    }


@app.get("/model-info")
def model_info() -> dict:
    return {
        "name": "Logistic Regression",
        "threshold": THRESHOLD,
        "metrics": {
            "accuracy": 0.88,
            "recall": 0.94,
            "roc_auc": 0.926,
            "cv_mean": 0.8474,
            "cv_std": 0.0291,
        },
        "alternatives": [
            {"name": "Random Forest", "accuracy": 0.87, "recall": 0.88, "roc_auc": 0.91},
            {"name": "K-NN", "accuracy": 0.82, "recall": 0.83, "roc_auc": 0.87},
            {"name": "XGBoost", "accuracy": 0.86, "recall": 0.87, "roc_auc": 0.90},
        ],
        "features": [
            "Age", "Sex", "MaxHR", "FastingBS", "ExerciseAngina",
            "ChestPainType (ASY/ATA/NAP/TA)", "ST_Slope (Up/Flat/Down)",
        ],
    }

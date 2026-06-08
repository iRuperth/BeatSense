---
title: BeatSense
emoji: 🩺
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
license: mit
short_description: Cardiovascular risk workstation (FastAPI + Next.js)
---

<p align="center">
  <img src="src/img/logo.png" alt="BeatSense" width="260" />
</p>

<h1 align="center">BeatSense — Cardiovascular Risk Intelligence</h1>

<p align="center">
  <a href="https://huggingface.co/spaces/devrup404/BeatSense">
    <img src="src/img/qr_hf.png" alt="QR — Hugging Face Space" width="160"/>
  </a>
</p>

<p align="center">
  <sub><b>Scan to open the Hugging Face Space</b></sub>
</p>

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/English-0d1a1f?style=flat&logoColor=7fd1c6&labelColor=0a1014" alt="English" /></a>
  ·
  <a href="README.es.md"><img src="https://img.shields.io/badge/Espa%C3%B1ol-0d1a1f?style=flat&logoColor=7fd1c6&labelColor=0a1014" alt="Español" /></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-0a1014?logo=python&logoColor=7fd1c6&labelColor=0d1a1f" />
  <img src="https://img.shields.io/badge/FastAPI-0.115-0a1014?logo=fastapi&logoColor=7fd1c6&labelColor=0d1a1f" />
  <img src="https://img.shields.io/badge/scikit--learn-1.8-0a1014?logo=scikitlearn&logoColor=7fd1c6&labelColor=0d1a1f" />
  <img src="https://img.shields.io/badge/XGBoost-3.x-0a1014?logoColor=7fd1c6&labelColor=0d1a1f" />
  <img src="https://img.shields.io/badge/Optuna-4.x-0a1014?logoColor=7fd1c6&labelColor=0d1a1f" />
  <img src="https://img.shields.io/badge/uv-package%20mgr-0a1014?logoColor=7fd1c6&labelColor=0d1a1f" />
  <img src="https://img.shields.io/badge/Next.js-16-0a1014?logo=nextdotjs&logoColor=7fd1c6&labelColor=0d1a1f" />
  <img src="https://img.shields.io/badge/React-19-0a1014?logo=react&logoColor=7fd1c6&labelColor=0d1a1f" />
  <img src="https://img.shields.io/badge/TypeScript-5-0a1014?logo=typescript&logoColor=7fd1c6&labelColor=0d1a1f" />
  <img src="https://img.shields.io/badge/Tailwind-v4-0a1014?logo=tailwindcss&logoColor=7fd1c6&labelColor=0d1a1f" />
  <img src="https://img.shields.io/badge/TanStack%20Query-5-0a1014?logoColor=7fd1c6&labelColor=0d1a1f" />
  <img src="https://img.shields.io/badge/Recharts-2-0a1014?logoColor=7fd1c6&labelColor=0d1a1f" />
  <img src="https://img.shields.io/badge/pnpm-10-0a1014?logo=pnpm&logoColor=7fd1c6&labelColor=0d1a1f" />
  <img src="https://img.shields.io/badge/Streamlit-1.x-0a1014?logo=streamlit&logoColor=7fd1c6&labelColor=0d1a1f" />
  <img src="https://img.shields.io/badge/Docker-compose-0a1014?logo=docker&logoColor=7fd1c6&labelColor=0d1a1f" />
</p>

<p align="center">
  <a href="https://medium.com/@devrup404/most-clinical-machine-learning-prototypes-share-the-same-fate-2c357e91e112"><img src="https://img.shields.io/badge/Medium-Read%20the%20article-0a1014?logo=medium&logoColor=7fd1c6&labelColor=0d1a1f" alt="Read on Medium" /></a>
</p>

> **BeatSense** is a cardiovascular risk assessment platform born from a question: what would a coronary risk tool actually feel like if it were built for the nurses station of a real hospital, instead of for a notebook demo?
>
> Around a trained scikit-learn model (918 patients, twelve clinical features), it ships three coordinated surfaces: a FastAPI service that exposes the model and persists every assessment, a Next.js 16 clinical workstation with sidebar navigation, dark mode, English and Spanish, and a result rendered as a printable thermal-style ticket ready to clip to the patient record, plus a legacy Streamlit dashboard kept alive for quick demos. The model itself is a Logistic Regression with a custom 0.4 decision threshold, picked because in cardiology a false negative is far more dangerous than a false positive, an interpretable choice that recovers 94% of true positives.
>
> The repo is end-to-end: notebooks for EDA and training, a typed REST API, a production-grade clinical UI, internationalization with zero hardcoded strings, and theme tokens out of the box.

---

## Table of Contents

| | |
|---|---|
| Overview | Live Demo |
| Features | Architecture |
| Project Structure | Tech Stack |
| Dataset | Model Selection |
| Getting Started | Make Targets |
| API Reference | Frontend Highlights |
| Internationalization | Theming |
| Testing | Docker |

---

## Overview

**BeatSense** predicts the probability of coronary heart disease from clinical patient data. It ships three independent surfaces sharing the same trained model:

- A **FastAPI** REST backend that wraps the production model (models/modelo_coronario.pkl).
- A **Next.js 16** clinical workstation UI — sidebar, ticket-style report, dark mode, EN/ES — for nurses and clinicians.
- A legacy **Streamlit** dashboard (still operational) for quick demos.

The trained model is a **Logistic Regression** with a custom decision threshold of 0.4, chosen because in cardiology the cost of a false negative (missing a sick patient) far exceeds that of a false positive.

---

## Live Demo

<p>
  <a href="https://huggingface.co/spaces/devrup404/BeatSense"><img src="https://img.shields.io/badge/Hugging%20Face-Open%20Space-0a1014?style=flat&logo=huggingface&logoColor=7fd1c6&labelColor=0d1a1f" alt="Hugging Face Space" /></a>
</p>

---

## Features

| Surface | Highlights |
|---|---|
| 🤖 **ML pipeline** | EDA + survival analysis (Kaplan–Meier, Cox), preprocessing, 4 models compared, Optuna tuning, full notebooks. |
| 🚀 **REST API** | FastAPI service with /predict, /history, /stats, /eda, /model-info, persistent CSV history, CORS enabled. |
| 🩺 **Clinical UI** | Next.js 16 + Tailwind v4 + shadcn-style components. Sidebar navigation, nurse-station header, KPI dashboard, filtered patient table, EDA charts, model insights. |
| 🖨️ **Printable ticket** | Risk result rendered as a thermal-printer ticket: monospace font, dashed dividers, barcode, window.print(). |
| 🌍 **i18n** | English (default) + Spanish, zero hardcoded strings, JSON dictionaries, cookie + Accept-Language detection. |
| 🌓 **Dark mode** | First-class next-themes integration, dark by default, no flash on first paint. |
| 📦 **Containerized** | Docker / docker-compose for the Streamlit surface. |
| 🛠️ **Dual toolchain** | uv for Python, pnpm for the Next.js workspace. One make dev boots both servers. |

---

## Architecture

```
┌─────────────────────────┐      HTTPS/REST       ┌────────────────────────┐
│ Next.js 16 frontend     │  ────────────────▶    │ FastAPI service         │
│ • App Router            │                       │ • /predict              │
│ • Server + Client       │                       │ • /history /stats       │
│   Components            │                       │ • /eda /model-info      │
│ • TanStack Query        │  ◀────────────────    │ • Loads .pkl + scaler   │
└─────────────┬───────────┘      JSON              └───────────┬────────────┘
              │                                                │
              │ static assets                                   │ joblib.load
              ▼                                                ▼
        ┌──────────┐                                ┌─────────────────────┐
        │ /public  │                                │ models/             │
        │ logu1.png│                                │  • modelo_coronario │
        └──────────┘                                │  • scaler_coronario │
                                                    └─────────────────────┘
                                                              ▲
                                                              │ persists
                                                              │
                                                    ┌─────────┴───────────┐
                                                    │ docs/                │
                                                    │ historial_pacientes  │
                                                    └──────────────────────┘
```

---

## Project Structure

```
BeatSense/
├── api/                              # FastAPI backend
│   └── main.py                       # /predict, /history, /stats, /eda, /model-info
│
├── app.py                            # Legacy Streamlit app (still works)
│
├── frontend/                         # Next.js 16 clinical workstation
│   ├── public/
│   │   └── logu1.png                 # Logo (auto-cropped for tight framing)
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx            # Root layout — ThemeProvider lives here
│   │   │   ├── globals.css           # Tailwind v4 + design tokens + print CSS
│   │   │   └── [lang]/               # Locale-scoped routes
│   │   │       ├── layout.tsx        # CRM shell (Sidebar + Header) + Providers
│   │   │       ├── page.tsx          # Dashboard (KPIs + recent + pie chart)
│   │   │       ├── new-evaluation/   # Clinical form → ticket result
│   │   │       ├── patients/         # Filterable history table + CSV export
│   │   │       ├── eda/              # Dataset analytics (Recharts)
│   │   │       ├── model/            # Model metrics + comparison
│   │   │       └── settings/         # Language + theme switcher
│   │   ├── components/
│   │   │   ├── ui/                   # Button, Card, Input, Label, Select, Badge
│   │   │   ├── layout/               # Sidebar, Header, PageHeader, toggles
│   │   │   ├── forms/                # EvaluationForm (RHF + Zod)
│   │   │   ├── ticket/               # Printable result ticket
│   │   │   ├── charts/               # EDA charts
│   │   │   ├── dashboard/            # Dashboard client widgets
│   │   │   ├── patients/             # Patient table
│   │   │   ├── model/                # Model insights
│   │   │   ├── settings/             # Settings panel
│   │   │   └── providers.tsx         # ThemeRoot + I18nProvider + QueryClient
│   │   ├── i18n/
│   │   │   ├── config.ts             # Locale list + defaultLocale
│   │   │   ├── context.tsx           # Client-side useT() hook
│   │   │   ├── dictionaries.ts       # Server-only loader
│   │   │   └── dictionaries/
│   │   │       ├── en.json
│   │   │       └── es.json
│   │   ├── lib/
│   │   │   ├── api.ts                # Typed REST client (TanStack-friendly)
│   │   │   └── utils.ts              # cn() helper
│   │   └── proxy.ts                  # Next 16 middleware: locale routing
│   ├── package.json
│   └── tsconfig.json
│
├── data/                             # Heart Disease dataset (918 records)
│   ├── heart.csv                     # Raw
│   ├── heart_procesado_g.csv         # Processed by Gema
│   ├── heart_procesado_i.csv         # Processed by Isrodam
│   └── heart_processed_R.csv         # Processed by Roberto
│
├── models/                           # Persisted scikit-learn artifacts
│   ├── modelo_coronario.pkl
│   ├── scaler_coronario.pkl
│   └── model_R.pkl
│
├── notebook/                         # EDA + training notebooks
│   ├── eda_heart_disease_p.ipynb     # EDA + survival analysis (Paloma)
│   ├── eda_heart_failure_g.ipynb     # EDA (Gema)
│   ├── eda_heart_failure_i.ipynb     # EDA (Isrodam)
│   ├── eda_heart_failure_R.ipynb     # EDA (Roberto)
│   ├── entrenamiento_modelo_final.ipynb
│   ├── entrenamiento_modelo_g.ipynb
│   └── entrenamiento_modelo_i.ipynb
│
├── report/                           # Evaluation reports (PDF)
├── docs/historial_pacientes.csv      # Patient history (written by /predict)
├── src/img/qr_app.png                # QR code to live demo
├── assets/                           # Static assets (lottie, etc.)
├── .streamlit/                       # Streamlit theming
├── Makefile                          # uv + pnpm orchestration
├── dockerfile
├── docker-compose.yml
├── pyproject.toml                    # uv-managed Python deps
└── uv.lock
```

---

## Tech Stack

### Backend / ML

- **Python 3.11** managed with **uv**
- **FastAPI** + **Uvicorn** — REST API
- **scikit-learn** — Logistic Regression, RF, KNN; StandardScaler
- **XGBoost** — alternative model evaluated
- **Optuna** — hyperparameter search
- **pandas / numpy** — data wrangling
- **joblib** — model persistence
- **Streamlit** — legacy interactive dashboard
- **pytest** — tests

### Frontend

- **Next.js 16** (App Router, Turbopack, Server Components)
- **React 19** + **TypeScript 5**
- **Tailwind CSS v4** with custom design tokens
- **shadcn-style UI** built on **Radix UI** primitives
- **TanStack Query 5** — server-state caching
- **React Hook Form 7** + **Zod 4** — typed forms with runtime validation
- **Recharts** — analytics charts
- **next-themes** — dark/light theme
- **next-intl-style i18n** using Next.js native dictionaries
- **lucide-react** — icon set
- **pnpm 10** — workspace package manager

### DevOps

- **Make** — single command interface
- **Docker / docker-compose** — containerised Streamlit deployment
- **GitHub Actions** — CI/CD
- **Render** — production hosting (Streamlit demo)

---

## Dataset

918 records, 12 features:

| Variable | Description | Type |
|---|---|---|
| Age | Patient age | Numeric |
| Sex | Sex (M/F) | Categorical |
| ChestPainType | Type (ATA, NAP, ASY, TA) | Categorical |
| RestingBP | Resting blood pressure (mm Hg) | Numeric |
| Cholesterol | Serum cholesterol (mg/dl) | Numeric |
| FastingBS | Fasting blood sugar > 120 mg/dl (0/1) | Binary |
| RestingECG | Resting ECG result | Categorical |
| MaxHR | Max heart rate achieved | Numeric |
| ExerciseAngina | Exercise-induced angina (Y/N) | Binary |
| Oldpeak | ST depression | Numeric |
| ST_Slope | ST segment slope | Categorical |
| HeartDisease | **Target** — heart disease (0/1) | Binary |

The production model uses **12 engineered features** (Age, Sex, MaxHR, FastingBS, ExerciseAngina, one-hot of ChestPainType, one-hot of ST_Slope). Only Age and MaxHR are scaled.

---

## Model Selection

| Model | Accuracy | Recall (class 1) | ROC-AUC | Notes |
|---|---|---|---|---|
| **Logistic Regression** *(threshold 0.4)* | **88 %** | **0.94** | **0.926** | ✅ Selected |
| Random Forest | ~87 % | ~0.88 | ~0.91 | Higher raw accuracy, lower recall |
| K-NN | ~82 % | ~0.83 | ~0.87 | Scale-sensitive |
| XGBoost | ~86 % | ~0.87 | ~0.90 | Strong, less interpretable |

### Why Logistic Regression?

1. **Highest recall (0.94)** — at threshold 0.4 it catches 94% of truly sick patients. A false negative in cardiology is far worse than a false positive.
2. **No overfitting** — train/test gap of only 0.007. 5-fold CV: 84.74% ± 2.91%.
3. **Clinical transparency** — linear coefficients let clinicians see exactly which features drive each prediction.

> Full analysis:
>
> <a href="notebook/entrenamiento_modelo_final.ipynb"><img src="https://img.shields.io/badge/notebook-entrenamiento__modelo__final.ipynb-0a1014?style=flat&logo=jupyter&logoColor=7fd1c6&labelColor=0d1a1f" alt="Notebook" /></a>
> <a href="report/entrenamiento_modelo_final.pdf"><img src="https://img.shields.io/badge/report-entrenamiento__modelo__final.pdf-0a1014?style=flat&logo=adobeacrobatreader&logoColor=7fd1c6&labelColor=0d1a1f" alt="Report" /></a>

---

## Getting Started

### Prerequisites

- Python >=3.11, <3.13
- <a href="https://docs.astral.sh/uv/"><img src="https://img.shields.io/badge/uv-Python%20toolchain-0a1014?style=flat&logoColor=7fd1c6&labelColor=0d1a1f" alt="uv" /></a>
- <a href="https://pnpm.io/"><img src="https://img.shields.io/badge/pnpm-%E2%89%A510%20Node.js%20toolchain-0a1014?style=flat&logo=pnpm&logoColor=7fd1c6&labelColor=0d1a1f" alt="pnpm" /></a>
- Node.js >=20

### Install

```bash
# Python deps
make install

# Frontend deps
make frontend-install
```

### Run everything (recommended)

```bash
make dev
```

This spawns:

<p>
  <a href="http://localhost:8000/docs"><img src="https://img.shields.io/badge/FastAPI-localhost:8000/docs-0a1014?style=flat&logo=fastapi&logoColor=7fd1c6&labelColor=0d1a1f" alt="FastAPI" /></a>
  <a href="http://localhost:3000"><img src="https://img.shields.io/badge/Next.js-localhost:3000-0a1014?style=flat&logo=nextdotjs&logoColor=7fd1c6&labelColor=0d1a1f" alt="Next.js" /></a>
</p>

### Run individually

```bash
make api          # FastAPI only
make frontend     # Next.js only
make streamlit    # Legacy Streamlit dashboard
```

---

## Make Targets

| Target | Purpose |
|---|---|
| make install | uv sync — install Python deps |
| make frontend-install | pnpm install — install frontend deps |
| make dev | Run **both** FastAPI + Next.js in parallel |
| make api | Run FastAPI only (uvicorn :8000) |
| make frontend | Run Next.js only (pnpm dev :3000) |
| make frontend-build | Production build of Next.js |
| make streamlit | Run legacy Streamlit app |
| make docker-up / docker-down / docker-build / docker-logs | Docker Compose lifecycle |
| make jupyter | Launch JupyterLab |
| make test | Run pytest |
| make clean | Remove caches and .next/ |

---

## API Reference

<p>
  <b>Base URL</b>&nbsp;
  <a href="http://localhost:8000"><img src="https://img.shields.io/badge/localhost:8000-0a1014?style=flat&logoColor=7fd1c6&labelColor=0d1a1f" alt="localhost:8000" /></a>
</p>

| Method | Path | Description |
|---|---|---|
| GET | /health | Liveness + model load status |
| POST | /predict | Run cardiovascular risk prediction |
| GET | /history | Return all saved patient assessments |
| GET | /stats | Aggregate KPIs (totals, high-risk %, today) |
| GET | /eda | Aggregated EDA payload for charts |
| GET | /model-info | Metrics of the selected model + alternatives |

### POST /predict payload

```json
{
  "patient_id": "P-001",
  "age": 55,
  "sex": "M",
  "chest_pain_type": "ASY",
  "max_hr": 130,
  "fasting_bs": 0,
  "exercise_angina": "Y",
  "st_slope": "Flat",
  "resting_bp": 140,
  "cholesterol": 240,
  "resting_ecg": "Normal",
  "oldpeak": 1.2
}
```

Response:

```json
{
  "patient_id": "P-001",
  "timestamp": "2026-06-08T10:32:41",
  "probability": 94.28,
  "classification": "HIGH",
  "threshold": 40.0,
  "probabilities": [0.057, 0.943]
}
```

---

## Frontend Highlights

- **/[lang]** Clinical dashboard — KPI cards, recent assessments, risk distribution pie.
- **/[lang]/new-evaluation** Clinical form in three sections (Identification, Vitals, Symptoms/ECG) with RHF + Zod validation. On submit, the answer renders as a printable **ticket** (window.print() switches the print stylesheet so only the ticket prints, like a thermal receipt).
- **/[lang]/patients** Searchable, filterable history table (high / low / all). CSV export client-side.
- **/[lang]/eda** Charts: age histogram, sex distribution, chest pain distribution, scatter Max HR vs Age coloured by outcome.
- **/[lang]/model** Selected model card, comparison bar chart, rationale paragraph.
- **/[lang]/settings** Language + theme switcher.

The layout is a **CRM/EHR shell** with a sticky dark sidebar (logo + navigation + institution badge), a header bar with patient search, shift indicator, language switch, theme toggle and a faux nurse-station avatar.

---

## Internationalization

- Built on **Next.js 16 native dictionaries** (app/[lang]/...).
- All UI strings live in frontend/src/i18n/dictionaries/{en,es}.json.
- Locale is resolved in this order by frontend/src/proxy.ts:
  1. locale cookie (set by the language switcher),
  2. Accept-Language header,
  3. fallback to **English**.
- useT() exposes the dictionary to client components.

Add a new locale by creating {xx}.json, adding xx to locales in src/i18n/config.ts, and registering it in src/i18n/dictionaries.ts.

---

## Theming

- Dark mode is the **default**.
- Theme tokens are defined as CSS variables in globals.css (:root for light, .dark for dark) and bridged to Tailwind v4 via @theme inline.
- ThemeProvider is mounted at the **root layout** to avoid hydration issues with next-themes.

---

## Testing

```bash
make test                  # pytest
cd frontend && pnpm build  # type-check + production build
```

---

## Docker

```bash
make docker-up      # Build and run Streamlit container
make docker-logs    # Stream logs
make docker-down    # Stop
```

> Containerising the Next.js + FastAPI duo is on the roadmap.

---


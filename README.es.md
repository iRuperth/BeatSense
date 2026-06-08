<p align="center">
  <img src="src/img/logo.png" alt="BeatSense" width="260" />
</p>

<h1 align="center">BeatSense · Inteligencia de Riesgo Cardiovascular</h1>

<p align="center">
  <a href="https://huggingface.co/spaces/devrup404/BeatSense">
    <img src="src/img/qr_hf.png" alt="QR — Hugging Face Space" width="160"/>
  </a>
</p>

<p align="center">
  <sub><b>Escanea para abrir el Space de Hugging Face</b></sub>
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
  <a href="https://medium.com/@devrup404/most-clinical-machine-learning-prototypes-share-the-same-fate-2c357e91e112"><img src="https://img.shields.io/badge/Medium-Leer%20el%20art%C3%ADculo-0a1014?logo=medium&logoColor=7fd1c6&labelColor=0d1a1f" alt="Leer en Medium" /></a>
</p>

> **BeatSense** es una plataforma de evaluación del riesgo cardiovascular que nace de una pregunta: ¿qué pinta tendría una herramienta de riesgo coronario si se construyera de verdad para el puesto de enfermería de un hospital, en lugar de para una demo de notebook?
>
> Sobre un modelo entrenado con scikit-learn (918 pacientes, doce variables clínicas), agrupa tres superficies coordinadas: un servicio FastAPI que expone el modelo y persiste cada evaluación, una estación clínica en Next.js 16 con navegación lateral, modo oscuro, inglés y español, y un resultado renderizado como ticket imprimible estilo impresora térmica listo para grapar a la historia del paciente, además de un dashboard heredado en Streamlit que sigue vivo para demos rápidas. El modelo es una Regresión Logística con umbral de decisión personalizado de 0.4, elegida porque en cardiología un falso negativo es mucho más peligroso que un falso positivo, una opción interpretable que recupera el 94 % de los verdaderos positivos.
>
> El repositorio es completo: notebooks de EDA y entrenamiento, una API REST tipada, una UI clínica en serio, internacionalización sin un solo texto cableado, tokens de tema y un único make dev que lo arranca todo.

---

## Índice

| | |
|---|---|
| Visión general | Demo en vivo |
| Funcionalidades | Arquitectura |
| Estructura del proyecto | Stack tecnológico |
| Dataset | Selección del modelo |
| Primeros pasos | Targets de Make |
| Referencia de la API | Características del frontend |
| Internacionalización | Temas |
| Pruebas | Docker |

---

## Visión general

**BeatSense** predice la probabilidad de enfermedad coronaria a partir de datos clínicos del paciente. Entrega tres superficies independientes que comparten el mismo modelo entrenado:

- Un backend **REST con FastAPI** que envuelve el modelo en producción (models/modelo_coronario.pkl).
- Una UI de **estación clínica con Next.js 16** — sidebar, informe con formato de ticket, modo oscuro y EN/ES — pensada para enfermería y personal clínico.
- Un dashboard heredado en **Streamlit** (sigue operativo) para demos rápidas.

El modelo en producción es una **Regresión Logística** con umbral de decisión personalizado de 0.4, elegido porque en cardiología el coste de un falso negativo (no detectar a un paciente enfermo) es muy superior al de un falso positivo.

---

## Demo en vivo

<p>
  <a href="https://huggingface.co/spaces/devrup404/BeatSense"><img src="https://img.shields.io/badge/Hugging%20Face-Abrir%20Space-0a1014?style=flat&logo=huggingface&logoColor=7fd1c6&labelColor=0d1a1f" alt="Hugging Face Space" /></a>
</p>

---

## Funcionalidades

| Superficie | Destacados |
|---|---|
| 🤖 **Pipeline ML** | EDA + análisis de supervivencia (Kaplan–Meier, Cox), preprocesado, comparación de 4 modelos, ajuste con Optuna y notebooks completos. |
| 🚀 **API REST** | FastAPI con /predict, /history, /stats, /eda, /model-info, historial persistente en CSV, CORS habilitado. |
| 🩺 **UI clínica** | Next.js 16 + Tailwind v4 + componentes estilo shadcn. Navegación lateral, cabecera tipo puesto de enfermería, panel de KPIs, tabla filtrable de pacientes, gráficos EDA e información del modelo. |
| 🖨️ **Ticket imprimible** | El resultado se renderiza como ticket de impresora térmica: tipografía monoespaciada, separadores punteados, código de barras y window.print(). |
| 🌍 **i18n** | Inglés (por defecto) + español, sin ningún texto cableado, diccionarios JSON, detección por cookie + Accept-Language. |
| 🌓 **Modo oscuro** | Integración con next-themes, oscuro por defecto, sin flash en el primer render. |
| 📦 **Containerizado** | Docker / docker-compose para la superficie Streamlit. |
| 🛠️ **Doble toolchain** | uv para Python, pnpm para el workspace de Next.js. Un solo make dev arranca ambos servidores. |

---

## Arquitectura

```
┌─────────────────────────┐      HTTPS/REST       ┌────────────────────────┐
│ Frontend Next.js 16     │  ────────────────▶    │ Servicio FastAPI        │
│ • App Router            │                       │ • /predict              │
│ • Server + Client       │                       │ • /history /stats       │
│   Components            │                       │ • /eda /model-info      │
│ • TanStack Query        │  ◀────────────────    │ • Carga .pkl + scaler   │
└─────────────┬───────────┘      JSON              └───────────┬────────────┘
              │                                                │
              │ assets estáticos                                │ joblib.load
              ▼                                                ▼
        ┌──────────┐                                ┌─────────────────────┐
        │ /public  │                                │ models/             │
        │ logu1.png│                                │  • modelo_coronario │
        └──────────┘                                │  • scaler_coronario │
                                                    └─────────────────────┘
                                                              ▲
                                                              │ persiste
                                                              │
                                                    ┌─────────┴───────────┐
                                                    │ docs/                │
                                                    │ historial_pacientes  │
                                                    └──────────────────────┘
```

---

## Estructura del proyecto

```
BeatSense/
├── api/                              # Backend FastAPI
│   └── main.py                       # /predict, /history, /stats, /eda, /model-info
│
├── app.py                            # Streamlit heredado (sigue funcionando)
│
├── frontend/                         # Estación clínica Next.js 16
│   ├── public/
│   │   └── logu1.png                 # Logo (recortado para encuadre ajustado)
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx            # Layout raíz — aquí vive el ThemeProvider
│   │   │   ├── globals.css           # Tailwind v4 + tokens de diseño + CSS de impresión
│   │   │   └── [lang]/               # Rutas por locale
│   │   │       ├── layout.tsx        # Shell del CRM (Sidebar + Header) + Providers
│   │   │       ├── page.tsx          # Panel (KPIs + recientes + pie chart)
│   │   │       ├── new-evaluation/   # Formulario clínico → ticket de resultado
│   │   │       ├── patients/         # Historial filtrable + export CSV
│   │   │       ├── eda/              # Analítica del dataset (Recharts)
│   │   │       ├── model/            # Métricas + comparación de modelos
│   │   │       └── settings/         # Selector de idioma y tema
│   │   ├── components/
│   │   │   ├── ui/                   # Button, Card, Input, Label, Select, Badge
│   │   │   ├── layout/               # Sidebar, Header, PageHeader, toggles
│   │   │   ├── forms/                # EvaluationForm (RHF + Zod)
│   │   │   ├── ticket/               # Ticket imprimible del resultado
│   │   │   ├── charts/               # Gráficos EDA
│   │   │   ├── dashboard/            # Widgets cliente del dashboard
│   │   │   ├── patients/             # Tabla de pacientes
│   │   │   ├── model/                # Insights del modelo
│   │   │   ├── settings/             # Panel de ajustes
│   │   │   └── providers.tsx         # ThemeRoot + I18nProvider + QueryClient
│   │   ├── i18n/
│   │   │   ├── config.ts             # Lista de locales + defaultLocale
│   │   │   ├── context.tsx           # Hook cliente useT()
│   │   │   ├── dictionaries.ts       # Loader server-only
│   │   │   └── dictionaries/
│   │   │       ├── en.json
│   │   │       └── es.json
│   │   ├── lib/
│   │   │   ├── api.ts                # Cliente REST tipado (TanStack-friendly)
│   │   │   └── utils.ts              # Helper cn()
│   │   └── proxy.ts                  # Middleware de Next 16: routing por locale
│   ├── package.json
│   └── tsconfig.json
│
├── data/                             # Dataset Heart Disease (918 registros)
│   ├── heart.csv                     # Crudo
│   ├── heart_procesado_g.csv         # Procesado por Gema
│   ├── heart_procesado_i.csv         # Procesado por Isrodam
│   └── heart_processed_R.csv         # Procesado por Roberto
│
├── models/                           # Artefactos persistidos de scikit-learn
│   ├── modelo_coronario.pkl
│   ├── scaler_coronario.pkl
│   └── model_R.pkl
│
├── notebook/                         # Notebooks de EDA + entrenamiento
│   ├── eda_heart_disease_p.ipynb     # EDA + supervivencia (Paloma)
│   ├── eda_heart_failure_g.ipynb     # EDA (Gema)
│   ├── eda_heart_failure_i.ipynb     # EDA (Isrodam)
│   ├── eda_heart_failure_R.ipynb     # EDA (Roberto)
│   ├── entrenamiento_modelo_final.ipynb
│   ├── entrenamiento_modelo_g.ipynb
│   └── entrenamiento_modelo_i.ipynb
│
├── report/                           # Informes de evaluación (PDF)
├── docs/historial_pacientes.csv      # Historial de pacientes (escrito por /predict)
├── src/img/qr_app.png                # Código QR a la demo
├── assets/                           # Assets estáticos (lottie, etc.)
├── .streamlit/                       # Theming de Streamlit
├── Makefile                          # Orquestación uv + pnpm
├── dockerfile
├── docker-compose.yml
├── pyproject.toml                    # Dependencias Python gestionadas por uv
└── uv.lock
```

---

## Stack tecnológico

### Backend / ML

- **Python 3.11** gestionado con **uv**
- **FastAPI** + **Uvicorn** — API REST
- **scikit-learn** — Regresión Logística, RF, KNN; StandardScaler
- **XGBoost** — modelo alternativo evaluado
- **Optuna** — búsqueda de hiperparámetros
- **pandas / numpy** — manipulación de datos
- **joblib** — persistencia del modelo
- **Streamlit** — dashboard interactivo heredado
- **pytest** — tests

### Frontend

- **Next.js 16** (App Router, Turbopack, Server Components)
- **React 19** + **TypeScript 5**
- **Tailwind CSS v4** con tokens de diseño personalizados
- **UI estilo shadcn** sobre primitivas de **Radix UI**
- **TanStack Query 5** — caching de estado de servidor
- **React Hook Form 7** + **Zod 4** — formularios tipados con validación en runtime
- **Recharts** — gráficos analíticos
- **next-themes** — tema oscuro/claro
- **i18n nativo de Next.js** mediante dictionaries
- **lucide-react** — iconografía
- **pnpm 10** — gestor de paquetes del workspace

### DevOps

- **Make** — interfaz de un solo comando
- **Docker / docker-compose** — despliegue containerizado de Streamlit
- **GitHub Actions** — CI/CD
- **Render** — hosting de producción (demo Streamlit)

---

## Dataset

918 registros, 12 variables:

| Variable | Descripción | Tipo |
|---|---|---|
| Age | Edad del paciente | Numérica |
| Sex | Sexo (M/F) | Categórica |
| ChestPainType | Tipo (ATA, NAP, ASY, TA) | Categórica |
| RestingBP | Presión arterial en reposo (mm Hg) | Numérica |
| Cholesterol | Colesterol sérico (mg/dl) | Numérica |
| FastingBS | Glucosa en ayunas > 120 mg/dl (0/1) | Binaria |
| RestingECG | ECG en reposo | Categórica |
| MaxHR | Frecuencia cardíaca máxima alcanzada | Numérica |
| ExerciseAngina | Angina inducida por ejercicio (Y/N) | Binaria |
| Oldpeak | Depresión del segmento ST | Numérica |
| ST_Slope | Pendiente del segmento ST | Categórica |
| HeartDisease | **Variable objetivo** — enfermedad cardíaca (0/1) | Binaria |

El modelo en producción utiliza **12 características derivadas** (Age, Sex, MaxHR, FastingBS, ExerciseAngina, one-hot de ChestPainType, one-hot de ST_Slope). Solo se escalan Age y MaxHR.

---

## Selección del modelo

| Modelo | Exactitud | Recall (clase 1) | ROC-AUC | Notas |
|---|---|---|---|---|
| **Regresión Logística** *(umbral 0.4)* | **88 %** | **0.94** | **0.926** | ✅ Seleccionado |
| Random Forest | ~87 % | ~0.88 | ~0.91 | Mayor exactitud bruta, menor recall |
| K-NN | ~82 % | ~0.83 | ~0.87 | Sensible a la escala |
| XGBoost | ~86 % | ~0.87 | ~0.90 | Fuerte, menos interpretable |

### ¿Por qué Regresión Logística?

1. **Recall máximo (0.94)** — con umbral 0.4 detecta al 94% de los pacientes realmente enfermos. En cardiología un falso negativo es mucho peor que un falso positivo.
2. **Sin sobreajuste** — diferencia train/test de solo 0.007. CV de 5 pliegues: 84.74% ± 2.91%.
3. **Transparencia clínica** — sus coeficientes lineales permiten al especialista entender exactamente qué variables influyen en cada predicción.

> Análisis completo:
>
> <a href="notebook/entrenamiento_modelo_final.ipynb"><img src="https://img.shields.io/badge/notebook-entrenamiento__modelo__final.ipynb-0a1014?style=flat&logo=jupyter&logoColor=7fd1c6&labelColor=0d1a1f" alt="Notebook" /></a>
> <a href="report/entrenamiento_modelo_final.pdf"><img src="https://img.shields.io/badge/report-entrenamiento__modelo__final.pdf-0a1014?style=flat&logo=adobeacrobatreader&logoColor=7fd1c6&labelColor=0d1a1f" alt="Report" /></a>

---

## Primeros pasos

### Prerrequisitos

- Python >=3.11, <3.13
- <a href="https://docs.astral.sh/uv/"><img src="https://img.shields.io/badge/uv-toolchain%20Python-0a1014?style=flat&logoColor=7fd1c6&labelColor=0d1a1f" alt="uv" /></a>
- <a href="https://pnpm.io/"><img src="https://img.shields.io/badge/pnpm-%E2%89%A510%20toolchain%20Node.js-0a1014?style=flat&logo=pnpm&logoColor=7fd1c6&labelColor=0d1a1f" alt="pnpm" /></a>
- Node.js >=20

### Instalación

```bash
# Dependencias Python
make install

# Dependencias frontend
make frontend-install
```

### Ejecutar todo (recomendado)

```bash
make dev
```

Esto lanza:

<p>
  <a href="http://localhost:8000/docs"><img src="https://img.shields.io/badge/FastAPI-localhost:8000/docs-0a1014?style=flat&logo=fastapi&logoColor=7fd1c6&labelColor=0d1a1f" alt="FastAPI" /></a>
  <a href="http://localhost:3000"><img src="https://img.shields.io/badge/Next.js-localhost:3000-0a1014?style=flat&logo=nextdotjs&logoColor=7fd1c6&labelColor=0d1a1f" alt="Next.js" /></a>
</p>

### Ejecutar por separado

```bash
make api          # Solo FastAPI
make frontend     # Solo Next.js
make streamlit    # Dashboard Streamlit heredado
```

---

## Targets de Make

| Target | Propósito |
|---|---|
| make install | uv sync — instala dependencias Python |
| make frontend-install | pnpm install — instala dependencias del frontend |
| make dev | Levanta **ambos** servidores (FastAPI + Next.js) en paralelo |
| make api | Solo FastAPI (uvicorn :8000) |
| make frontend | Solo Next.js (pnpm dev :3000) |
| make frontend-build | Build de producción de Next.js |
| make streamlit | Ejecuta la app Streamlit heredada |
| make docker-up / docker-down / docker-build / docker-logs | Ciclo Docker Compose |
| make jupyter | Arranca JupyterLab |
| make test | Ejecuta pytest |
| make clean | Limpia cachés y .next/ |

---

## Referencia de la API

<p>
  <b>URL base</b>&nbsp;
  <a href="http://localhost:8000"><img src="https://img.shields.io/badge/localhost:8000-0a1014?style=flat&logoColor=7fd1c6&labelColor=0d1a1f" alt="localhost:8000" /></a>
</p>

| Método | Ruta | Descripción |
|---|---|---|
| GET | /health | Liveness + estado del modelo |
| POST | /predict | Ejecuta la predicción de riesgo cardiovascular |
| GET | /history | Devuelve todas las evaluaciones guardadas |
| GET | /stats | KPIs agregados (totales, % alto riesgo, hoy) |
| GET | /eda | Payload agregado de EDA para los gráficos |
| GET | /model-info | Métricas del modelo seleccionado + alternativas |

### Payload POST /predict

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

Respuesta:

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

## Características del frontend

- **/[lang]** Panel clínico — tarjetas de KPI, evaluaciones recientes, pie de distribución de riesgo.
- **/[lang]/new-evaluation** Formulario clínico en tres secciones (Identificación, Constantes, Síntomas/ECG) con validación RHF + Zod. Al enviar, el resultado se renderiza como **ticket imprimible** (window.print() cambia la hoja de impresión para que solo el ticket salga, como un recibo térmico).
- **/[lang]/patients** Tabla de historial con búsqueda y filtros (alto / bajo / todos). Export a CSV en cliente.
- **/[lang]/eda** Gráficos: histograma de edad, distribución por sexo, distribución por tipo de dolor torácico y scatter Max HR vs Edad coloreado por outcome.
- **/[lang]/model** Tarjeta del modelo seleccionado, gráfico comparativo en barras y justificación.
- **/[lang]/settings** Selector de idioma y tema.

El layout es un **shell tipo CRM/EHR** con sidebar oscura sticky (logo + navegación + badge de la institución), cabecera con buscador de paciente, indicador de turno, selector de idioma, toggle de tema y avatar de la enfermería.

---

## Internacionalización

- Basada en los **dictionaries nativos de Next.js 16** (app/[lang]/...).
- Todos los textos viven en frontend/src/i18n/dictionaries/{en,es}.json.
- La detección de locale la realiza frontend/src/proxy.ts en este orden:
  1. Cookie locale (puesta por el selector de idioma),
  2. Header Accept-Language,
  3. Fallback a **inglés**.
- useT() expone el diccionario a los client components.

Para añadir un nuevo idioma: crea {xx}.json, añade xx a locales en src/i18n/config.ts y regístralo en src/i18n/dictionaries.ts.

---

## Temas

- El modo oscuro es el **predeterminado**.
- Los tokens viven como variables CSS en globals.css (:root claro, .dark oscuro) y se conectan con Tailwind v4 vía @theme inline.
- El ThemeProvider se monta en el **layout raíz** para evitar problemas de hidratación de next-themes.

---

## Pruebas

```bash
make test                  # pytest
cd frontend && pnpm build  # type-check + build de producción
```

---

## Docker

```bash
make docker-up      # Construye y arranca el contenedor de Streamlit
make docker-logs    # Stream de logs
make docker-down    # Para
```

> Containerizar el dúo Next.js + FastAPI está en la hoja de ruta.

---


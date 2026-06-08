# BeatSense: A Production-Grade Cardiovascular Risk Workstation Built Around a Logistic Regression

Most clinical machine learning prototypes share the same fate. A notebook is written, a model is trained, a Streamlit dashboard is glued on top, and the result is shown to stakeholders as proof that the underlying science works. The science usually does. What rarely works is the surface: it does not look like a tool a clinician would use at a hospital workstation.

BeatSense was built to close that gap. The model itself is intentionally simple, a logistic regression trained on 918 patient records from the Heart Disease dataset, with a deliberately low decision threshold. The novelty is not in the algorithm. It is in how the trained model is exposed, consumed and rendered for the actual environment where coronary risk assessments take place: a nurse station inside a cardiology unit.

This article walks through the full architecture of the project end to end. The dataset and the modelling decisions, the FastAPI service that wraps the model, the Next.js clinical workstation that consumes it, the ticket-style result rendering, the dual toolchain that orchestrates everything, and the design trade-offs behind each layer.

## The Problem

The classical heart disease dataset contains twelve clinical variables per patient. Age, sex, chest pain type, resting blood pressure, cholesterol, fasting blood sugar, resting ECG, max heart rate, exercise-induced angina, ST depression, ST slope, and a binary target indicating presence of heart disease.

Four candidate models were trained and benchmarked: logistic regression, random forest, k-nearest neighbors, and XGBoost. Random forest produced slightly higher raw accuracy. Logistic regression with a decision threshold lowered from 0.5 to 0.4 was the final selection. This is the most important technical decision in the project and the one that frames every downstream choice.

The argument is grounded in clinical cost asymmetry. In cardiology, false negatives and false positives have radically different costs. A false positive triggers additional examinations: stress test, 24-hour Holter monitoring, echocardiogram. The patient is inconvenienced; the system absorbs the workload. A false negative discharges a patient at real cardiovascular risk without follow-up. The downstream cost of that missed diagnosis dominates the cost of any number of false positives.

Optimising for accuracy under those conditions produces the wrong model. The correct metric to maximise is recall on the positive class, also called sensitivity. With the threshold at 0.4, logistic regression captured 94% of true positives in the test set. Random forest captured fewer. Two additional properties closed the case: train/test accuracy gap of 0.007, indicating no overfitting, and full interpretability through linear coefficients, which is non-negotiable in a clinical context where the model's reasoning must be auditable.

This single decision shapes the entire downstream architecture. The API exposes the same threshold. The UI surfaces the threshold and the probability side by side. The printed ticket annotates whether the score exceeds the decision boundary. Every layer of the system is consistent with the clinical optimisation target.

## The Architecture

BeatSense is structured as three coordinated surfaces sharing the same trained model.

```
┌─────────────────────────┐      HTTPS/REST       ┌────────────────────────┐
│ Next.js 16 frontend     │  ────────────────▶    │ FastAPI service        │
│ • App Router            │                       │ • /predict             │
│ • Server + Client       │                       │ • /history /stats      │
│   Components            │                       │ • /eda /model-info     │
│ • TanStack Query        │  ◀────────────────    │ • Loads .pkl + scaler  │
└─────────────┬───────────┘      JSON              └───────────┬────────────┘
              │                                                │
              ▼                                                ▼
        ┌──────────┐                                ┌─────────────────────┐
        │ /public  │                                │ models/             │
        │ assets   │                                │ historial CSV       │
        └──────────┘                                └─────────────────────┘
```

The backend serves the model. The frontend renders the clinical workstation. A legacy Streamlit surface is preserved for quick demonstrations and shares the same persistent history file.

## The Backend: Faithfully Exposing the Model

The FastAPI service exists for one reason: scikit-learn artifacts cannot be loaded directly from a JavaScript runtime. A thin Python service wraps the pickled estimator and serves predictions over JSON.

The non-trivial part is reproducing the exact preprocessing pipeline used during training. If the production service builds features in a different order, applies a different encoding, or scales different columns, predictions drift silently and the model becomes useless. The build function mirrors the training notebook one to one:

```python
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

    X = pd.DataFrame([[
        req.age, sex_num, req.max_hr, req.fasting_bs,
        exercise_bin, cp_asy, cp_ata, cp_nap, cp_ta,
        st_flat, st_up, st_down,
    ]], columns=[
        "Age", "Sex", "MaxHR", "FastingBS", "ExerciseAngina",
        "CP_ASY", "CP_ATA", "CP_NAP", "CP_TA",
        "ST_Slope_Flat", "ST_Slope_Up", "ST_Slope_Down",
    ])
    X[["Age", "MaxHR"]] = scaler.transform(X[["Age", "MaxHR"]])
    return X
```

Twelve features in a fixed order. Only Age and MaxHR are scaled, exactly as in training. The classification head applies the 0.4 threshold inside the response handler, so the calling client never has to know how to interpret the raw probability.

Validation of the migration was empirical. A representative test case was passed through both the legacy Streamlit pipeline and the new FastAPI service. The probabilities matched to four decimal places: 94.28225938492596. The numerical agreement is the only acceptable correctness signal when migrating an ML service. Anything less indicates a silent regression.

Five endpoints are exposed in total. `/predict` runs the model and persists the assessment to a shared CSV. `/history` returns the full assessment log. `/stats` aggregates totals for the dashboard. `/eda` returns precomputed distributions for the analytics charts. `/model-info` exposes the metrics of the selected model alongside the alternatives that were evaluated.

Persisting predictions to the same CSV used by the legacy Streamlit surface keeps the two interfaces consistent. A patient evaluated through Streamlit appears in the Next.js patient history without any synchronisation layer.

## The Frontend: A Clinical Workstation, Not a Dashboard

The design brief for the frontend was deliberately narrow. The interface should match the visual and ergonomic conventions of a hospital EHR-style workstation, not those of a marketing landing page. Specifically: a dense dark sidebar with primary navigation, a header with a patient search field and clinician identity, tables with status badges, sans-serif type for the UI, monospace type for clinical data, and a result format that mirrors the printed receipts familiar to clinical workflows.

The implementation uses Next.js 16 with the App Router, React 19, TypeScript, Tailwind v4, shadcn-style components on top of Radix UI primitives, TanStack Query for server-state caching, React Hook Form with Zod for form validation, Recharts for analytics, and next-themes for dark mode. The package manager is pnpm.

Next.js 16 introduced changes that affect the layout. Middleware is renamed `proxy.ts`. Page `params` are asynchronous and must be awaited. Native locale-aware dictionaries are available without external i18n libraries. The architecture takes advantage of all three.

The route tree is organised under a dynamic `[lang]` segment. The root layout mounts the global font variables and the theme provider. The locale-scoped layout mounts the sidebar, header, and the query and i18n providers. Each page is a Server Component that loads the dictionary and delegates interactive parts to Client Components.

One non-obvious detail concerns the placement of the theme provider. The `next-themes` package injects an inline script tag to prevent a flash of the wrong theme on first paint. Under React 19, that script tag must be a direct descendant of `<body>`, not nested inside another Client Component. Placing the `ThemeProvider` in the locale-scoped layout produced a hydration warning. Moving it to the root layout, immediately inside `<body>`, resolved it cleanly.

```tsx
export default function RootLayout({ children }) {
  return (
    <html suppressHydrationWarning>
      <body className={`${inter.variable} ${mono.variable} antialiased`}>
        <ThemeRoot>{children}</ThemeRoot>
      </body>
    </html>
  );
}
```

## The Clinical Form

The new evaluation form is structured in three sections that follow the natural intake order: patient identification, vitals and lab values, symptoms and ECG findings. The form uses React Hook Form for state management and Zod for runtime validation. Required clinical fields are constrained to physiological ranges. Optional fields, such as resting blood pressure or cholesterol, accept either a numeric value or an empty string.

Handling that union cleanly requires a small Zod transform:

```typescript
const numberOrEmpty = z
  .union([z.string(), z.number()])
  .transform((v) => {
    if (typeof v === "number") return v;
    if (v === "" || v == null) return undefined;
    const n = Number(v);
    return Number.isFinite(n) ? n : undefined;
  })
  .optional();
```

Empty strings become `undefined`, string-encoded numbers are parsed, invalid input is normalised away. When the schema declares transforms, `useForm` must be parameterised with three generics: input type, context, and output type. Without the third generic, TypeScript will refuse to type `onSubmit` arguments correctly.

```typescript
useForm<FormValues, unknown, FormOutput>({
  resolver: zodResolver(schema),
  defaultValues: DEFAULTS,
});
```

## The Ticket: Treating the Output as a Clinical Artifact

The result of a prediction is not rendered as a modal or a card. It is rendered as a thermal-printer ticket, fixed at 420 pixels wide, in JetBrains Mono, with dotted dividers, an institutional header, patient and clinician metadata, the full clinical snapshot, the probability score in large type, the classification badge, a probability bar showing the decision threshold marker, the recommendation, a decorative barcode and a footer.

The barcode is a visual signal, not a scannable code. It is generated deterministically from the patient identifier so that two evaluations of the same patient produce visually consistent tickets without storing additional state:

```typescript
function Barcode({ value }: { value: string }) {
  const bars = Array.from(value).flatMap((c, i) => {
    const code = c.charCodeAt(0) + i;
    return [
      { w: (code % 4) + 1, gap: 1 },
      { w: ((code >> 2) % 3) + 1, gap: 2 },
    ];
  });
  return (
    <div className="flex flex-col items-center">
      <div className="flex h-10 items-end gap-[1px]">
        {bars.map((b, i) => (
          <div key={i} className="bg-foreground"
            style={{ width: `${b.w}px`, height: "100%" }} />
        ))}
      </div>
      <div className="mt-1 font-mono text-[10px] tracking-widest">{value}</div>
    </div>
  );
}
```

The decisive feature of the ticket is that it prints. A header button triggers `window.print()`, and a global print stylesheet hides everything outside the ticket container. The output is a clean monochrome page sized to the ticket, ready to be physically attached to the patient record:

```css
@media print {
  body * { visibility: hidden; }
  .print-area, .print-area * { visibility: visible; }
  .print-area {
    position: absolute;
    left: 0; top: 0;
    width: 100%;
    background: #fff !important;
    color: #000 !important;
  }
}
```

This single piece of functionality changes how the application is perceived. The result stops feeling like screen output and starts feeling like a clinical document.

## Internationalization Without Compromises

The interface ships with zero hardcoded strings. Every label, button, error message and field name is loaded from a JSON dictionary. English is the default. Spanish is the second supported locale. Additional languages require only a new JSON file and an entry in the locale registry.

The implementation uses the native dictionary pattern in Next.js 16. Server Components load the dictionary directly. Client Components receive it through a small React context exposing a `useT()` hook. Locale resolution is performed inside the proxy (middleware) in a deterministic order: an explicit locale cookie set by the language switcher, the browser's `Accept-Language` header, and a fallback to English.

```typescript
function pickLocale(request: NextRequest): string {
  const cookie = request.cookies.get("locale")?.value;
  if (cookie && (locales as readonly string[]).includes(cookie)) return cookie;
  const header = request.headers.get("accept-language") ?? "";
  for (const part of header.split(",")) {
    const code = part.split(";")[0].trim().toLowerCase().split("-")[0];
    if ((locales as readonly string[]).includes(code)) return code;
  }
  return defaultLocale;
}
```

This pattern keeps locale state outside React, prevents flashes of the wrong language during navigation, and removes the need for an external i18n library.

## The Toolchain

The repository uses two package managers: uv for Python and pnpm for Node.js. Both are designed around reproducible lockfiles and aggressive caching. A single Make target orchestrates the dual stack:

```makefile
dev:
	@trap 'kill 0' INT; \
	uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000 & \
	(cd frontend && pnpm dev) & \
	wait
```

`make dev` starts the FastAPI service on port 8000 and the Next.js development server on port 3000 in parallel, propagates interrupts to both child processes, and keeps the developer in a single terminal. The same Makefile exposes targets for production builds, the legacy Streamlit surface, Docker Compose, JupyterLab and pytest.

## Design Principles Behind the System

A few principles guided the architecture and are worth stating explicitly.

**Optimisation metric drives model selection.** In any domain with asymmetric error costs, choosing the metric is more impactful than choosing the algorithm. Maximising recall on the positive class is the correct objective for coronary risk assessment, and the choice of logistic regression with a lowered threshold follows directly from it.

**Reproducibility of preprocessing is the integrity boundary.** Any divergence between the training preprocessing and the inference preprocessing produces silent failures. The only acceptable validation is end-to-end numerical agreement.

**Surface design encodes credibility.** Identical predictions carry different weight depending on the surface that delivers them. A printable ticket carries authority. A modal does not. The frontend is engineered around that asymmetry.

**Internationalisation is cheap at the start and expensive later.** Building with a JSON dictionary from the first commit costs nothing. Retrofitting it after hardcoded strings have spread through the codebase is a multi-day undertaking.

**Tooling unification removes friction.** A single `make dev` boots the entire system. A single lockfile per language guarantees reproducibility. The cognitive cost of the development environment is kept close to zero.

## What Is Next

Several extensions are planned and tracked. A combined Docker image bundling FastAPI and Next.js for single-container deployment on managed platforms. Authentication so every assessment is signed by an authenticated clinician identity. Multi-tenant support to allow separate cardiology units to share infrastructure without mixing patient data. SHAP-based explanations rendered directly on the ticket, so the clinician sees which variables pushed the prediction in either direction. PDF export as an alternative to direct printing.

The core architecture is in place to accommodate all of these without structural changes.

## Try It and Contribute

BeatSense is open source. The full source code is available on GitHub. A working demo is hosted as a Hugging Face Space.

<p>
  <a href="https://github.com/iRuperth/BeatSense"><img src="https://img.shields.io/badge/GitHub-iRuperth%2FBeatSense-0a1014?style=flat&logo=github&logoColor=7fd1c6&labelColor=0d1a1f" alt="GitHub" /></a>
  <a href="https://huggingface.co/spaces/devrup404/BeatSense"><img src="https://img.shields.io/badge/Hugging%20Face-Open%20Space-0a1014?style=flat&logo=huggingface&logoColor=7fd1c6&labelColor=0d1a1f" alt="Hugging Face Space" /></a>
</p>

Pull requests, issue reports and design proposals are welcome. If the system is extended into a related clinical domain or adapted for production deployment in a healthcare setting, please share the experience back. The architecture is intended to be reused, not just read about.

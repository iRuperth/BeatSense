"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import {
  Heart,
  Stethoscope,
  ClipboardList,
  Loader2,
  RotateCcw,
  Activity,
} from "lucide-react";
import { useT } from "@/i18n/context";
import { api, type PredictRequest, type PredictResponse } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Ticket } from "@/components/ticket/ticket";

const numberOrEmpty = z
  .union([z.string(), z.number()])
  .transform((v) => {
    if (typeof v === "number") return v;
    if (v === "" || v == null) return undefined;
    const n = Number(v);
    return Number.isFinite(n) ? n : undefined;
  })
  .optional();

const requiredNumber = z
  .union([z.string(), z.number()])
  .transform((v) => Number(v))
  .refine((n) => Number.isFinite(n), { message: "Invalid number" });

const schema = z.object({
  patient_id: z.string().max(64).optional(),
  age: requiredNumber.refine((n) => n >= 1 && n <= 120, "Age out of range"),
  sex: z.enum(["M", "F"]),
  resting_bp: numberOrEmpty,
  cholesterol: numberOrEmpty,
  max_hr: requiredNumber.refine((n) => n >= 40 && n <= 240, "HR out of range"),
  fasting_bs: z.enum(["0", "1"]),
  exercise_angina: z.enum(["Y", "N"]),
  chest_pain_type: z.enum(["ASY", "ATA", "NAP", "TA"]),
  resting_ecg: z.enum(["Normal", "ST", "LVH"]).optional(),
  st_slope: z.enum(["Up", "Flat", "Down"]),
  oldpeak: numberOrEmpty,
});

type FormValues = z.input<typeof schema>;
type FormOutput = z.output<typeof schema>;

const DEFAULTS: Partial<FormValues> = {
  patient_id: "",
  sex: "M",
  fasting_bs: "0",
  exercise_angina: "N",
  chest_pain_type: "ASY",
  resting_ecg: "Normal",
  st_slope: "Flat",
};

export function EvaluationForm() {
  const { dict } = useT();
  const [result, setResult] = useState<{
    response: PredictResponse;
    snapshot: FormOutput;
  } | null>(null);

  const {
    register,
    handleSubmit,
    reset,
    setValue,
    watch,
    formState: { errors },
  } = useForm<FormValues, unknown, FormOutput>({
    resolver: zodResolver(schema),
    defaultValues: DEFAULTS,
  });

  const mutation = useMutation({
    mutationFn: (values: PredictRequest) => api.predict(values),
  });

  const onSubmit = handleSubmit(async (values) => {
    const payload: PredictRequest = {
      patient_id: values.patient_id || null,
      age: values.age,
      sex: values.sex,
      chest_pain_type: values.chest_pain_type,
      max_hr: values.max_hr,
      fasting_bs: Number(values.fasting_bs) as 0 | 1,
      exercise_angina: values.exercise_angina,
      st_slope: values.st_slope,
      resting_bp: values.resting_bp ?? null,
      cholesterol: values.cholesterol ?? null,
      resting_ecg: values.resting_ecg ?? null,
      oldpeak: values.oldpeak ?? null,
    };
    const response = await mutation.mutateAsync(payload);
    setResult({ response, snapshot: values });
  });

  if (result) {
    return (
      <Ticket
        response={result.response}
        snapshot={result.snapshot}
        onNew={() => {
          setResult(null);
          reset(DEFAULTS);
        }}
      />
    );
  }

  return (
    <form onSubmit={onSubmit} className="space-y-6">
      <Card>
        <CardContent className="grid gap-6 p-6">
          <SectionTitle
            icon={<ClipboardList className="h-4 w-4" />}
            label={dict.form.sections.demographics}
          />
          <div className="grid gap-4 sm:grid-cols-3">
            <Field
              label={dict.form.fields.patientId}
              error={errors.patient_id?.message}
            >
              <Input
                placeholder={dict.form.fields.patientIdPlaceholder}
                {...register("patient_id")}
              />
            </Field>
            <Field label={dict.form.fields.age} error={errors.age?.message}>
              <Input
                type="number"
                min={1}
                max={120}
                {...register("age")}
              />
            </Field>
            <Field label={dict.form.fields.sex} error={errors.sex?.message}>
              <Select
                value={watch("sex")}
                onValueChange={(v) => setValue("sex", v as "M" | "F")}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="M">{dict.common.male}</SelectItem>
                  <SelectItem value="F">{dict.common.female}</SelectItem>
                </SelectContent>
              </Select>
            </Field>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="grid gap-6 p-6">
          <SectionTitle
            icon={<Activity className="h-4 w-4" />}
            label={dict.form.sections.vitals}
          />
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <Field
              label={dict.form.fields.restingBp}
              error={errors.resting_bp?.message}
            >
              <Input type="number" min={60} max={250} {...register("resting_bp")} />
            </Field>
            <Field
              label={dict.form.fields.cholesterol}
              error={errors.cholesterol?.message}
            >
              <Input type="number" min={0} max={700} {...register("cholesterol")} />
            </Field>
            <Field label={dict.form.fields.maxHr} error={errors.max_hr?.message}>
              <Input type="number" min={40} max={240} {...register("max_hr")} />
            </Field>
            <Field
              label={dict.form.fields.fastingBs}
              error={errors.fasting_bs?.message}
            >
              <Select
                value={watch("fasting_bs")}
                onValueChange={(v) =>
                  setValue("fasting_bs", v as "0" | "1")
                }
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="0">{dict.common.no}</SelectItem>
                  <SelectItem value="1">{dict.common.yes}</SelectItem>
                </SelectContent>
              </Select>
            </Field>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="grid gap-6 p-6">
          <SectionTitle
            icon={<Stethoscope className="h-4 w-4" />}
            label={dict.form.sections.symptoms}
          />
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <Field
              label={dict.form.fields.chestPainType}
              error={errors.chest_pain_type?.message}
            >
              <Select
                value={watch("chest_pain_type")}
                onValueChange={(v) =>
                  setValue("chest_pain_type", v as FormValues["chest_pain_type"])
                }
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {(["ASY", "ATA", "NAP", "TA"] as const).map((k) => (
                    <SelectItem key={k} value={k}>
                      {dict.form.options.chestPain[k]}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </Field>

            <Field
              label={dict.form.fields.exerciseAngina}
              error={errors.exercise_angina?.message}
            >
              <Select
                value={watch("exercise_angina")}
                onValueChange={(v) =>
                  setValue("exercise_angina", v as "Y" | "N")
                }
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="N">{dict.common.no}</SelectItem>
                  <SelectItem value="Y">{dict.common.yes}</SelectItem>
                </SelectContent>
              </Select>
            </Field>

            <Field
              label={dict.form.fields.restingEcg}
              error={errors.resting_ecg?.message}
            >
              <Select
                value={watch("resting_ecg") ?? "Normal"}
                onValueChange={(v) =>
                  setValue("resting_ecg", v as FormValues["resting_ecg"])
                }
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {(["Normal", "ST", "LVH"] as const).map((k) => (
                    <SelectItem key={k} value={k}>
                      {dict.form.options.restingEcg[k]}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </Field>

            <Field
              label={dict.form.fields.stSlope}
              error={errors.st_slope?.message}
            >
              <Select
                value={watch("st_slope")}
                onValueChange={(v) =>
                  setValue("st_slope", v as FormValues["st_slope"])
                }
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {(["Up", "Flat", "Down"] as const).map((k) => (
                    <SelectItem key={k} value={k}>
                      {dict.form.options.stSlope[k]}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </Field>

            <Field
              label={dict.form.fields.oldpeak}
              error={errors.oldpeak?.message}
            >
              <Input
                type="number"
                step="0.1"
                min={-5}
                max={10}
                {...register("oldpeak")}
              />
            </Field>
          </div>
        </CardContent>
      </Card>

      {mutation.error && (
        <div className="rounded-md border border-destructive bg-destructive/10 px-4 py-3 text-sm text-destructive">
          {dict.result.error}
        </div>
      )}

      <div className="flex flex-wrap items-center justify-end gap-3">
        <Button
          type="button"
          variant="ghost"
          onClick={() => reset(DEFAULTS)}
          disabled={mutation.isPending}
        >
          <RotateCcw className="h-4 w-4" />
          {dict.form.actions.reset}
        </Button>
        <Button type="submit" size="lg" disabled={mutation.isPending}>
          {mutation.isPending ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <Heart className="h-4 w-4" />
          )}
          {mutation.isPending ? dict.result.predicting : dict.form.actions.submit}
        </Button>
      </div>
    </form>
  );
}

function SectionTitle({
  icon,
  label,
}: {
  icon: React.ReactNode;
  label: string;
}) {
  return (
    <div className="flex items-center gap-2 border-b border-border pb-3">
      <div className="flex h-7 w-7 items-center justify-center rounded-md bg-primary/10 text-primary">
        {icon}
      </div>
      <span className="text-sm font-semibold tracking-wide">{label}</span>
    </div>
  );
}

function Field({
  label,
  error,
  children,
}: {
  label: string;
  error?: string;
  children: React.ReactNode;
}) {
  return (
    <div className="space-y-1.5">
      <Label>{label}</Label>
      {children}
      {error && <p className="text-xs text-destructive">{error}</p>}
    </div>
  );
}

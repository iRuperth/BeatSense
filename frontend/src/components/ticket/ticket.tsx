"use client";

import { useRef } from "react";
import Image from "next/image";
import { Printer, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useT } from "@/i18n/context";
import type { PredictResponse } from "@/lib/api";

export type FormSnapshot = {
  patient_id?: string;
  age: number;
  sex: "M" | "F";
  max_hr: number;
  fasting_bs: "0" | "1";
  exercise_angina: "Y" | "N";
  chest_pain_type: "ASY" | "ATA" | "NAP" | "TA";
  st_slope: "Up" | "Flat" | "Down";
  resting_bp?: number;
  cholesterol?: number;
  resting_ecg?: "Normal" | "ST" | "LVH";
  oldpeak?: number;
};

export function Ticket({
  response,
  snapshot,
  onNew,
}: {
  response: PredictResponse;
  snapshot: FormSnapshot;
  onNew: () => void;
}) {
  const { dict } = useT();
  const ticketRef = useRef<HTMLDivElement>(null);

  const ts = new Date(response.timestamp);
  const date = ts.toLocaleDateString();
  const time = ts.toLocaleTimeString();
  const isHigh = response.classification === "HIGH";

  return (
    <div className="mx-auto max-w-2xl space-y-4">
      <div className="flex justify-end gap-2 print:hidden">
        <Button variant="outline" onClick={onNew}>
          <Plus className="h-4 w-4" />
          {dict.ticket.newAssessment}
        </Button>
        <Button onClick={() => window.print()}>
          <Printer className="h-4 w-4" />
          {dict.common.print}
        </Button>
      </div>

      <div
        ref={ticketRef}
        className="print-area mx-auto rounded-lg border border-dashed border-foreground/30 bg-card p-8 font-mono text-[13px] leading-relaxed text-foreground shadow-2xl print:shadow-none"
        style={{ maxWidth: "420px" }}
      >
        <div className="flex flex-col items-center gap-2 pb-3 text-center">
          <div className="flex h-14 w-14 items-center justify-center overflow-hidden rounded-md">
            <Image
              src="/logu1.png"
              alt="BeatSense"
              width={56}
              height={56}
              className="h-12 w-12 object-contain"
            />
          </div>
          <div className="text-base font-bold tracking-widest uppercase">
            {dict.app.name}
          </div>
          <div className="text-[10px] uppercase tracking-wider opacity-70">
            {dict.ticket.facility}
          </div>
        </div>

        <Divider />

        <div className="grid grid-cols-2 gap-y-1 text-[12px]">
          <span className="opacity-70">{dict.ticket.code}</span>
          <span className="text-right font-bold">{response.patient_id}</span>
          <span className="opacity-70">{dict.ticket.date}</span>
          <span className="text-right">{date}</span>
          <span className="opacity-70">{dict.ticket.time}</span>
          <span className="text-right">{time}</span>
          <span className="opacity-70">{dict.ticket.clinician}</span>
          <span className="text-right">{dict.header.user}</span>
        </div>

        <Divider />

        <div className="text-[10px] uppercase tracking-widest opacity-70">
          {dict.ticket.vitals}
        </div>
        <div className="mt-2 space-y-0.5 text-[12px]">
          <Row label={dict.form.fields.age} value={`${snapshot.age}`} />
          <Row
            label={dict.form.fields.sex}
            value={snapshot.sex === "M" ? dict.common.male : dict.common.female}
          />
          {snapshot.resting_bp ? (
            <Row
              label={dict.form.fields.restingBp}
              value={`${snapshot.resting_bp} mmHg`}
            />
          ) : null}
          {snapshot.cholesterol ? (
            <Row
              label={dict.form.fields.cholesterol}
              value={`${snapshot.cholesterol} mg/dL`}
            />
          ) : null}
          <Row
            label={dict.form.fields.maxHr}
            value={`${snapshot.max_hr} bpm`}
          />
          <Row
            label={dict.form.fields.fastingBs}
            value={snapshot.fasting_bs === "1" ? dict.common.yes : dict.common.no}
          />
          <Row
            label={dict.form.fields.chestPainType}
            value={snapshot.chest_pain_type}
          />
          <Row
            label={dict.form.fields.exerciseAngina}
            value={
              snapshot.exercise_angina === "Y" ? dict.common.yes : dict.common.no
            }
          />
          <Row label={dict.form.fields.stSlope} value={snapshot.st_slope} />
        </div>

        <Divider />

        <div className="text-center">
          <div className="text-[10px] uppercase tracking-widest opacity-70">
            {dict.ticket.result}
          </div>
          <div className="mt-2 text-4xl font-black">
            {response.probability.toFixed(1)}%
          </div>
          <div className="mt-1 text-[10px] uppercase opacity-60">
            {dict.ticket.riskScore} · {dict.ticket.threshold}: {response.threshold}%
          </div>
          <div
            className={`mt-3 inline-block rounded-sm border-2 px-3 py-1 text-sm font-bold tracking-widest ${
              isHigh
                ? "border-destructive text-destructive"
                : "border-success text-success"
            }`}
          >
            {isHigh ? dict.ticket.highRisk : dict.ticket.lowRisk}
          </div>
          <ProbabilityBar value={response.probability} threshold={response.threshold} />
        </div>

        <Divider />

        <div className="text-[10px] uppercase tracking-widest opacity-70">
          {dict.ticket.recommendation}
        </div>
        <p className="mt-1 text-[12px]">
          {isHigh ? dict.ticket.recHigh : dict.ticket.recLow}
        </p>

        <Divider />

        <div className="mt-2 flex flex-col items-center gap-2 text-[10px] opacity-70">
          <Barcode value={response.patient_id} />
          <div className="text-center">{dict.ticket.footer}</div>
        </div>
      </div>
    </div>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between gap-2">
      <span className="opacity-70">{label}</span>
      <span className="text-right font-medium">{value}</span>
    </div>
  );
}

function Divider() {
  return (
    <div
      className="my-3 h-px w-full"
      style={{
        background:
          "repeating-linear-gradient(90deg, currentColor 0 4px, transparent 4px 8px)",
        opacity: 0.4,
      }}
    />
  );
}

function ProbabilityBar({
  value,
  threshold,
}: {
  value: number;
  threshold: number;
}) {
  return (
    <div className="mt-3">
      <div className="relative h-2 w-full overflow-hidden rounded-sm border border-foreground/30">
        <div
          className="h-full"
          style={{
            width: `${Math.min(100, value)}%`,
            background: value >= threshold ? "var(--destructive)" : "var(--success)",
          }}
        />
        <div
          className="absolute top-0 h-full w-px bg-foreground/80"
          style={{ left: `${threshold}%` }}
        />
      </div>
      <div className="mt-1 flex justify-between font-mono text-[9px] opacity-60">
        <span>0%</span>
        <span>{threshold}%</span>
        <span>100%</span>
      </div>
    </div>
  );
}

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
          <div
            key={i}
            className="bg-foreground"
            style={{ width: `${b.w}px`, height: "100%" }}
          />
        ))}
      </div>
      <div className="mt-1 font-mono text-[10px] tracking-widest">{value}</div>
    </div>
  );
}

"use client";

import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Download, Search } from "lucide-react";
import { api, type HistoryEntry } from "@/lib/api";
import { useT } from "@/i18n/context";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

type Filter = "all" | "high" | "low";

export function PatientsTable() {
  const { dict } = useT();
  const [query, setQuery] = useState("");
  const [filter, setFilter] = useState<Filter>("all");

  const { data } = useQuery({ queryKey: ["history"], queryFn: api.history });

  const rows = useMemo(() => {
    let r = [...(data ?? [])].reverse();
    if (filter === "high") r = r.filter((x) => x.risk === "ALTO");
    if (filter === "low") r = r.filter((x) => x.risk !== "ALTO");
    if (query.trim())
      r = r.filter((x) =>
        x.patient_id.toLowerCase().includes(query.toLowerCase())
      );
    return r;
  }, [data, query, filter]);

  function exportCsv() {
    const headers = [
      "Date","Time","Patient ID","Age","Sex","Max HR","Fasting BS","Exercise Angina","Chest Pain","ST Slope","Probability","Risk",
    ];
    const lines = [
      headers.join(","),
      ...rows.map((r: HistoryEntry) =>
        [
          r.date,
          r.time,
          r.patient_id,
          r.age,
          r.sex,
          r.max_hr,
          r.fasting_bs,
          r.exercise_angina,
          r.chest_pain_type,
          r.st_slope,
          r.probability,
          r.risk,
        ].join(",")
      ),
    ];
    const blob = new Blob([lines.join("\n")], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `beatsense-patients-${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <Card>
      <CardContent className="space-y-4 p-6">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="relative">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={dict.history.search}
              className="h-9 w-72 rounded-md border border-input bg-background pl-9 pr-3 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
            />
          </div>
          <div className="flex items-center gap-2">
            <FilterButton
              label={dict.history.filterAll}
              active={filter === "all"}
              onClick={() => setFilter("all")}
            />
            <FilterButton
              label={dict.history.filterHigh}
              active={filter === "high"}
              onClick={() => setFilter("high")}
            />
            <FilterButton
              label={dict.history.filterLow}
              active={filter === "low"}
              onClick={() => setFilter("low")}
            />
            <Button variant="outline" size="sm" onClick={exportCsv}>
              <Download className="h-4 w-4" />
              {dict.common.export}
            </Button>
          </div>
        </div>

        <div className="overflow-x-auto rounded-md border border-border">
          <table className="w-full text-sm">
            <thead className="bg-muted/40 text-xs uppercase tracking-wide text-muted-foreground">
              <tr>
                <Th>{dict.history.columns.date}</Th>
                <Th>{dict.history.columns.time}</Th>
                <Th>{dict.history.columns.patientId}</Th>
                <Th className="text-right">{dict.history.columns.age}</Th>
                <Th>{dict.history.columns.sex}</Th>
                <Th className="text-right">{dict.history.columns.maxHr}</Th>
                <Th>{dict.history.columns.fastingBs}</Th>
                <Th>{dict.history.columns.exerciseAngina}</Th>
                <Th>{dict.history.columns.chestPain}</Th>
                <Th>{dict.history.columns.stSlope}</Th>
                <Th className="text-right">{dict.history.columns.probability}</Th>
                <Th className="text-right">{dict.history.columns.risk}</Th>
              </tr>
            </thead>
            <tbody>
              {rows.length === 0 ? (
                <tr>
                  <td
                    colSpan={12}
                    className="py-10 text-center text-muted-foreground"
                  >
                    {dict.common.noData}
                  </td>
                </tr>
              ) : (
                rows.map((r, i) => (
                  <tr key={`${r.patient_id}-${i}`} className="border-t border-border hover:bg-muted/20">
                    <Td>{r.date}</Td>
                    <Td>{r.time}</Td>
                    <Td className="font-mono text-xs">{r.patient_id}</Td>
                    <Td className="text-right">{r.age}</Td>
                    <Td>{r.sex}</Td>
                    <Td className="text-right">{r.max_hr}</Td>
                    <Td>{r.fasting_bs}</Td>
                    <Td>{r.exercise_angina}</Td>
                    <Td>{r.chest_pain_type}</Td>
                    <Td>{r.st_slope}</Td>
                    <Td className="text-right font-semibold">
                      {r.probability.toFixed(1)}%
                    </Td>
                    <Td className="text-right">
                      <Badge
                        variant={r.risk === "ALTO" ? "destructive" : "success"}
                      >
                        {r.risk === "ALTO" ? dict.common.high : dict.common.low}
                      </Badge>
                    </Td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
}

function FilterButton({
  label,
  active,
  onClick,
}: {
  label: string;
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={`h-9 rounded-md border px-3 text-xs font-medium transition-colors ${
        active
          ? "border-primary bg-primary/10 text-primary"
          : "border-border bg-card text-muted-foreground hover:text-foreground"
      }`}
    >
      {label}
    </button>
  );
}

function Th({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <th className={`px-3 py-2 text-left ${className ?? ""}`}>{children}</th>
  );
}

function Td({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return <td className={`px-3 py-2 ${className ?? ""}`}>{children}</td>;
}

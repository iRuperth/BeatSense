"use client";

import { useQuery } from "@tanstack/react-query";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { CheckCircle2 } from "lucide-react";
import { api } from "@/lib/api";
import { useT } from "@/i18n/context";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export function ModelInsights() {
  const { dict } = useT();
  const { data, isLoading } = useQuery({
    queryKey: ["model-info"],
    queryFn: api.modelInfo,
  });

  if (isLoading || !data) {
    return (
      <Card>
        <CardContent className="p-10 text-center text-sm text-muted-foreground">
          {dict.common.loading}
        </CardContent>
      </Card>
    );
  }

  const all = [
    {
      name: data.name,
      accuracy: data.metrics.accuracy,
      recall: data.metrics.recall,
      roc_auc: data.metrics.roc_auc,
      selected: true,
    },
    ...data.alternatives.map((a) => ({ ...a, selected: false })),
  ];

  const chartData = all.map((m) => ({
    name: m.name,
    Accuracy: +(m.accuracy * 100).toFixed(1),
    Recall: +(m.recall * 100).toFixed(1),
    "ROC-AUC": +(m.roc_auc * 100).toFixed(1),
  }));

  return (
    <div className="grid gap-6 lg:grid-cols-3">
      <Card className="lg:col-span-1">
        <CardContent className="p-6">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="h-5 w-5 text-success" />
            <h2 className="text-sm font-semibold uppercase tracking-wide text-muted-foreground">
              {dict.model.selected}
            </h2>
          </div>
          <div className="mt-3 text-2xl font-bold">{data.name}</div>
          <Badge variant="success" className="mt-2">
            threshold {data.threshold}%
          </Badge>

          <div className="mt-6 grid grid-cols-2 gap-3">
            <Metric label={dict.model.metrics.accuracy} value={`${(data.metrics.accuracy * 100).toFixed(0)}%`} />
            <Metric label={dict.model.metrics.recall} value={data.metrics.recall.toFixed(2)} />
            <Metric label={dict.model.metrics.rocAuc} value={data.metrics.roc_auc.toFixed(3)} />
            <Metric
              label={dict.model.metrics.cv}
              value={`${(data.metrics.cv_mean * 100).toFixed(1)}% ± ${(data.metrics.cv_std * 100).toFixed(1)}`}
            />
          </div>
        </CardContent>
      </Card>

      <Card className="lg:col-span-2">
        <CardContent className="p-6">
          <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-muted-foreground">
            {dict.model.comparison}
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="name" tick={{ fontSize: 11 }} stroke="var(--muted-foreground)" />
              <YAxis tick={{ fontSize: 11 }} stroke="var(--muted-foreground)" unit="%" />
              <Tooltip
                contentStyle={{
                  background: "var(--popover)",
                  border: "1px solid var(--border)",
                  borderRadius: 8,
                  fontSize: 12,
                }}
              />
              <Legend wrapperStyle={{ fontSize: 12 }} />
              <Bar dataKey="Accuracy" fill="var(--primary)" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Recall" fill="var(--success)" radius={[4, 4, 0, 0]} />
              <Bar dataKey="ROC-AUC" fill="var(--accent-foreground)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card className="lg:col-span-3">
        <CardContent className="p-6">
          <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted-foreground">
            {dict.model.rationale}
          </h2>
          <p className="text-sm leading-relaxed">{dict.model.rationaleText}</p>
        </CardContent>
      </Card>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-border bg-muted/30 p-3">
      <div className="text-[10px] uppercase tracking-wide text-muted-foreground">
        {label}
      </div>
      <div className="mt-1 text-lg font-bold tabular-nums">{value}</div>
    </div>
  );
}

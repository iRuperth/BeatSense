"use client";

import { useQuery } from "@tanstack/react-query";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  ScatterChart,
  Scatter,
  Legend,
  Cell,
  PieChart,
  Pie,
} from "recharts";
import { api } from "@/lib/api";
import { useT } from "@/i18n/context";
import { Card, CardContent } from "@/components/ui/card";

const TOOLTIP = {
  contentStyle: {
    background: "var(--popover)",
    border: "1px solid var(--border)",
    borderRadius: 8,
    fontSize: 12,
    color: "var(--popover-foreground)",
  },
  cursor: { fill: "var(--muted)", opacity: 0.3 },
};

export function EdaCharts() {
  const { dict } = useT();
  const { data, isLoading } = useQuery({ queryKey: ["eda"], queryFn: api.eda });

  if (isLoading || !data) {
    return (
      <Card>
        <CardContent className="p-10 text-center text-sm text-muted-foreground">
          {dict.common.loading}
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <ChartCard title={dict.eda.ageDist}>
        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={data.age_dist}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
            <XAxis dataKey="bin" tick={{ fontSize: 10 }} stroke="var(--muted-foreground)" />
            <YAxis tick={{ fontSize: 10 }} stroke="var(--muted-foreground)" />
            <Tooltip {...TOOLTIP} />
            <Bar dataKey="count" fill="var(--primary)" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </ChartCard>

      <ChartCard title={dict.eda.sexDist}>
        <ResponsiveContainer width="100%" height={280}>
          <PieChart>
            <Pie
              data={data.sex_dist}
              dataKey="count"
              nameKey="sex"
              innerRadius={50}
              outerRadius={90}
              label
            >
              {data.sex_dist.map((_, i) => (
                <Cell key={i} fill={i === 0 ? "var(--primary)" : "var(--accent)"} />
              ))}
            </Pie>
            <Tooltip {...TOOLTIP} />
            <Legend wrapperStyle={{ fontSize: 12 }} />
          </PieChart>
        </ResponsiveContainer>
      </ChartCard>

      <ChartCard title={dict.eda.chestPainDist}>
        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={data.chest_pain_dist}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
            <XAxis dataKey="type" tick={{ fontSize: 11 }} stroke="var(--muted-foreground)" />
            <YAxis tick={{ fontSize: 11 }} stroke="var(--muted-foreground)" />
            <Tooltip {...TOOLTIP} />
            <Bar dataKey="count" fill="var(--primary)" radius={[4, 4, 0, 0]} />
            <Bar dataKey="risk_rate" fill="var(--destructive)" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </ChartCard>

      <ChartCard title={dict.eda.maxHrVsAge}>
        <ResponsiveContainer width="100%" height={280}>
          <ScatterChart>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
            <XAxis
              dataKey="Age"
              type="number"
              tick={{ fontSize: 11 }}
              stroke="var(--muted-foreground)"
              name="Age"
            />
            <YAxis
              dataKey="MaxHR"
              type="number"
              tick={{ fontSize: 11 }}
              stroke="var(--muted-foreground)"
              name="MaxHR"
            />
            <Tooltip {...TOOLTIP} />
            <Scatter
              data={data.scatter.filter((d) => d.HeartDisease === 0)}
              fill="var(--success)"
              name={dict.common.low}
            />
            <Scatter
              data={data.scatter.filter((d) => d.HeartDisease === 1)}
              fill="var(--destructive)"
              name={dict.common.high}
            />
            <Legend wrapperStyle={{ fontSize: 12 }} />
          </ScatterChart>
        </ResponsiveContainer>
      </ChartCard>
    </div>
  );
}

function ChartCard({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <Card>
      <CardContent className="p-6">
        <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-muted-foreground">
          {title}
        </h2>
        {children}
      </CardContent>
    </Card>
  );
}

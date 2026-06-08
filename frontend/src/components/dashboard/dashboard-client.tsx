"use client";

import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import {
  Activity,
  AlertTriangle,
  CalendarDays,
  HeartPulse,
  TrendingUp,
} from "lucide-react";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from "recharts";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";
import { useT } from "@/i18n/context";

export function DashboardClient() {
  const { dict, locale } = useT();
  const stats = useQuery({ queryKey: ["stats"], queryFn: api.stats });
  const history = useQuery({ queryKey: ["history"], queryFn: api.history });

  const s = stats.data ?? {
    total: 0,
    high_risk: 0,
    low_risk: 0,
    high_risk_pct: 0,
    today: 0,
  };

  const recent = (history.data ?? []).slice(-8).reverse();

  const pieData = [
    { name: dict.dashboard.kpi.lowRisk, value: s.low_risk, color: "var(--success)" },
    { name: dict.dashboard.kpi.highRisk, value: s.high_risk, color: "var(--destructive)" },
  ];

  return (
    <div className="grid gap-6">
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <KpiCard
          icon={<Activity className="h-4 w-4" />}
          label={dict.dashboard.kpi.totalAssessments}
          value={s.total.toString()}
        />
        <KpiCard
          icon={<CalendarDays className="h-4 w-4" />}
          label={dict.dashboard.kpi.todayAssessments}
          value={s.today.toString()}
        />
        <KpiCard
          icon={<AlertTriangle className="h-4 w-4" />}
          label={dict.dashboard.kpi.highRiskPct}
          value={`${s.high_risk_pct}%`}
          tone={s.high_risk_pct >= 40 ? "danger" : "default"}
        />
        <KpiCard
          icon={<TrendingUp className="h-4 w-4" />}
          label={dict.dashboard.kpi.highRisk}
          value={s.high_risk.toString()}
          tone="danger"
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardContent className="p-6">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-sm font-semibold uppercase tracking-wide text-muted-foreground">
                {dict.dashboard.recentTitle}
              </h2>
              <Button asChild size="sm">
                <Link href={`/${locale}/new-evaluation`}>
                  <HeartPulse className="h-4 w-4" />
                  {dict.dashboard.quickAction}
                </Link>
              </Button>
            </div>
            {recent.length === 0 ? (
              <div className="rounded-md border border-dashed border-border py-10 text-center text-sm text-muted-foreground">
                {dict.dashboard.recentEmpty}
              </div>
            ) : (
              <div className="overflow-hidden rounded-md border border-border">
                <table className="w-full text-sm">
                  <thead className="bg-muted/40 text-xs uppercase tracking-wide text-muted-foreground">
                    <tr>
                      <th className="px-3 py-2 text-left">{dict.history.columns.patientId}</th>
                      <th className="px-3 py-2 text-left">{dict.history.columns.date}</th>
                      <th className="px-3 py-2 text-left">{dict.history.columns.age}</th>
                      <th className="px-3 py-2 text-left">{dict.history.columns.sex}</th>
                      <th className="px-3 py-2 text-right">{dict.history.columns.probability}</th>
                      <th className="px-3 py-2 text-right">{dict.history.columns.risk}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {recent.map((r, i) => (
                      <tr
                        key={`${r.patient_id}-${i}`}
                        className="border-t border-border"
                      >
                        <td className="px-3 py-2 font-mono text-xs">{r.patient_id}</td>
                        <td className="px-3 py-2">{r.date} · {r.time}</td>
                        <td className="px-3 py-2">{r.age}</td>
                        <td className="px-3 py-2">{r.sex}</td>
                        <td className="px-3 py-2 text-right font-semibold">
                          {r.probability.toFixed(1)}%
                        </td>
                        <td className="px-3 py-2 text-right">
                          <Badge variant={r.risk === "ALTO" ? "destructive" : "success"}>
                            {r.risk === "ALTO"
                              ? dict.common.high
                              : dict.common.low}
                          </Badge>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-muted-foreground">
              {dict.dashboard.riskDistribution}
            </h2>
            <div className="h-64">
              {s.total === 0 ? (
                <div className="flex h-full items-center justify-center text-sm text-muted-foreground">
                  {dict.common.noData}
                </div>
              ) : (
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={pieData}
                      dataKey="value"
                      nameKey="name"
                      innerRadius={50}
                      outerRadius={80}
                      paddingAngle={2}
                    >
                      {pieData.map((d, i) => (
                        <Cell key={i} fill={d.color} />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{
                        background: "var(--popover)",
                        border: "1px solid var(--border)",
                        borderRadius: 8,
                        fontSize: 12,
                      }}
                    />
                    <Legend wrapperStyle={{ fontSize: 12 }} />
                  </PieChart>
                </ResponsiveContainer>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function KpiCard({
  icon,
  label,
  value,
  tone = "default",
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  tone?: "default" | "danger";
}) {
  return (
    <Card>
      <CardContent className="flex items-center justify-between gap-4 p-5">
        <div>
          <div className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
            {label}
          </div>
          <div
            className={`mt-1 text-3xl font-bold ${
              tone === "danger" ? "text-destructive" : "text-foreground"
            }`}
          >
            {value}
          </div>
        </div>
        <div
          className={`flex h-11 w-11 items-center justify-center rounded-lg ${
            tone === "danger"
              ? "bg-destructive/10 text-destructive"
              : "bg-primary/10 text-primary"
          }`}
        >
          {icon}
        </div>
      </CardContent>
    </Card>
  );
}

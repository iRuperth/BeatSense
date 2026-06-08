import { notFound } from "next/navigation";
import { isLocale } from "@/i18n/config";
import { getDictionary } from "@/i18n/dictionaries";
import { PageHeader } from "@/components/layout/page-header";
import { EdaCharts } from "@/components/charts/eda-charts";

export default async function Page({
  params,
}: {
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  if (!isLocale(lang)) notFound();
  const dict = await getDictionary(lang);
  return (
    <div className="space-y-6">
      <PageHeader title={dict.eda.title} subtitle={dict.eda.subtitle} />
      <EdaCharts />
    </div>
  );
}

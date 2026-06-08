import { EvaluationForm } from "@/components/forms/evaluation-form";
import { PageHeader } from "@/components/layout/page-header";
import { getDictionary } from "@/i18n/dictionaries";
import { isLocale } from "@/i18n/config";
import { notFound } from "next/navigation";

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
      <PageHeader title={dict.form.title} subtitle={dict.form.subtitle} />
      <EvaluationForm />
    </div>
  );
}

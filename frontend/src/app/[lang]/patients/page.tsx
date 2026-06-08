import { notFound } from "next/navigation";
import { isLocale } from "@/i18n/config";
import { getDictionary } from "@/i18n/dictionaries";
import { PageHeader } from "@/components/layout/page-header";
import { PatientsTable } from "@/components/patients/patients-table";

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
      <PageHeader title={dict.history.title} subtitle={dict.history.subtitle} />
      <PatientsTable />
    </div>
  );
}

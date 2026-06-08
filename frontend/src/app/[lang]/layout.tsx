import { notFound } from "next/navigation";
import { isLocale, locales } from "@/i18n/config";
import { getDictionary } from "@/i18n/dictionaries";
import { Providers } from "@/components/providers";
import { Sidebar } from "@/components/layout/sidebar";
import { Header } from "@/components/layout/header";

export async function generateStaticParams() {
  return locales.map((lang) => ({ lang }));
}

export default async function LangLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ lang: string }>;
}) {
  const { lang } = await params;
  if (!isLocale(lang)) notFound();
  const dict = await getDictionary(lang);

  return (
    <Providers dict={dict} locale={lang}>
      <div className="flex min-h-screen bg-background text-foreground">
        <Sidebar />
        <div className="flex flex-1 flex-col">
          <Header />
          <main className="flex-1 overflow-x-hidden p-6 lg:p-8">{children}</main>
        </div>
      </div>
    </Providers>
  );
}

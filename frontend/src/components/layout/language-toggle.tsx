"use client";

import { Languages } from "lucide-react";
import { usePathname, useRouter } from "next/navigation";
import { locales, type Locale } from "@/i18n/config";
import { useT } from "@/i18n/context";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export function LanguageToggle() {
  const { locale } = useT();
  const router = useRouter();
  const pathname = usePathname();

  function handleChange(next: string) {
    document.cookie = `locale=${next}; path=/; max-age=31536000`;
    const segments = pathname.split("/");
    segments[1] = next;
    router.push(segments.join("/") || `/${next}`);
    router.refresh();
  }

  return (
    <Select value={locale} onValueChange={handleChange}>
      <SelectTrigger className="h-9 w-[110px] gap-2">
        <Languages className="h-4 w-4 opacity-70" />
        <SelectValue />
      </SelectTrigger>
      <SelectContent>
        {(locales as readonly Locale[]).map((l) => (
          <SelectItem key={l} value={l}>
            {l === "en" ? "English" : "Español"}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}

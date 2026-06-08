"use client";

import { useTheme } from "next-themes";
import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { useT } from "@/i18n/context";
import { LanguageToggle } from "@/components/layout/language-toggle";
import { Sun, Moon, Monitor } from "lucide-react";

export function SettingsPanel() {
  const { dict } = useT();
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  const options = [
    { v: "light", label: dict.settings.themeLight, icon: Sun },
    { v: "dark", label: dict.settings.themeDark, icon: Moon },
    { v: "system", label: dict.settings.themeSystem, icon: Monitor },
  ];

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <Card>
        <CardContent className="space-y-3 p-6">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-muted-foreground">
            {dict.settings.language}
          </h2>
          <LanguageToggle />
        </CardContent>
      </Card>

      <Card>
        <CardContent className="space-y-3 p-6">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-muted-foreground">
            {dict.settings.theme}
          </h2>
          <div className="grid grid-cols-3 gap-2">
            {options.map(({ v, label, icon: Icon }) => {
              const active = mounted && theme === v;
              return (
                <button
                  key={v}
                  onClick={() => setTheme(v)}
                  className={`flex flex-col items-center gap-2 rounded-md border p-3 text-sm transition-colors ${
                    active
                      ? "border-primary bg-primary/10 text-primary"
                      : "border-border bg-card text-muted-foreground hover:text-foreground"
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  {label}
                </button>
              );
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

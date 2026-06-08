"use client";

import { Search, Activity } from "lucide-react";
import { useT } from "@/i18n/context";
import { ThemeToggle } from "./theme-toggle";
import { LanguageToggle } from "./language-toggle";

export function Header() {
  const { dict } = useT();
  const now = new Date();
  const date = now.toLocaleDateString(undefined, {
    weekday: "long",
    day: "2-digit",
    month: "short",
    year: "numeric",
  });

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center justify-between gap-4 border-b border-border bg-card/80 px-6 backdrop-blur lg:px-8">
      <div className="flex items-center gap-3">
        <div className="relative hidden md:block">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <input
            type="search"
            placeholder={dict.header.search}
            className="h-9 w-72 rounded-md border border-input bg-background pl-9 pr-3 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </div>
      </div>

      <div className="flex items-center gap-3">
        <div className="hidden items-center gap-2 rounded-md border border-border bg-background px-3 py-1.5 text-xs text-muted-foreground md:flex">
          <Activity className="h-3.5 w-3.5 text-success" />
          <span className="font-medium">{dict.header.shift}</span>
          <span className="text-muted-foreground/60">·</span>
          <span>{date}</span>
        </div>
        <LanguageToggle />
        <ThemeToggle />
        <div className="flex items-center gap-2 border-l border-border pl-3">
          <div className="hidden text-right text-xs leading-tight md:block">
            <div className="font-semibold">{dict.header.user}</div>
            <div className="text-muted-foreground">{dict.header.role}</div>
          </div>
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-primary text-sm font-bold text-primary-foreground">
            NP
          </div>
        </div>
      </div>
    </header>
  );
}

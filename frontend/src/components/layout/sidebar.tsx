"use client";

import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  HeartPulse,
  Users,
  BarChart3,
  Brain,
  Settings,
} from "lucide-react";
import { useT } from "@/i18n/context";
import { cn } from "@/lib/utils";

export function Sidebar() {
  const { dict, locale } = useT();
  const pathname = usePathname();

  const items = [
    { href: "", label: dict.nav.dashboard, icon: LayoutDashboard },
    { href: "new-evaluation", label: dict.nav.newEvaluation, icon: HeartPulse },
    { href: "patients", label: dict.nav.patients, icon: Users },
    { href: "eda", label: dict.nav.eda, icon: BarChart3 },
    { href: "model", label: dict.nav.model, icon: Brain },
    { href: "settings", label: dict.nav.settings, icon: Settings },
  ];

  return (
    <aside className="sticky top-0 hidden h-screen w-64 flex-col border-r border-sidebar-border bg-sidebar text-sidebar-foreground lg:flex">
      <div className="flex items-center gap-3 border-b border-sidebar-border px-5 py-5">
        <div className="flex h-11 w-11 items-center justify-center overflow-hidden rounded-lg bg-white/5 ring-1 ring-white/10">
          <Image
            src="/logu1.png"
            alt="BeatSense"
            width={40}
            height={40}
            className="h-9 w-9 object-contain"
            priority
          />
        </div>
        <div className="leading-tight">
          <div className="text-sm font-bold tracking-wide text-white">
            {dict.app.name}
          </div>
          <div className="text-[10px] uppercase tracking-widest text-sidebar-foreground/60">
            {dict.app.tagline}
          </div>
        </div>
      </div>

      <nav className="flex-1 space-y-1 px-3 py-4">
        {items.map(({ href, label, icon: Icon }) => {
          const full = `/${locale}${href ? `/${href}` : ""}`;
          const active =
            href === ""
              ? pathname === `/${locale}` || pathname === `/${locale}/`
              : pathname.startsWith(full);
          return (
            <Link
              key={href}
              href={full}
              className={cn(
                "group flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium transition-colors",
                active
                  ? "bg-sidebar-accent text-white"
                  : "text-sidebar-foreground/80 hover:bg-sidebar-accent/60 hover:text-white"
              )}
            >
              <Icon className="h-4 w-4" />
              {label}
            </Link>
          );
        })}
      </nav>

      <div className="border-t border-sidebar-border px-5 py-4 text-[11px] leading-relaxed text-sidebar-foreground/60">
        <div className="font-mono">{dict.app.institution}</div>
        <div className="mt-1">v1.0 · {new Date().getFullYear()}</div>
      </div>
    </aside>
  );
}

"use client";

import { createContext, useContext, type ReactNode } from "react";
import type { Dictionary } from "./dictionaries";
import type { Locale } from "./config";

type Ctx = { dict: Dictionary; locale: Locale };

const I18nContext = createContext<Ctx | null>(null);

export function I18nProvider({
  dict,
  locale,
  children,
}: {
  dict: Dictionary;
  locale: Locale;
  children: ReactNode;
}) {
  return (
    <I18nContext.Provider value={{ dict, locale }}>
      {children}
    </I18nContext.Provider>
  );
}

export function useT() {
  const ctx = useContext(I18nContext);
  if (!ctx) throw new Error("useT must be used inside I18nProvider");
  return ctx;
}

import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import { ThemeRoot } from "@/components/providers";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const mono = JetBrains_Mono({
  variable: "--font-jetbrains-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "BeatSense — Cardiovascular Risk Intelligence",
  description:
    "Clinical workstation for cardiovascular risk assessment powered by ML.",
  icons: { icon: "/logu1.png" },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html suppressHydrationWarning>
      <body
        className={`${inter.variable} ${mono.variable} min-h-screen antialiased`}
      >
        <ThemeRoot>{children}</ThemeRoot>
      </body>
    </html>
  );
}

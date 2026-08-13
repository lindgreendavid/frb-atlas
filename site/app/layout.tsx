import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "FRB Atlas — reanalyzing CHIME/FRB Catalog 1",
  description:
    "An accessible reanalysis of CHIME/FRB Catalog 1 comparing repeating and non-repeating fast radio bursts by dispersion measure, pulse width, and spectral bandwidth, with a frozen, reproducible result registry.",
  applicationName: "FRB Atlas",
  keywords: [
    "fast radio bursts",
    "CHIME/FRB",
    "dispersion measure",
    "repeating FRB",
    "radio astronomy",
    "astrostatistics",
    "reproducible research",
    "web accessibility",
  ],
  openGraph: {
    title: "FRB Atlas",
    description:
      "Do repeating and non-repeating fast radio bursts differ in dispersion measure, pulse width, and spectral bandwidth? A reproducible reanalysis of CHIME/FRB Catalog 1.",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "FRB Atlas",
    description:
      "A reproducible reanalysis of CHIME/FRB Catalog 1's repeater vs. non-repeater burst statistics.",
  },
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>{children}</body>
    </html>
  );
}

import type { Metadata } from "next";
import { Quicksand } from "next/font/google";
import "./globals.css";
import { ClientLayout } from "@/components/client-layout";

const quicksand = Quicksand({
  variable: "--font-sans",
  subsets: ["latin"],
  display: 'swap',
});

export const metadata: Metadata = {
  title: "PhishGuard — Instantly check links. Recover accounts. Stay safe.",
  description: "AI-powered scam detection and step-by-step recovery guidance for Myanmar. Simple English. Free & anonymous.",
  keywords: ["phishing", "scam detection", "cybersecurity", "Myanmar", "AI", "security"],
  authors: [{ name: "Team Vaultaris", url: "https://phishguard.com" }],
  creator: "Team Vaultaris - University of Information Technology",
  openGraph: {
    title: "PhishGuard — AI-Powered Scam Detection",
    description: "Protect yourself from online scams with our AI-powered link scanner and recovery guidance.",
    url: "https://phishguard.com",
    siteName: "PhishGuard",
    type: "website",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "PhishGuard — AI-Powered Scam Detection",
    description: "Protect yourself from online scams with our AI-powered link scanner and recovery guidance.",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  verification: {
    // Add verification codes when deploying
    // google: "verification_code",
    // yandex: "verification_code",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              try {
                if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                  document.documentElement.classList.add('dark')
                  document.body.classList.add('dark')
                } else {
                  document.documentElement.classList.remove('dark')
                  document.body.classList.remove('dark')
                }
              } catch (_) {}
            `,
          }}
        />
      </head>
      <body
        className={`${quicksand.variable} font-sans antialiased cursor-none`}
        suppressHydrationWarning
      >
        <ClientLayout>
          {children}
        </ClientLayout>
      </body>
    </html>
  );
}

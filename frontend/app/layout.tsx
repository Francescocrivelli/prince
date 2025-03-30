import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/theme-provider";
import { AuthProvider } from "@/contexts/AuthContext";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Find My Bun - Exclusive AI Pet Tracking Service",
  description: "Find My Bun helps you track and manage information about your pet bunnies. An exclusive service for pet owners.",
  keywords: ["pet tracking", "bunny tracking", "rabbit tracking", "pet management", "exclusive service"],
  authors: [{ name: "Find My Bun Team" }],
  creator: "Find My Bun Team",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <AuthProvider>
          <ThemeProvider
            attribute="class"
            defaultTheme="light"
            enableSystem
            disableTransitionOnChange
          >
            {children}
          </ThemeProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
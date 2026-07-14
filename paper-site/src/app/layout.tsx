import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Are the Stonehenge carvings mushrooms? — Shape analysis",
  description:
    "A computational shape analysis of the 115 prehistoric carvings on Stonehenge suggests they may depict Amanita muscaria mushrooms rather than Bronze Age axeheads.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}

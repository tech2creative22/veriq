import type { Metadata } from "next";
import "./globals.css";
import "./refinement.css";
import "./brand-refresh.css";

export const metadata: Metadata = {
  title: "Veriq | School Pulse",
  description: "Educational Decision Intelligence",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}

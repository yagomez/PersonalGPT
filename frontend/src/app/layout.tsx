import type { Metadata } from "next"
import "./globals.css"

export const metadata: Metadata = {
  title: "PersonalGPT - Your AI Assistant",
  description: "A personalized AI assistant with full-stack integration",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

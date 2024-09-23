import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Ranobe Reader',
  description: 'A simple ranobe reader application'
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

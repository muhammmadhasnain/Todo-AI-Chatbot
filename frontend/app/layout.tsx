import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import  AuthProvider  from  "./../components/auth/AuthProvider";
import Navigation from "./../components/Navigation";
import { Toaster } from 'react-hot-toast';
import GlobalChatProvider from './../components/GlobalChatProvider';

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Todo AI",
  description: "AI-powered task management application",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <AuthProvider>
          <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
            <Navigation />
            <main>
              {children}
            </main>
            <Toaster position="top-right" />
            <GlobalChatProvider />
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}
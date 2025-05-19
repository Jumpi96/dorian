"use client"

import type React from "react"
import Link from "next/link"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Shirt, LuggageIcon as Suitcase, ShoppingBag, History, User } from "lucide-react"
import { Button } from "@/components/ui/button"
import { useAuth } from "@/lib/auth"
import { useRouter, usePathname } from "next/navigation"

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const { logout } = useAuth()
  const router = useRouter()
  const pathname = usePathname()

  const handleLogout = async () => {
    await logout()
    router.push("/")
  }

  const getActiveTab = () => {
    if (pathname === "/dashboard") return "wear"
    if (pathname === "/dashboard/pack") return "pack"
    if (pathname === "/dashboard/buy") return "buy"
    if (pathname === "/dashboard/history") return "history"
    return "wear"
  }

  return (
    <div className="flex flex-col min-h-screen">
      <header className="border-b">
        <div className="container flex justify-between items-center py-4">
          <Link href="/dashboard" className="text-2xl font-bold">
            Dorian
          </Link>
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="icon">
              <User className="h-5 w-5" />
            </Button>
            <Button variant="outline" onClick={handleLogout}>
              Logout
            </Button>
          </div>
        </div>
      </header>

      <div className="container py-4">
        <Tabs value={getActiveTab()} className="w-full">
          <TabsList className="grid grid-cols-4 w-full max-w-md mx-auto">
            <TabsTrigger value="wear" asChild>
              <Link href="/dashboard" className="flex items-center gap-2">
                <Shirt className="h-4 w-4" />
                <span className="hidden sm:inline">Wear</span>
              </Link>
            </TabsTrigger>
            <TabsTrigger value="pack" asChild>
              <Link href="/dashboard/pack" className="flex items-center gap-2">
                <Suitcase className="h-4 w-4" />
                <span className="hidden sm:inline">Pack</span>
              </Link>
            </TabsTrigger>
            <TabsTrigger value="buy" asChild>
              <Link href="/dashboard/buy" className="flex items-center gap-2">
                <ShoppingBag className="h-4 w-4" />
                <span className="hidden sm:inline">Buy</span>
              </Link>
            </TabsTrigger>
            <TabsTrigger value="history" asChild>
              <Link href="/dashboard/history" className="flex items-center gap-2">
                <History className="h-4 w-4" />
                <span className="hidden sm:inline">History</span>
              </Link>
            </TabsTrigger>
          </TabsList>
        </Tabs>
      </div>

      <main className="flex-1 container py-6">{children}</main>

      <footer className="border-t py-4">
        <div className="container text-center text-gray-500 text-sm">
          <p>© {new Date().getFullYear()} Dorian. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}

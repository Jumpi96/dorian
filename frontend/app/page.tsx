'use client';

import { Button } from "@/components/ui/button"
import Link from "next/link"
import { ArrowRight, Shirt, LuggageIcon as Suitcase, ShoppingBag } from "lucide-react"
import { GoogleSignInButton } from "@/components/google-signin-button"
import { useAuth } from "@/lib/auth"

export default function Home() {
  const { isAuthenticated, logout } = useAuth();

  return (
    <div className="flex flex-col min-h-screen">
      <header className="border-b">
        <div className="container flex justify-between items-center py-4">
          <h1 className="text-2xl font-bold">Dorian</h1>
          <div className="flex gap-4">
            {isAuthenticated ? (
              <>
                <Link href="/dashboard">
                  <Button>Go to Dashboard</Button>
                </Link>
                <Button variant="outline" onClick={logout}>
                  Logout
                </Button>
              </>
            ) : (
              <GoogleSignInButton />
            )}
          </div>
        </div>
      </header>

      <main className="flex-1">
        <section className="py-20">
          <div className="container text-center">
            <h2 className="text-4xl font-bold mb-6">Your Personal Wardrobe Assistant</h2>
            <p className="text-xl mb-10 text-gray-600">
              Manage your clothing collection and get personalized outfit recommendations for any occasion.
            </p>
            {isAuthenticated ? (
              <Link href="/dashboard">
                <Button size="lg" className="mb-10">
                  Go to Dashboard <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </Link>
            ) : (
              <GoogleSignInButton />
            )}

            <div className="grid md:grid-cols-3 gap-8 mt-16">
              <div className="p-6 border rounded-lg">
                <div className="bg-gray-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Shirt className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Wear</h3>
                <p className="text-gray-600">Get outfit suggestions for any occasion based on your wardrobe.</p>
              </div>

              <div className="p-6 border rounded-lg">
                <div className="bg-gray-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Suitcase className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Pack</h3>
                <p className="text-gray-600">Create packing lists for your trips with items from your wardrobe.</p>
              </div>

              <div className="p-6 border rounded-lg">
                <div className="bg-gray-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4">
                  <ShoppingBag className="h-6 w-6" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Buy</h3>
                <p className="text-gray-600">Get recommendations on what to buy next to complement your wardrobe.</p>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t py-6">
        <div className="container text-center text-gray-500">
          <p>© {new Date().getFullYear()} Dorian. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}

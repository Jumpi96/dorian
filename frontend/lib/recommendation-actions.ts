"use server"

import { revalidatePath } from "next/cache"
import { cookies } from "next/headers"

type RecommendationMode = "wear" | "pack" | "buy"

// In a real app, this would interact with a database and LLM API
export async function getRecommendation(mode: RecommendationMode, prompt: string, tripId?: string) {
  const cookieStore = await cookies()
  const token = cookieStore.get('auth_token')?.value

  if (!token) {
    throw new Error('Not authenticated')
  }

  const url = new URL(`http://localhost:3001/recommend/${mode}`)
  if (tripId) {
    url.searchParams.append('tripId', tripId)
  }

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ situation: prompt })
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.message || 'Failed to get recommendation')
  }

  const data = await response.json()
  revalidatePath(`/dashboard/${mode === "wear" ? "" : mode}`)
  return data
}

// Helper function to get wardrobe items
async function getWardrobeItems() {
  const cookieStore = await cookies()
  const token = cookieStore.get('auth_token')?.value

  if (!token) {
    throw new Error('Not authenticated')
  }

  const response = await fetch('http://localhost:3001/wardrobe', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })

  if (!response.ok) {
    throw new Error('Failed to fetch wardrobe items')
  }

  return response.json()
}

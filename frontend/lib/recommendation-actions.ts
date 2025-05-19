"use server"

import { revalidatePath } from "next/cache"
import { cookies } from "next/headers"

type RecommendationMode = "wear" | "pack" | "buy"

class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public type?: string
  ) {
    super(message)
    this.name = 'APIError'
  }
}

// In a real app, this would interact with a database and LLM API
export async function getRecommendation(mode: RecommendationMode, prompt: string, tripId?: string) {
  const cookieStore = await cookies()
  const token = cookieStore.get('auth_token')?.value

  if (!token) {
    throw new Error('Not authenticated')
  }

  const url = new URL(`${process.env.NEXT_PUBLIC_API_URL}/recommend/${mode}${tripId ? `/trip/${tripId}` : ''}`)

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
    throw new APIError(
      error.message || 'Failed to get recommendation',
      response.status,
      error.type
    )
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

  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/wardrobe`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })

  if (!response.ok) {
    const error = await response.json()
    throw new APIError(
      error.message || 'Failed to fetch wardrobe items',
      response.status,
      error.type
    )
  }

  return response.json()
}

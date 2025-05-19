"use server"

import { revalidatePath } from "next/cache"
import { cookies } from "next/headers"

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

// In a real app, this would interact with a database
export async function addWardrobeItem(description: string): Promise<string> {
  const cookieStore = await cookies()
  const token = cookieStore.get('auth_token')?.value

  if (!token) {
    throw new Error('Not authenticated')
  }

  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/wardrobe`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ description })
  })

  if (!response.ok) {
    const error = await response.json()
    throw new APIError(
      error.message || 'Failed to add wardrobe item',
      response.status,
      error.type
    )
  }

  const data = await response.json()
  revalidatePath('/dashboard')
  return data.itemId
}

export async function deleteWardrobeItem(itemId: string): Promise<void> {
  const cookieStore = await cookies()
  const token = cookieStore.get('auth_token')?.value

  if (!token) {
    throw new Error('Not authenticated')
  }

  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/wardrobe/${itemId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })

  if (!response.ok) {
    const error = await response.json()
    throw new APIError(
      error.message || 'Failed to delete wardrobe item',
      response.status,
      error.type
    )
  }

  revalidatePath('/dashboard')
}

export async function getWardrobeItems() {
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

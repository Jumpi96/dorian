"use server"

import { cookies } from "next/headers"
import { revalidatePath } from "next/cache"

export async function getCurrentTrip() {
  const cookieStore = await cookies()
  const token = cookieStore.get('auth_token')?.value

  if (!token) {
    throw new Error('Not authenticated')
  }

  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/trips`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })

  if (response.status === 404) {
    return null
  }

  if (!response.ok) {
    let errorMessage = 'Failed to get current trip'
    try {
      const error = await response.json()
      errorMessage = error.message || errorMessage
    } catch {
      // If response is not JSON, use the status text
      errorMessage = response.statusText || errorMessage
    }
    throw new Error(errorMessage)
  }

  try {
    return await response.json()
  } catch (error) {
    throw new Error('Invalid response from server')
  }
}

export async function deleteTrip(tripId: string) {
  const cookieStore = await cookies()
  const token = cookieStore.get('auth_token')?.value

  if (!token) {
    throw new Error('Not authenticated')
  }

  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/trips/${tripId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })

  if (!response.ok) {
    let errorMessage = 'Failed to delete trip'
    try {
      const error = await response.json()
      errorMessage = error.message || errorMessage
    } catch {
      errorMessage = response.statusText || errorMessage
    }
    throw new Error(errorMessage)
  }

  revalidatePath('/dashboard/pack')
} 
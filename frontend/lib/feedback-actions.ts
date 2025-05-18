"use server"

import { cookies } from "next/headers"
import { revalidatePath } from "next/cache"

// In a real app, this would interact with a database
export async function submitFeedback(interactionId: string, feedback: "thumbsUp" | "thumbsDown"): Promise<void> {
  const cookieStore = await cookies()
  const token = cookieStore.get('auth_token')?.value

  if (!token) {
    throw new Error('Not authenticated')
  }

  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/interactions/${interactionId}/feedback`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      feedback: feedback === "thumbsUp" ? 1 : 0
    })
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.message || 'Failed to submit feedback')
  }

  revalidatePath("/dashboard/history")
}

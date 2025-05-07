"use server"

import { revalidatePath } from "next/cache"

// In a real app, this would interact with a database
export async function addWardrobeItem(description: string): Promise<string> {
  // For demo purposes, we're not checking authentication
  const userId = "demo-user"

  // Simulate database interaction
  await new Promise((resolve) => setTimeout(resolve, 500))

  // Generate a random ID for the new item
  const id = Math.random().toString(36).substring(2, 9)

  revalidatePath("/dashboard")
  return id
}

export async function deleteWardrobeItem(itemId: string): Promise<void> {
  // For demo purposes, we're not checking authentication
  const userId = "demo-user"

  // Simulate database interaction
  await new Promise((resolve) => setTimeout(resolve, 500))

  revalidatePath("/dashboard")
}

export async function getWardrobeItems() {
  // For demo purposes, we're not checking authentication
  const userId = "demo-user"

  // Simulate database interaction
  await new Promise((resolve) => setTimeout(resolve, 500))

  // Return mock data
  return [
    { id: "1", description: "Black t-shirt" },
    { id: "2", description: "Blue jeans" },
    { id: "3", description: "White sneakers" },
    { id: "4", description: "Gray hoodie" },
  ]
}

"use server"

import { revalidatePath } from "next/cache"

type RecommendationMode = "wear" | "pack" | "buy"

// In a real app, this would interact with a database and LLM API
export async function getRecommendation(mode: RecommendationMode, prompt: string) {
  // For demo purposes, we're not checking authentication
  const userId = "demo-user"

  // Check rate limit (in a real app, this would query a database)
  const userRequestCount = 5 // Mock value
  const maxRequestsPerDay = 10

  if (userRequestCount >= maxRequestsPerDay) {
    throw new Error("Rate limit exceeded. Try again tomorrow.")
  }

  // Get user's wardrobe items
  const wardrobeItems = await getWardrobeItems()

  if (wardrobeItems.length < 3) {
    throw new Error("Add a few more items to get better recommendations.")
  }

  try {
    // In a real implementation, this would use the AI SDK to generate recommendations
    // based on the user's wardrobe and prompt
    const systemPrompt = getSystemPrompt(mode, wardrobeItems)

    // This is a simplified example - in a real app, you would call an LLM API
    // For demo purposes, we'll just simulate a delay
    await new Promise((resolve) => setTimeout(resolve, 1000))

    // Store the interaction in the database
    const interactionId = Math.random().toString(36).substring(2, 9)

    // Update rate limit counter

    revalidatePath(`/dashboard/${mode === "wear" ? "" : mode}`)
    return interactionId
  } catch (error) {
    console.error("Error generating recommendation:", error)
    throw new Error("Failed to generate recommendation. Please try again later.")
  }
}

// Helper function to get wardrobe items (mock implementation)
async function getWardrobeItems() {
  // In a real app, this would query a database
  return ["Black t-shirt", "Blue jeans", "White sneakers", "Gray hoodie"]
}

// Helper function to create system prompt based on mode and wardrobe
function getSystemPrompt(mode: RecommendationMode, wardrobeItems: string[]): string {
  const wardrobeList = wardrobeItems.join(", ")

  switch (mode) {
    case "wear":
      return `You are a helpful wardrobe assistant. The user has the following items in their wardrobe: ${wardrobeList}. 
      Based on their prompt and these items, suggest an outfit. 
      Return your response as a JSON object with the following structure:
      {
        "top": "item name",
        "bottom": "item name",
        "shoes": "item name",
        "outerwear": "item name (optional)",
        "accessories": "item name (optional)"
      }`

    case "pack":
      return `You are a helpful wardrobe assistant. The user has the following items in their wardrobe: ${wardrobeList}. 
      Based on their prompt and these items, suggest a packing list. 
      Return your response as a JSON object with the following structure:
      {
        "tops": ["item1", "item2", ...],
        "bottoms": ["item1", "item2", ...],
        "shoes": ["item1", "item2", ...],
        "outerwear": ["item1", "item2", ...],
        "accessories": ["item1", "item2", ...],
        "essentials": ["item1", "item2", ...]
      }`

    case "buy":
      return `You are a helpful wardrobe assistant. The user has the following items in their wardrobe: ${wardrobeList}. 
      Based on their prompt and these items, suggest one item they should buy next to complement their wardrobe. 
      Return your response as a JSON object with the following structure:
      {
        "item": "suggested item to buy",
        "reason": "explanation of why this item would complement their wardrobe"
      }`

    default:
      return ""
  }
}

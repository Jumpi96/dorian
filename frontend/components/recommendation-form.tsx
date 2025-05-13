"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { useToast } from "@/hooks/use-toast"
import { getRecommendation } from "@/lib/recommendation-actions"

type RecommendationMode = "wear" | "pack" | "buy"

interface RecommendationFormProps {
  mode: RecommendationMode;
  onSituationChange?: (situation: string) => void;
}

export function RecommendationForm({ mode, onSituationChange }: RecommendationFormProps) {
  const [prompt, setPrompt] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const { toast } = useToast()

  const placeholderText = {
    wear: "What should I wear for a casual dinner tonight?",
    pack: "What should I pack for a weekend trip to the beach?",
    buy: "What should I buy to complement my current wardrobe?",
  }

  const buttonText = {
    wear: "Find My Outfit",
    pack: "Create Packing List",
    buy: "Get Purchase Advice"
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!prompt.trim()) return

    setIsLoading(true)
    try {
      await getRecommendation(mode, prompt)
      onSituationChange?.(prompt.trim())
      toast({
        title: "Recommendation generated",
        description: "Your recommendation has been generated.",
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to generate recommendation. Try again later.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <Textarea
        placeholder={placeholderText[mode]}
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        className="mb-4 h-24"
      />
      <Button type="submit" disabled={isLoading || !prompt.trim()}>
        {isLoading ? "Generating..." : buttonText[mode]}
      </Button>
    </form>
  )
}

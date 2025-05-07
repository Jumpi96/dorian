"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ThumbsUp, ThumbsDown } from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import { submitFeedback } from "@/lib/feedback-actions"

export function OutfitDisplay() {
  const [outfit, setOutfit] = useState({
    top: "Black t-shirt",
    bottom: "Olive chinos",
    shoes: "White sneakers",
    outerwear: "Grey hoodie",
    accessories: "Black cap",
  })
  const [interactionId, setInteractionId] = useState("sample-id")
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false)
  const { toast } = useToast()

  const handleFeedback = async (type: "thumbsUp" | "thumbsDown") => {
    try {
      await submitFeedback(interactionId, type)
      setFeedbackSubmitted(true)
      toast({
        title: "Feedback submitted",
        description: "Thank you for your feedback!",
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to submit feedback.",
        variant: "destructive",
      })
    }
  }

  // If no outfit has been generated yet
  if (!outfit) {
    return (
      <Card>
        <CardContent className="p-6 text-center text-gray-500">
          Enter a prompt above to get an outfit recommendation.
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Your Outfit Recommendation</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-2 mb-6">
          {Object.entries(outfit).map(([category, item]) => (
            <div key={category} className="flex justify-between">
              <span className="capitalize font-medium">{category}:</span>
              <span>{item}</span>
            </div>
          ))}
        </div>

        <div className="flex justify-center gap-4">
          <Button variant="outline" size="sm" onClick={() => handleFeedback("thumbsUp")} disabled={feedbackSubmitted}>
            <ThumbsUp className="h-4 w-4 mr-2" />
            Like
          </Button>
          <Button variant="outline" size="sm" onClick={() => handleFeedback("thumbsDown")} disabled={feedbackSubmitted}>
            <ThumbsDown className="h-4 w-4 mr-2" />
            Dislike
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}

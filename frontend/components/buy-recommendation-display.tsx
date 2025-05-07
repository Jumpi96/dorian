"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ThumbsUp, ThumbsDown } from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import { submitFeedback } from "@/lib/feedback-actions"

export function BuyRecommendationDisplay() {
  const [recommendation, setRecommendation] = useState({
    item: "Navy blue blazer",
    reason:
      "A versatile blazer would complement your existing casual items and allow you to create more formal outfits. Navy is a classic color that pairs well with most of your current wardrobe.",
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

  // If no recommendation has been generated yet
  if (!recommendation) {
    return (
      <Card>
        <CardContent className="p-6 text-center text-gray-500">
          Enter a prompt above to get a purchase recommendation.
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Recommended Purchase</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4 mb-6">
          <div>
            <h3 className="font-medium mb-2">Item:</h3>
            <p>{recommendation.item}</p>
          </div>
          <div>
            <h3 className="font-medium mb-2">Why:</h3>
            <p>{recommendation.reason}</p>
          </div>
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

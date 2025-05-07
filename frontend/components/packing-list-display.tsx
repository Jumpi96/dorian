"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ThumbsUp, ThumbsDown } from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import { submitFeedback } from "@/lib/feedback-actions"

export function PackingListDisplay() {
  const [packingList, setPackingList] = useState({
    tops: ["White t-shirt", "Blue button-up shirt", "Grey sweater"],
    bottoms: ["Blue jeans", "Khaki shorts"],
    shoes: ["White sneakers", "Sandals"],
    outerwear: ["Light jacket"],
    accessories: ["Sunglasses", "Hat"],
    essentials: ["Toiletries", "Chargers"],
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

  // If no packing list has been generated yet
  if (!packingList) {
    return (
      <Card>
        <CardContent className="p-6 text-center text-gray-500">
          Enter a prompt above to get a packing list recommendation.
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Your Packing List</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4 mb-6">
          {Object.entries(packingList).map(([category, items]) => (
            <div key={category}>
              <h3 className="capitalize font-medium mb-2">{category}:</h3>
              <ul className="list-disc pl-5">
                {items.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
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

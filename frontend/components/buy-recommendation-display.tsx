"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ThumbsUp, ThumbsDown } from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import { submitFeedback } from "@/lib/feedback-actions"
import { getRecommendation } from "@/lib/recommendation-actions"

interface BuyRecommendationDisplayProps {
  situation?: string;
}

export function BuyRecommendationDisplay({ situation }: BuyRecommendationDisplayProps) {
  const [recommendation, setRecommendation] = useState<{ item: string; explanation: string } | null>(null)
  const [interactionId, setInteractionId] = useState<string | null>(null)
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const { toast } = useToast()

  useEffect(() => {
    const fetchRecommendation = async () => {
      if (!situation) return;
      
      setIsLoading(true);
      try {
        const data = await getRecommendation("buy", situation);
        setRecommendation(data.item_to_buy);
        setInteractionId(data.interaction_id);
      } catch (error) {
        toast({
          title: "Error",
          description: error instanceof Error ? error.message : "Failed to fetch purchase recommendation",
          variant: "destructive",
        });
      } finally {
        setIsLoading(false);
      }
    };

    fetchRecommendation();
  }, [situation, toast]);

  const handleFeedback = async (type: "thumbsUp" | "thumbsDown") => {
    if (!interactionId) return;
    
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

  // If no situation is provided
  if (!situation) {
    return (
      <Card>
        <CardContent className="p-6 text-center text-gray-500">
          Tell me about your situation and I'll help you find the perfect addition to your wardrobe!
        </CardContent>
      </Card>
    )
  }

  // If loading
  if (isLoading) {
    return (
      <Card>
        <CardContent className="p-6 text-center text-gray-500">
          Loading your purchase recommendation...
        </CardContent>
      </Card>
    )
  }

  // If no recommendation has been generated yet
  if (!recommendation) {
    return (
      <Card>
        <CardContent className="p-6 text-center text-gray-500">
          No purchase recommendation available.
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
            <p>{recommendation.explanation}</p>
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

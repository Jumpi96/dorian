"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ThumbsUp, ThumbsDown } from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import { submitFeedback } from "@/lib/feedback-actions"
import { getRecommendation } from "@/lib/recommendation-actions"

interface OutfitDisplayProps {
  situation?: string;
}

export function OutfitDisplay({ situation }: OutfitDisplayProps) {
  const [outfit, setOutfit] = useState<Record<string, string> | null>(null)
  const [interactionId, setInteractionId] = useState<string | null>(null)
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const { toast } = useToast()

  useEffect(() => {
    const fetchOutfit = async () => {
      if (!situation) return;
      
      setIsLoading(true);
      try {
        const data = await getRecommendation("wear", situation);
        setOutfit(data.outfit);
        setInteractionId(data.interaction_id);
      } catch (error) {
        toast({
          title: "Error",
          description: error instanceof Error ? error.message : "Failed to fetch outfit recommendation",
          variant: "destructive",
        });
      } finally {
        setIsLoading(false);
      }
    };

    fetchOutfit();
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
          Tell me about your occasion and I'll help you pick the perfect outfit!
        </CardContent>
      </Card>
    )
  }

  // If loading
  if (isLoading) {
    return (
      <Card>
        <CardContent className="p-6 text-center text-gray-500">
          Loading your outfit recommendation...
        </CardContent>
      </Card>
    )
  }

  // If no outfit has been generated yet
  if (!outfit) {
    return (
      <Card>
        <CardContent className="p-6 text-center text-gray-500">
          No outfit recommendation available.
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

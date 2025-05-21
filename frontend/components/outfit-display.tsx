"use client"

import { useState, useEffect, useRef } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ThumbsUp, ThumbsDown } from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import { submitFeedback } from "@/lib/feedback-actions"
import { getRecommendation } from "@/lib/recommendation-actions"

interface OutfitDisplayProps {
  situation?: string;
  tripId?: string;
  initialData?: {
    outfit: Record<string, string>;
    interaction_id: string;
  };
}

export function OutfitDisplay({ situation, tripId, initialData }: OutfitDisplayProps) {
  const [outfit, setOutfit] = useState<Record<string, string> | null>(initialData?.outfit || null)
  const [interactionId, setInteractionId] = useState<string | null>(initialData?.interaction_id || null)
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false)
  const [selectedFeedback, setSelectedFeedback] = useState<"thumbsUp" | "thumbsDown" | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isSubmittingFeedback, setIsSubmittingFeedback] = useState(false)
  const { toast } = useToast()
  const requestInProgress = useRef(false)

  useEffect(() => {
    const fetchOutfit = async () => {
      if (!situation || requestInProgress.current || initialData) return;
      
      requestInProgress.current = true;
      setIsLoading(true);
      try {
        const data = await getRecommendation("wear", situation, tripId);
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
        requestInProgress.current = false;
      }
    };

    fetchOutfit();
  }, [situation, tripId, initialData]);

  // Update state when initialData changes
  useEffect(() => {
    if (initialData) {
      setOutfit(initialData.outfit);
      setInteractionId(initialData.interaction_id);
    }
  }, [initialData]);

  const handleFeedback = async (type: "thumbsUp" | "thumbsDown") => {
    if (!interactionId || isSubmittingFeedback) return;
    
    setIsSubmittingFeedback(true);
    try {
      await submitFeedback(interactionId, type)
      setFeedbackSubmitted(true)
      setSelectedFeedback(type)
      toast({
        title: "Feedback submitted",
        description: "Thank you for your feedback!",
      })
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to submit feedback.",
        variant: "destructive",
      })
    } finally {
      setIsSubmittingFeedback(false);
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
          <Button 
            variant={selectedFeedback === "thumbsUp" ? "default" : "outline"}
            size="sm" 
            onClick={() => handleFeedback("thumbsUp")} 
            disabled={feedbackSubmitted || isSubmittingFeedback}
            className={selectedFeedback === "thumbsUp" ? "bg-green-600 hover:bg-green-700" : ""}
          >
            <ThumbsUp className="h-4 w-4 mr-2" />
            Like
          </Button>
          <Button 
            variant={selectedFeedback === "thumbsDown" ? "default" : "outline"}
            size="sm" 
            onClick={() => handleFeedback("thumbsDown")} 
            disabled={feedbackSubmitted || isSubmittingFeedback}
            className={selectedFeedback === "thumbsDown" ? "bg-red-600 hover:bg-red-700" : ""}
          >
            <ThumbsDown className="h-4 w-4 mr-2" />
            Dislike
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}

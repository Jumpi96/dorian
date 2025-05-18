"use client"

import { useEffect, useState } from "react"
import { Interaction } from "@/lib/types"
import { getInteractions } from "@/lib/interaction-actions"
import { format } from "date-fns"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { useToast } from "@/components/ui/use-toast"
import { Badge } from "@/components/ui/badge"
import { ThumbsUp, ThumbsDown } from "lucide-react"

export function HistoryList() {
  const [interactions, setInteractions] = useState<Interaction[]>([])
  const [loading, setLoading] = useState(true)
  const { toast } = useToast()

  useEffect(() => {
    const fetchInteractions = async () => {
      try {
        const data = await getInteractions()
        setInteractions(data)
      } catch (error) {
        toast({
          title: "Error",
          description: "Failed to load history",
          variant: "destructive",
        })
      } finally {
        setLoading(false)
      }
    }

    fetchInteractions()
  }, [toast])

  const getBadgeVariant = (type: string): "default" | "secondary" | "outline" => {
    switch (type) {
      case "outfit_recommendation":
        return "default"
      case "trip":
        return "secondary"
      case "purchase_recommendation":
        return "outline"
      default:
        return "default"
    }
  }

  const getBadgeText = (type: string): string => {
    switch (type) {
      case "outfit_recommendation":
        return "WEAR"
      case "trip":
        return "PACK"
      case "purchase_recommendation":
        return "BUY"
      default:
        return type.toUpperCase()
    }
  }

  if (loading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <Card key={i}>
            <CardHeader>
              <Skeleton className="h-6 w-1/3" data-testid="skeleton" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-4 w-full mb-2" data-testid="skeleton" />
              <Skeleton className="h-4 w-2/3" data-testid="skeleton" />
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  if (interactions.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No history available yet.</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {interactions.map((interaction) => (
        <Card key={interaction.interactionId}>
          <CardHeader className="pb-2">
            <div className="flex justify-between items-start">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <Badge variant={getBadgeVariant(interaction.type)}>
                    {getBadgeText(interaction.type)}
                  </Badge>
                  <span className="text-sm text-gray-500">
                    {format(new Date(interaction.createdAt), "PPP p")}
                  </span>
                  {interaction.feedback !== undefined && (
                    <div className="ml-2">
                      {interaction.feedback === "1" ? (
                        <ThumbsUp className="h-4 w-4 text-green-600" />
                      ) : interaction.feedback === "0" ? (
                        <ThumbsDown className="h-4 w-4 text-red-600" />
                      ) : null}
                    </div>
                  )}
                </div>
                <CardTitle className="text-lg">
                  {interaction.type === "outfit_recommendation" && interaction.situation}
                  {interaction.type === "trip" && interaction.description}
                </CardTitle>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            {interaction.type === "outfit_recommendation" && (
              <div>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <p><span className="font-medium">Top:</span> {interaction.recommendation.top}</p>
                  <p><span className="font-medium">Bottom:</span> {interaction.recommendation.bottom}</p>
                  <p><span className="font-medium">Outerwear:</span> {interaction.recommendation.outerwear}</p>
                  <p><span className="font-medium">Shoes:</span> {interaction.recommendation.shoes}</p>
                </div>
              </div>
            )}
            {interaction.type === "purchase_recommendation" && (
              <div>
                <p className="font-medium">Recommended Item: {interaction.recommendation.item}</p>
                <p className="text-sm mt-2">{interaction.recommendation.explanation}</p>
              </div>
            )}
            {interaction.type === "trip" && (
              <div className="space-y-2">
                <div>
                  <p className="font-medium">Tops:</p>
                  <ul className="list-disc list-inside text-sm">
                    {interaction.recommendation.packingList.tops.map((item, i) => (
                      <li key={i}>{item}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <p className="font-medium">Bottoms:</p>
                  <ul className="list-disc list-inside text-sm">
                    {interaction.recommendation.packingList.bottoms.map((item, i) => (
                      <li key={i}>{item}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <p className="font-medium">Outerwear:</p>
                  <ul className="list-disc list-inside text-sm">
                    {interaction.recommendation.packingList.outerwear.map((item, i) => (
                      <li key={i}>{item}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <p className="font-medium">Shoes:</p>
                  <ul className="list-disc list-inside text-sm">
                    {interaction.recommendation.packingList.shoes.map((item, i) => (
                      <li key={i}>{item}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <p className="font-medium">Accessories:</p>
                  <ul className="list-disc list-inside text-sm">
                    {interaction.recommendation.packingList.accessories.map((item, i) => (
                      <li key={i}>{item}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

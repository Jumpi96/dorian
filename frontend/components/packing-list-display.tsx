"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Trash2 } from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import { deleteTrip } from "@/lib/trip-actions"

interface PackingListDisplayProps {
  trip?: {
    tripId: string;
    description: string;
    packingList: {
      accessories: string[];
      bottoms: string[];
      outerwear: string[];
      shoes: string[];
      tops: string[];
    };
  } | null;
  onTripDeleted?: () => void;
}

export function PackingListDisplay({ trip, onTripDeleted }: PackingListDisplayProps) {
  const [isDeleting, setIsDeleting] = useState(false)
  const { toast } = useToast()

  const handleDelete = async () => {
    if (!trip?.tripId) return

    setIsDeleting(true)
    try {
      await deleteTrip(trip.tripId)
      toast({
        title: "Trip deleted",
        description: "Your trip has been deleted successfully.",
      })
      onTripDeleted?.()
    } catch (error) {
      if (error instanceof Error && error.name === 'APIError' && (error as any).status === 429) {
        toast({
          title: "Rate Limit Exceeded",
          description: "You've reached your daily limit for trip operations. Please try again tomorrow.",
          variant: "destructive",
        })
      } else {
        toast({
          title: "Error",
          description: error instanceof Error ? error.message : "Failed to delete trip",
          variant: "destructive",
        })
      }
    } finally {
      setIsDeleting(false)
    }
  }

  if (!trip) {
    return (
      <Card>
        <CardContent className="p-6 text-center text-gray-500">
          Enter your trip details to get a packing list recommendation.
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle>Your Packing List</CardTitle>
        <Button
          variant="ghost"
          size="icon"
          onClick={handleDelete}
          disabled={isDeleting}
          className="text-red-500 hover:text-red-700 hover:bg-red-50"
        >
          <Trash2 className="h-4 w-4" />
        </Button>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {Object.entries(trip.packingList).map(([category, items]) => (
            <div key={category}>
              <h3 className="font-medium mb-2 capitalize">{category}:</h3>
              <ul className="list-disc list-inside space-y-1">
                {items.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}

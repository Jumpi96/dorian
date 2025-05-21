"use client"

import { useState, useEffect, useRef } from "react"
import { RecommendationForm } from "@/components/recommendation-form"
import { PackingListDisplay } from "@/components/packing-list-display"
import { OutfitDisplay } from "@/components/outfit-display"
import { getCurrentTrip } from "@/lib/trip-actions"
import { useToast } from "@/hooks/use-toast"

interface Trip {
  tripId: string;
  description: string;
  packingList: {
    accessories: string[];
    bottoms: string[];
    outerwear: string[];
    shoes: string[];
    tops: string[];
  };
  createdAt: string;
}

export default function PackPage() {
  const [situation, setSituation] = useState<string>()
  const [trip, setTrip] = useState<Trip | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const { toast } = useToast()
  const initialLoadDone = useRef(false)

  const fetchTrip = async () => {
    try {
      const tripData = await getCurrentTrip()
      setTrip(tripData)
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to fetch trip information",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    if (initialLoadDone.current) return
    initialLoadDone.current = true
    fetchTrip()
  }, [])

  if (isLoading) {
    return (
      <div className="container max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center text-gray-500">Loading...</div>
      </div>
    )
  }

  return (
    <div className="container max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="grid md:grid-cols-2 gap-8">
        <div>
          {trip ? (
            <>
              <h2 className="text-2xl font-bold mb-4">What should I wear?</h2>
              <p className="text-gray-600 mb-6">Get outfit recommendations for your trip.</p>

              <RecommendationForm 
                mode="wear" 
                onSituationChange={setSituation} 
                tripId={trip.tripId}
                onTripCreated={fetchTrip}
              />

              <div className="mt-8">
                <OutfitDisplay situation={situation} tripId={trip.tripId} />
              </div>
            </>
          ) : (
            <>
              <h2 className="text-2xl font-bold mb-4">What should I pack?</h2>
              <p className="text-gray-600 mb-6">Get packing recommendations based on your trip details.</p>

              <RecommendationForm 
                mode="pack" 
                onSituationChange={setSituation}
                onTripCreated={fetchTrip}
              />

              <div className="mt-8">
                <OutfitDisplay situation={situation} />
              </div>
            </>
          )}
        </div>

        <div>
          <h2 className="text-2xl font-bold mb-4">Your Packing List</h2>
          {trip && (
            <p className="text-gray-600 mb-6">{trip.description}</p>
          )}
          <PackingListDisplay trip={trip} onTripDeleted={fetchTrip} />
        </div>
      </div>
    </div>
  )
}

"use client"

import { useState } from "react"
import { WardrobeSection } from "@/components/wardrobe-section"
import { RecommendationForm } from "@/components/recommendation-form"
import { OutfitDisplay } from "@/components/outfit-display"

export default function DashboardPage() {
  const [situation, setSituation] = useState<string>()
  const [recommendationData, setRecommendationData] = useState<{ outfit: Record<string, string>, interaction_id: string }>()

  const handleSituationChange = (newSituation: string, data?: { outfit: Record<string, string>, interaction_id: string }) => {
    setSituation(newSituation)
    if (data) {
      setRecommendationData(data)
    }
  }

  return (
    <div className="container max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="grid md:grid-cols-2 gap-8">
        <div>
          <h2 className="text-2xl font-bold mb-4">What should I wear?</h2>
          <p className="text-gray-600 mb-6">Get outfit recommendations based on your wardrobe and occasion.</p>

          <RecommendationForm mode="wear" onSituationChange={handleSituationChange} />

          <div className="mt-8">
            <OutfitDisplay situation={situation} initialData={recommendationData} />
          </div>
        </div>

        <div>
          <WardrobeSection />
        </div>
      </div>
    </div>
  )
}

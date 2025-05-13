"use client"

import { useState } from "react"
import { WardrobeSection } from "@/components/wardrobe-section"
import { RecommendationForm } from "@/components/recommendation-form"
import { BuyRecommendationDisplay } from "@/components/buy-recommendation-display"

export default function BuyPage() {
  const [situation, setSituation] = useState<string>()

  return (
    <div className="container max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="grid md:grid-cols-2 gap-8">
        <div>
          <h2 className="text-2xl font-bold mb-4">What should I buy next?</h2>
          <p className="text-gray-600 mb-6">Get recommendations on what to add to your wardrobe.</p>

          <RecommendationForm mode="buy" onSituationChange={setSituation} />

          <div className="mt-8">
            <BuyRecommendationDisplay situation={situation} />
          </div>
        </div>

        <div>
          <WardrobeSection />
        </div>
      </div>
    </div>
  )
}

import { WardrobeSection } from "@/components/wardrobe-section"
import { RecommendationForm } from "@/components/recommendation-form"
import { OutfitDisplay } from "@/components/outfit-display"

export default function DashboardPage() {
  return (
    <div className="grid md:grid-cols-2 gap-8">
      <div>
        <h2 className="text-2xl font-bold mb-4">What should I wear?</h2>
        <p className="text-gray-600 mb-6">Get outfit recommendations based on your wardrobe and occasion.</p>

        <RecommendationForm mode="wear" />

        <div className="mt-8">
          <OutfitDisplay />
        </div>
      </div>

      <div>
        <WardrobeSection />
      </div>
    </div>
  )
}

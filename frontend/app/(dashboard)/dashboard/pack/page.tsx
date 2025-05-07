import { WardrobeSection } from "@/components/wardrobe-section"
import { RecommendationForm } from "@/components/recommendation-form"
import { PackingListDisplay } from "@/components/packing-list-display"

export default function PackPage() {
  return (
    <div className="grid md:grid-cols-2 gap-8">
      <div>
        <h2 className="text-2xl font-bold mb-4">What should I pack?</h2>
        <p className="text-gray-600 mb-6">Get packing recommendations based on your trip details.</p>

        <RecommendationForm mode="pack" />

        <div className="mt-8">
          <PackingListDisplay />
        </div>
      </div>

      <div>
        <WardrobeSection />
      </div>
    </div>
  )
}

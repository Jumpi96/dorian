import { HistoryList } from "@/components/history-list"

export default function HistoryPage() {
  return (
    <div className="container max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h2 className="text-2xl font-bold mb-4">Recommendation History</h2>
      <p className="text-gray-600 mb-6">View your past outfit and packing recommendations.</p>

      <HistoryList />
    </div>
  )
}

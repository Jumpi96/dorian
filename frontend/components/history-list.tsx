"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { formatDistanceToNow } from "date-fns"

type HistoryItem = {
  id: string
  mode: "wear" | "pack" | "buy"
  prompt: string
  response: any
  timestamp: string
  feedback?: "thumbsUp" | "thumbsDown"
}

export function HistoryList() {
  const [history, setHistory] = useState<HistoryItem[]>([
    {
      id: "1",
      mode: "wear",
      prompt: "What should I wear to a casual dinner?",
      response: {
        top: "Black t-shirt",
        bottom: "Olive chinos",
        shoes: "White sneakers",
        outerwear: "Grey hoodie",
      },
      timestamp: "2025-04-08T14:00:00Z",
      feedback: "thumbsUp",
    },
    {
      id: "2",
      mode: "pack",
      prompt: "What should I pack for a weekend trip?",
      response: {
        tops: ["White t-shirt", "Blue button-up shirt"],
        bottoms: ["Blue jeans", "Khaki shorts"],
        shoes: ["White sneakers"],
        outerwear: ["Light jacket"],
      },
      timestamp: "2025-04-07T10:30:00Z",
      feedback: "thumbsDown",
    },
    {
      id: "3",
      mode: "buy",
      prompt: "What should I buy next?",
      response: {
        item: "Navy blue blazer",
        reason: "A versatile blazer would complement your existing casual items.",
      },
      timestamp: "2025-04-06T16:45:00Z",
    },
  ])

  if (history.length === 0) {
    return (
      <Card>
        <CardContent className="p-6 text-center text-gray-500">
          You haven't received any recommendations yet.
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      {history.map((item) => (
        <Card key={item.itemId}>
          <CardHeader className="pb-2">
            <div className="flex justify-between items-start">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <Badge variant={getBadgeVariant(item.mode)}>{item.mode.toUpperCase()}</Badge>
                  <span className="text-sm text-gray-500">
                    {formatDistanceToNow(new Date(item.timestamp), { addSuffix: true })}
                  </span>
                </div>
                <CardTitle className="text-lg">{item.prompt}</CardTitle>
              </div>
              {item.feedback && (
                <Badge variant={item.feedback === "thumbsUp" ? "outline" : "secondary"}>
                  {item.feedback === "thumbsUp" ? "Liked" : "Disliked"}
                </Badge>
              )}
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {item.mode === "wear" && renderWearResponse(item.response)}
              {item.mode === "pack" && renderPackResponse(item.response)}
              {item.mode === "buy" && renderBuyResponse(item.response)}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

function getBadgeVariant(mode: string): "default" | "secondary" | "outline" {
  switch (mode) {
    case "wear":
      return "default"
    case "pack":
      return "secondary"
    case "buy":
      return "outline"
    default:
      return "default"
  }
}

function renderWearResponse(response: any) {
  return (
    <>
      {Object.entries(response).map(([category, item]) => (
        <div key={category} className="flex justify-between">
          <span className="capitalize font-medium">{category}:</span>
          <span>{item as string}</span>
        </div>
      ))}
    </>
  )
}

function renderPackResponse(response: any) {
  return (
    <>
      {Object.entries(response).map(([category, items]) => (
        <div key={category}>
          <h3 className="capitalize font-medium mb-1">{category}:</h3>
          <ul className="list-disc pl-5">
            {(items as string[]).map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      ))}
    </>
  )
}

function renderBuyResponse(response: any) {
  return (
    <>
      <div>
        <h3 className="font-medium mb-1">Item:</h3>
        <p>{response.item}</p>
      </div>
      <div className="mt-2">
        <h3 className="font-medium mb-1">Why:</h3>
        <p>{response.reason}</p>
      </div>
    </>
  )
}

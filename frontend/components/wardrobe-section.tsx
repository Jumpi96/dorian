"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Plus, Trash2 } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useToast } from "@/hooks/use-toast"
import { addWardrobeItem, deleteWardrobeItem } from "@/lib/wardrobe-actions"

export function WardrobeSection() {
  const [newItem, setNewItem] = useState("")
  const [items, setItems] = useState<{ id: string; description: string }[]>([
    { id: "1", description: "Black t-shirt" },
    { id: "2", description: "Blue jeans" },
    { id: "3", description: "White sneakers" },
    { id: "4", description: "Gray hoodie" },
  ])
  const [isLoading, setIsLoading] = useState(false)
  const { toast } = useToast()

  const handleAddItem = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newItem.trim()) return

    setIsLoading(true)
    try {
      const id = await addWardrobeItem(newItem)
      setItems([...items, { id, description: newItem }])
      setNewItem("")
      toast({
        title: "Item added",
        description: `${newItem} has been added to your wardrobe.`,
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to add item to your wardrobe.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleDeleteItem = async (id: string) => {
    try {
      await deleteWardrobeItem(id)
      setItems(items.filter((item) => item.id !== id))
      toast({
        title: "Item removed",
        description: "Item has been removed from your wardrobe.",
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to remove item from your wardrobe.",
        variant: "destructive",
      })
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>My Wardrobe</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleAddItem} className="flex gap-2 mb-4">
          <Input
            placeholder="Add a clothing item (e.g., brown sweatshirt)"
            value={newItem}
            onChange={(e) => setNewItem(e.target.value)}
          />
          <Button type="submit" size="icon" disabled={isLoading}>
            <Plus className="h-4 w-4" />
          </Button>
        </form>

        {items.length === 0 ? (
          <p className="text-gray-500 text-center py-4">Your wardrobe is empty. Add some items to get started.</p>
        ) : (
          <ul className="space-y-2">
            {items.map((item) => (
              <li key={item.id} className="flex justify-between items-center p-2 border rounded-md">
                <span>{item.description}</span>
                <Button variant="ghost" size="icon" onClick={() => handleDeleteItem(item.id)}>
                  <Trash2 className="h-4 w-4 text-gray-500" />
                </Button>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  )
}

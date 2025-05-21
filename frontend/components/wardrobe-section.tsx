"use client"

import type React from "react"
import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Plus, Trash2 } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useToast } from "@/hooks/use-toast"
import { addWardrobeItem, deleteWardrobeItem, getWardrobeItems } from "@/lib/wardrobe-actions"
import { useAuth } from "@/lib/auth"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"

interface WardrobeItem {
  itemId: string
  description: string
}

export function WardrobeSection() {
  const [newItem, setNewItem] = useState("")
  const [isMultipleMode, setIsMultipleMode] = useState(false)
  const [items, setItems] = useState<WardrobeItem[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 5
  const { toast } = useToast()
  const { isAuthenticated, login } = useAuth()

  useEffect(() => {
    if (isAuthenticated) {
      loadWardrobeItems()
    }
  }, [isAuthenticated])

  const loadWardrobeItems = async () => {
    try {
      const response = await getWardrobeItems()
      // Ensure we have an array of items
      const wardrobeItems = Array.isArray(response) ? response : response.items || []
      setItems(wardrobeItems)
    } catch (error) {
      console.error('Error loading wardrobe items:', error)
      setItems([])
      if (error instanceof Error && error.name === 'APIError' && (error as any).status === 429) {
        toast({
          title: "Rate Limit Exceeded",
          description: "You've reached your daily limit for wardrobe operations. Please try again tomorrow.",
          variant: "destructive",
        })
      } else {
        toast({
          title: "Error",
          description: "Failed to load wardrobe items.",
          variant: "destructive",
        })
      }
    }
  }

  const handleAddItem = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newItem.trim()) return

    if (!isAuthenticated) {
      login()
      return
    }

    setIsLoading(true)
    try {
      if (isMultipleMode) {
        const items = newItem.split('\n').filter(item => item.trim())
        const addedItems: WardrobeItem[] = []
        
        for (const item of items) {
          const itemId = await addWardrobeItem(item)
          addedItems.push({ itemId, description: item })
        }
        
        setItems(prevItems => [...prevItems, ...addedItems])
        toast({
          title: "Items added",
          description: `Added ${addedItems.length} item${addedItems.length > 1 ? 's' : ''} to your wardrobe.`,
        })
      } else {
        const itemId = await addWardrobeItem(newItem)
        setItems(prevItems => [...prevItems, { itemId, description: newItem }])
        toast({
          title: "Item added",
          description: `${newItem} has been added to your wardrobe.`,
        })
      }
      setNewItem("")
    } catch (error) {
      console.error('Error adding item(s):', error)
      toast({
        title: "Error",
        description: `Failed to add ${isMultipleMode ? 'items' : 'item'} to your wardrobe.`,
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleDeleteItem = async (id: string) => {
    if (!isAuthenticated) {
      login()
      return
    }

    try {
      await deleteWardrobeItem(id)
      setItems(prevItems => prevItems.filter((item) => item.itemId !== id))
      toast({
        title: "Item removed",
        description: "Item has been removed from your wardrobe.",
      })
    } catch (error) {
      console.error('Error deleting item:', error)
      toast({
        title: "Error",
        description: "Failed to remove item from your wardrobe.",
        variant: "destructive",
      })
    }
  }

  if (!isAuthenticated) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>My Wardrobe</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-500 text-center py-4">
            Please log in to manage your wardrobe.
          </p>
          <Button onClick={login} className="w-full">
            Log in
          </Button>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>My Wardrobe</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleAddItem} className="flex flex-col gap-2 mb-4">
          {isMultipleMode ? (
            <Textarea
              placeholder="Add clothing items (one per line)"
              value={newItem}
              onChange={(e) => setNewItem(e.target.value)}
              className="min-h-[100px]"
            />
          ) : (
            <Input
              placeholder="Add a clothing item (e.g., brown sweatshirt)"
              value={newItem}
              onChange={(e) => setNewItem(e.target.value)}
            />
          )}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Switch
                id="multiple-mode"
                checked={isMultipleMode}
                onCheckedChange={setIsMultipleMode}
              />
              <Label htmlFor="multiple-mode">Multiple</Label>
            </div>
            <Button type="submit" size={isMultipleMode ? "default" : "icon"} disabled={isLoading}>
              <Plus className="h-4 w-4" />
              {isMultipleMode && <span className="ml-2">Add Items</span>}
            </Button>
          </div>
        </form>

        {!Array.isArray(items) || items.length === 0 ? (
          <p className="text-gray-500 text-center py-4">Your wardrobe is empty. Add some items to get started.</p>
        ) : (
          <>
            <ul className="space-y-2">
              {items
                .slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage)
                .map((item) => (
                  <li key={item.itemId} className="flex justify-between items-center p-2 border rounded-md">
                    <span>{item.description}</span>
                    <Button variant="ghost" size="icon" onClick={() => handleDeleteItem(item.itemId)}>
                      <Trash2 className="h-4 w-4 text-gray-500" />
                    </Button>
                  </li>
                ))}
            </ul>
            {items.length > itemsPerPage && (
              <div className="flex justify-center items-center gap-2 mt-4">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                  disabled={currentPage === 1}
                >
                  Previous
                </Button>
                <span className="text-sm text-gray-500">
                  Page {currentPage} of {Math.ceil(items.length / itemsPerPage)}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrentPage(prev => Math.min(prev + 1, Math.ceil(items.length / itemsPerPage)))}
                  disabled={currentPage === Math.ceil(items.length / itemsPerPage)}
                >
                  Next
                </Button>
              </div>
            )}
          </>
        )}
      </CardContent>
    </Card>
  )
}

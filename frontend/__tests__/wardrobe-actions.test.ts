import { addWardrobeItem, deleteWardrobeItem, getWardrobeItems } from '@/lib/wardrobe-actions'
import { cookies } from 'next/headers'
import { revalidatePath } from 'next/cache'

// Mock the next/headers and next/cache modules
jest.mock('next/headers', () => ({
  cookies: jest.fn()
}))

jest.mock('next/cache', () => ({
  revalidatePath: jest.fn()
}))

// Mock fetch
global.fetch = jest.fn()

describe('Wardrobe Actions', () => {
  const mockToken = 'mock-token'
  const mockCookieStore = {
    get: jest.fn().mockReturnValue({ value: mockToken })
  }

  beforeEach(() => {
    jest.clearAllMocks()
    ;(cookies as jest.Mock).mockReturnValue(mockCookieStore)
    ;(global.fetch as jest.Mock).mockReset()
  })

  describe('addWardrobeItem', () => {
    it('should successfully add a wardrobe item', async () => {
      const mockResponse = { itemId: '123', description: 'Test item' }
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse)
      })

      const result = await addWardrobeItem('Test item')

      expect(result).toBe('123')
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:3001/wardrobe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${mockToken}`
        },
        body: JSON.stringify({ description: 'Test item' })
      })
      expect(revalidatePath).toHaveBeenCalledWith('/dashboard')
    })

    it('should throw error when not authenticated', async () => {
      mockCookieStore.get.mockReturnValueOnce(undefined)

      await expect(addWardrobeItem('Test item')).rejects.toThrow('Not authenticated')
    })

    it('should throw error when API call fails', async () => {
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        json: () => Promise.resolve({ message: 'Failed to add wardrobe item' })
      })

      await expect(addWardrobeItem('Test item')).rejects.toThrow('Failed to add wardrobe item')
    })
  })

  describe('deleteWardrobeItem', () => {
    it('should successfully delete a wardrobe item', async () => {
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true
      })

      await deleteWardrobeItem('123')

      expect(global.fetch).toHaveBeenCalledWith('http://localhost:3001/wardrobe/123', {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${mockToken}`
        }
      })
      expect(revalidatePath).toHaveBeenCalledWith('/dashboard')
    })

    it('should throw error when not authenticated', async () => {
      mockCookieStore.get.mockReturnValueOnce(undefined)

      await expect(deleteWardrobeItem('123')).rejects.toThrow('Not authenticated')
    })

    it('should throw error when API call fails', async () => {
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        json: () => Promise.resolve({ message: 'Failed to delete wardrobe item' })
      })

      await expect(deleteWardrobeItem('123')).rejects.toThrow('Failed to delete wardrobe item')
    })
  })

  describe('getWardrobeItems', () => {
    it('should successfully fetch wardrobe items', async () => {
      const mockItems = [{ itemId: '123', description: 'Test item' }]
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockItems)
      })

      const result = await getWardrobeItems()

      expect(result).toEqual(mockItems)
      expect(global.fetch).toHaveBeenCalledWith('http://localhost:3001/wardrobe', {
        headers: {
          'Authorization': `Bearer ${mockToken}`
        }
      })
    })

    it('should throw error when not authenticated', async () => {
      mockCookieStore.get.mockReturnValueOnce(undefined)

      await expect(getWardrobeItems()).rejects.toThrow('Not authenticated')
    })

    it('should throw error when API call fails', async () => {
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        json: () => Promise.resolve({ message: 'Failed to fetch wardrobe items' })
      })

      await expect(getWardrobeItems()).rejects.toThrow('Failed to fetch wardrobe items')
    })
  })
}) 
import { getRecommendation } from '../recommendation-actions'
import { cookies } from 'next/headers'

// Mock next/cache's revalidatePath
jest.mock('next/cache', () => ({
  revalidatePath: jest.fn(),
}))

// Mock next/headers
jest.mock('next/headers', () => ({
  cookies: jest.fn()
}))

// Mock fetch
global.fetch = jest.fn()

describe('recommendation-actions', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  describe('getRecommendation', () => {
    const mockToken = 'test-token'
    const mockSituation = 'casual dinner'
    const mockResponse = {
      outfit: {
        top: 'Black t-shirt',
        bottom: 'Blue jeans',
        shoes: 'White sneakers'
      },
      interaction_id: 'test-interaction-id'
    }

    it('should successfully get a recommendation', async () => {
      // Mock cookies
      ;(cookies as jest.Mock).mockReturnValue({
        get: jest.fn().mockReturnValue({ value: mockToken })
      })

      // Mock fetch response
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: jest.fn().mockResolvedValueOnce(mockResponse)
      })

      const result = await getRecommendation('wear', mockSituation)

      expect(result).toEqual(mockResponse)
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:3001/recommend/wear',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${mockToken}`
          },
          body: JSON.stringify({ situation: mockSituation })
        }
      )
    })

    it('should throw error when not authenticated', async () => {
      // Mock cookies with no token
      ;(cookies as jest.Mock).mockReturnValue({
        get: jest.fn().mockReturnValue(undefined)
      })

      await expect(getRecommendation('wear', mockSituation))
        .rejects
        .toThrow('Not authenticated')
    })

    it('should throw error when API request fails', async () => {
      // Mock cookies
      ;(cookies as jest.Mock).mockReturnValue({
        get: jest.fn().mockReturnValue({ value: mockToken })
      })

      // Mock fetch error response
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        json: jest.fn().mockResolvedValueOnce({ message: 'API Error' })
      })

      await expect(getRecommendation('wear', mockSituation))
        .rejects
        .toThrow('API Error')
    })

    it('should handle different recommendation modes', async () => {
      // Mock cookies
      ;(cookies as jest.Mock).mockReturnValue({
        get: jest.fn().mockReturnValue({ value: mockToken })
      })

      // Mock fetch response
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: jest.fn().mockResolvedValueOnce(mockResponse)
      })

      await getRecommendation('pack', mockSituation)

      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:3001/recommend/pack',
        expect.any(Object)
      )
    })
  })
}) 
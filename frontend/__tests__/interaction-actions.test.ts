import { getInteractions } from '@/lib/interaction-actions';
import { cookies } from 'next/headers';

// Mock next/headers
jest.mock('next/headers', () => ({
  cookies: jest.fn()
}));

// Mock fetch
global.fetch = jest.fn();

describe('interaction-actions', () => {
  const mockToken = 'test-token';
  const mockInteractions = [
    {
      createdAt: '2025-05-11T18:32:28.970390+00:00',
      interactionId: 'buy_2025-05-11T18:32:28.970390+00:00',
      recommendation: {
        explanation: 'A navy blue blazer would be a great addition...',
        item: 'navy blue blazer'
      },
      situation: 'What should I wear for a casual dinner tonight?',
      type: 'purchase_recommendation',
      userId: '118389069705649237875'
    },
    {
      createdAt: '2025-05-11T18:01:42.079166+00:00',
      interactionId: 'rec_2025-05-11T18:01:42.079154+00:00',
      recommendation: {
        bottom: 'lighter Blue Denim slim jeans',
        outerwear: 'grey coat',
        shoes: 'casual sneakers',
        top: 'blue sweatshirt'
      },
      situation: 'What should I wear for a casual dinner tonight?',
      type: 'outfit_recommendation',
      userId: '118389069705649237875'
    }
  ];

  beforeEach(() => {
    jest.clearAllMocks();
    (cookies as jest.Mock).mockReturnValue({
      get: jest.fn().mockReturnValue({ value: mockToken })
    });
  });

  describe('getInteractions', () => {
    it('should successfully fetch interactions', async () => {
      // Mock fetch response
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: jest.fn().mockResolvedValueOnce(mockInteractions)
      });

      const result = await getInteractions();

      expect(result).toEqual(mockInteractions);
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/interactions'),
        {
          headers: {
            'Authorization': `Bearer ${mockToken}`
          }
        }
      );
    });

    it('should throw error when not authenticated', async () => {
      // Mock cookies with no token
      (cookies as jest.Mock).mockReturnValue({
        get: jest.fn().mockReturnValue(undefined)
      });

      await expect(getInteractions()).rejects.toThrow('Not authenticated');
    });

    it('should throw error when API request fails', async () => {
      // Mock fetch error response
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false
      });

      await expect(getInteractions()).rejects.toThrow('Failed to fetch interactions');
    });
  });
}); 
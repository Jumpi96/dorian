import '@testing-library/jest-dom'
import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import { OutfitDisplay } from '../outfit-display'
import { getRecommendation } from '@/lib/recommendation-actions'
import { submitFeedback } from '@/lib/feedback-actions'
import { useToast } from '@/hooks/use-toast'

// Mock the server actions
jest.mock('@/lib/recommendation-actions')
jest.mock('@/lib/feedback-actions')
jest.mock('@/hooks/use-toast')

describe('OutfitDisplay', () => {
  const mockToast = {
    toast: jest.fn()
  }

  beforeEach(() => {
    jest.clearAllMocks()
    ;(useToast as jest.Mock).mockReturnValue(mockToast)
  })

  it('should show initial message when no situation is provided', () => {
    render(<OutfitDisplay />)
    expect(screen.getByText("Tell me about your occasion and I'll help you pick the perfect outfit!")).toBeInTheDocument()
  })

  it('should show loading state while fetching recommendation', async () => {
    const mockSituation = 'casual dinner'
    ;(getRecommendation as jest.Mock).mockImplementation(() => new Promise(() => {}))

    render(<OutfitDisplay situation={mockSituation} />)
    expect(screen.getByText('Loading your outfit recommendation...')).toBeInTheDocument()
  })

  it('should display outfit recommendation when available', async () => {
    const mockSituation = 'casual dinner'
    const mockOutfit = {
      top: 'Black t-shirt',
      bottom: 'Blue jeans',
      shoes: 'White sneakers'
    }
    const mockInteractionId = 'test-interaction-id'

    ;(getRecommendation as jest.Mock).mockResolvedValueOnce({
      outfit: mockOutfit,
      interaction_id: mockInteractionId
    })

    render(<OutfitDisplay situation={mockSituation} />)

    await waitFor(() => {
      expect(screen.getByText('Your Outfit Recommendation')).toBeInTheDocument()
      expect(screen.getByText('top:')).toBeInTheDocument()
      expect(screen.getByText('Black t-shirt')).toBeInTheDocument()
      expect(screen.getByText('bottom:')).toBeInTheDocument()
      expect(screen.getByText('Blue jeans')).toBeInTheDocument()
      expect(screen.getByText('shoes:')).toBeInTheDocument()
      expect(screen.getByText('White sneakers')).toBeInTheDocument()
    })
  })

  it('should show error toast when recommendation fails', async () => {
    const mockSituation = 'casual dinner'
    const mockError = new Error('API Error')
    ;(getRecommendation as jest.Mock).mockRejectedValueOnce(mockError)

    render(<OutfitDisplay situation={mockSituation} />)

    await waitFor(() => {
      expect(mockToast.toast).toHaveBeenCalledWith({
        title: 'Error',
        description: 'API Error',
        variant: 'destructive'
      })
    })
  })

  it('should handle feedback submission', async () => {
    const mockSituation = 'casual dinner'
    const mockOutfit = {
      top: 'Black t-shirt',
      bottom: 'Blue jeans',
      shoes: 'White sneakers'
    }
    const mockInteractionId = 'test-interaction-id'

    ;(getRecommendation as jest.Mock).mockResolvedValueOnce({
      outfit: mockOutfit,
      interaction_id: mockInteractionId
    })
    ;(submitFeedback as jest.Mock).mockResolvedValueOnce(undefined)

    render(<OutfitDisplay situation={mockSituation} />)

    await waitFor(() => {
      expect(screen.getByText('Like')).toBeInTheDocument()
      expect(screen.getByText('Dislike')).toBeInTheDocument()
    })

    fireEvent.click(screen.getByText('Like'))

    await waitFor(() => {
      expect(submitFeedback).toHaveBeenCalledWith(mockInteractionId, 'thumbsUp')
      expect(mockToast.toast).toHaveBeenCalledWith({
        title: 'Feedback submitted',
        description: 'Thank you for your feedback!'
      })
    })

    // Verify buttons are disabled after feedback
    expect(screen.getByText('Like')).toBeDisabled()
    expect(screen.getByText('Dislike')).toBeDisabled()
  })

  it('should handle feedback submission error', async () => {
    const mockSituation = 'casual dinner'
    const mockOutfit = {
      top: 'Black t-shirt',
      bottom: 'Blue jeans',
      shoes: 'White sneakers'
    }
    const mockInteractionId = 'test-interaction-id'

    ;(getRecommendation as jest.Mock).mockResolvedValueOnce({
      outfit: mockOutfit,
      interaction_id: mockInteractionId
    })
    ;(submitFeedback as jest.Mock).mockRejectedValueOnce(new Error('Feedback Error'))

    render(<OutfitDisplay situation={mockSituation} />)

    await waitFor(() => {
      expect(screen.getByText('Like')).toBeInTheDocument()
    })

    fireEvent.click(screen.getByText('Like'))

    await waitFor(() => {
      expect(mockToast.toast).toHaveBeenCalledWith({
        title: 'Error',
        description: 'Failed to submit feedback.',
        variant: 'destructive'
      })
    })

    // Verify buttons are still enabled after error
    expect(screen.getByText('Like')).not.toBeDisabled()
    expect(screen.getByText('Dislike')).not.toBeDisabled()
  })
}) 
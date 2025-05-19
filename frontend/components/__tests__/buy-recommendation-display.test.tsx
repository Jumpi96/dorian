import '@testing-library/jest-dom'
import { render, screen, waitFor, fireEvent, act } from '@testing-library/react'
import { BuyRecommendationDisplay } from '../buy-recommendation-display'
import { getRecommendation } from '@/lib/recommendation-actions'
import { submitFeedback } from '@/lib/feedback-actions'
import { useToast } from '@/hooks/use-toast'

// Mock the server actions
jest.mock('@/lib/recommendation-actions')
jest.mock('@/lib/feedback-actions')
jest.mock('@/hooks/use-toast')

describe('BuyRecommendationDisplay', () => {
  const mockToast = {
    toast: jest.fn(),
  }

  beforeEach(() => {
    jest.clearAllMocks()
    ;(useToast as jest.Mock).mockReturnValue(mockToast)
    ;(getRecommendation as jest.Mock).mockResolvedValue({
      item_to_buy: {
        item: "Black leather loafers",
        explanation: "These versatile loafers would be perfect for your casual dinner."
      },
      interaction_id: "test-interaction-id"
    })
    ;(submitFeedback as jest.Mock).mockResolvedValue(undefined)
  })

  it('shows initial message when no situation is provided', () => {
    render(<BuyRecommendationDisplay />)
    expect(screen.getByText(/Tell me about your situation/i)).toBeInTheDocument()
  })

  it('shows loading state while fetching recommendation', async () => {
    // Create a promise that we can control
    let resolvePromise: (value: any) => void
    const promise = new Promise((resolve) => {
      resolvePromise = resolve
    })
    
    // Mock getRecommendation to return our controlled promise
    ;(getRecommendation as jest.Mock).mockImplementation(() => promise)

    // Render the component
    await act(async () => {
      render(<BuyRecommendationDisplay situation="casual dinner" />)
    })

    // Verify loading state is shown
    expect(screen.getByText(/Loading your purchase recommendation/i)).toBeInTheDocument()

    // Resolve the promise
    await act(async () => {
      resolvePromise({
        item_to_buy: {
          item: "Black leather loafers",
          explanation: "These versatile loafers would be perfect for your casual dinner."
        },
        interaction_id: "test-interaction-id"
      })
    })

    // Verify recommendation is shown after loading
    await waitFor(() => {
      expect(screen.getByText('Recommended Purchase')).toBeInTheDocument()
    })
  })

  it('displays recommendation when data is loaded', async () => {
    await act(async () => {
      render(<BuyRecommendationDisplay situation="casual dinner" />)
    })

    await waitFor(() => {
      expect(screen.getByText('Recommended Purchase')).toBeInTheDocument()
      expect(screen.getByText('Black leather loafers')).toBeInTheDocument()
      expect(screen.getByText('These versatile loafers would be perfect for your casual dinner.')).toBeInTheDocument()
    })
  })

  it('handles error when fetching recommendation fails', async () => {
    const error = new Error('Failed to fetch recommendation')
    ;(getRecommendation as jest.Mock).mockRejectedValue(error)

    await act(async () => {
      render(<BuyRecommendationDisplay situation="casual dinner" />)
    })

    await waitFor(() => {
      expect(mockToast.toast).toHaveBeenCalledWith({
        title: 'Error',
        description: 'Failed to fetch recommendation',
        variant: 'destructive',
      })
    })
  })

  it('submits feedback successfully', async () => {
    await act(async () => {
      render(<BuyRecommendationDisplay situation="casual dinner" />)
    })

    await waitFor(() => {
      expect(screen.getByText('Recommended Purchase')).toBeInTheDocument()
    })

    await act(async () => {
      fireEvent.click(screen.getByText('Like'))
    })

    await waitFor(() => {
      expect(submitFeedback).toHaveBeenCalledWith('test-interaction-id', 'thumbsUp')
      expect(mockToast.toast).toHaveBeenCalledWith({
        title: 'Feedback submitted',
        description: 'Thank you for your feedback!',
      })
    })
  })

  it('handles feedback submission error', async () => {
    const error = new Error('Failed to submit feedback')
    ;(submitFeedback as jest.Mock).mockRejectedValue(error)

    await act(async () => {
      render(<BuyRecommendationDisplay situation="casual dinner" />)
    })

    await waitFor(() => {
      expect(screen.getByText('Recommended Purchase')).toBeInTheDocument()
    })

    await act(async () => {
      fireEvent.click(screen.getByText('Like'))
    })

    await waitFor(() => {
      expect(mockToast.toast).toHaveBeenCalledWith({
        title: 'Error',
        description: 'Failed to submit feedback',
        variant: 'destructive',
      })
    })
  })

  it('disables feedback buttons after submission', async () => {
    await act(async () => {
      render(<BuyRecommendationDisplay situation="casual dinner" />)
    })

    await waitFor(() => {
      expect(screen.getByText('Recommended Purchase')).toBeInTheDocument()
    })

    await act(async () => {
      fireEvent.click(screen.getByText('Like'))
    })

    await waitFor(() => {
      expect(screen.getByText('Like')).toBeDisabled()
      expect(screen.getByText('Dislike')).toBeDisabled()
    })
  })
}) 
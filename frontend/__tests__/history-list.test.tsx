import { render, screen, waitFor } from '@testing-library/react';
import { HistoryList } from '@/components/history-list';
import { getInteractions } from '@/lib/interaction-actions';
import { format } from 'date-fns';

// Mock the interaction actions
jest.mock('@/lib/interaction-actions', () => ({
  getInteractions: jest.fn()
}));

// Mock the toast
jest.mock('@/components/ui/use-toast', () => ({
  useToast: () => ({
    toast: jest.fn()
  })
}));

describe('HistoryList', () => {
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
    },
    {
      createdAt: '2025-05-14T07:12:17.342208+00:00',
      description: 'Weeklong Japan Trip: 25°C',
      interactionId: 'trip_2025-05-14T07:12:17.342208+00:00',
      recommendation: {
        packingList: {
          accessories: ['suggest to pack an umbrella in case it rains'],
          bottoms: ['lighter Blue Denim slim jeans'],
          outerwear: ['grey coat'],
          shoes: ['suggest to pack comfortable shoes suitable for walking in case it rains'],
          tops: ['dark grey hoodie', 'blue sweatshirt', 'black shirt']
        }
      },
      type: 'trip',
      userId: '118389069705649237875'
    }
  ];

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should show loading state initially', () => {
    (getInteractions as jest.Mock).mockImplementation(() => new Promise(() => {}));
    render(<HistoryList />);
    
    // Each card has 3 skeleton elements (header + 2 content lines)
    expect(screen.getAllByTestId('skeleton')).toHaveLength(9);
  });

  it('should show empty state when no interactions', async () => {
    (getInteractions as jest.Mock).mockResolvedValueOnce([]);
    render(<HistoryList />);
    
    await waitFor(() => {
      expect(screen.getByText('No history available yet.')).toBeInTheDocument();
    });
  });

  it('should handle error state', async () => {
    const mockToast = jest.fn();
    jest.spyOn(require('@/components/ui/use-toast'), 'useToast').mockReturnValue({
      toast: mockToast
    });

    (getInteractions as jest.Mock).mockRejectedValueOnce(new Error('API Error'));
    render(<HistoryList />);
    
    await waitFor(() => {
      expect(mockToast).toHaveBeenCalledWith({
        title: 'Error',
        description: 'Failed to load history',
        variant: 'destructive',
      });
    });
  });
}); 
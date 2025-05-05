import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import WardrobePage from '../WardrobePage';
import { wardrobeService } from '../../services/wardrobeService';

// Mock the wardrobe service
vi.mock('../../services/wardrobeService');

describe('WardrobePage', () => {
    beforeEach(() => {
        // Clear all mocks before each test
        vi.clearAllMocks();
        
        // Mock localStorage
        Storage.prototype.getItem = vi.fn(() => 'mock-token');
    });

    it('loads and displays wardrobe items', async () => {
        // Mock the getItems response
        wardrobeService.getItems.mockResolvedValueOnce({
            items: [
                { itemId: '1', description: 'Blue jeans' },
                { itemId: '2', description: 'White t-shirt' }
            ]
        });

        render(<WardrobePage />);

        // Check loading state
        expect(screen.getByText('Loading...')).toBeInTheDocument();

        // Wait for items to load
        await waitFor(() => {
            expect(screen.getByText('Blue jeans')).toBeInTheDocument();
            expect(screen.getByText('White t-shirt')).toBeInTheDocument();
        });

        // Verify service was called
        expect(wardrobeService.getItems).toHaveBeenCalledTimes(1);
    });

    it('shows empty state when no items', async () => {
        // Mock empty response
        wardrobeService.getItems.mockResolvedValueOnce({ items: [] });

        render(<WardrobePage />);

        await waitFor(() => {
            expect(screen.getByText(/Your wardrobe is empty/i)).toBeInTheDocument();
        });
    });

    it('adds a new item and refreshes the list', async () => {
        // Mock initial empty state
        wardrobeService.getItems.mockResolvedValueOnce({ items: [] });
        
        // Mock successful add
        wardrobeService.addItem.mockResolvedValueOnce({
            itemId: '1',
            description: 'New item'
        });
        
        // Mock updated list
        wardrobeService.getItems.mockResolvedValueOnce({
            items: [{ itemId: '1', description: 'New item' }]
        });

        render(<WardrobePage />);

        // Wait for initial load
        await waitFor(() => {
            expect(screen.getByText(/Your wardrobe is empty/i)).toBeInTheDocument();
        });

        // Add new item
        const input = screen.getByPlaceholderText(/Add a new item/i);
        fireEvent.change(input, { target: { value: 'New item' } });
        fireEvent.click(screen.getByText('Add'));

        // Verify service calls
        await waitFor(() => {
            expect(wardrobeService.addItem).toHaveBeenCalledWith('New item');
            expect(wardrobeService.getItems).toHaveBeenCalledTimes(2);
        });

        // Verify new item is displayed
        expect(screen.getByText('New item')).toBeInTheDocument();
    });

    it('shows error message when API calls fail', async () => {
        // Mock failed getItems
        wardrobeService.getItems.mockRejectedValueOnce(new Error('API Error'));

        render(<WardrobePage />);

        await waitFor(() => {
            expect(screen.getByText(/Failed to load wardrobe items/i)).toBeInTheDocument();
        });
    });
}); 
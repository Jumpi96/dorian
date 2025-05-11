import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { WardrobeSection } from '@/components/wardrobe-section'
import { useAuth } from '@/lib/auth'
import { addWardrobeItem, deleteWardrobeItem, getWardrobeItems } from '@/lib/wardrobe-actions'

// Mock the auth hook
jest.mock('@/lib/auth', () => ({
  useAuth: jest.fn()
}))

// Mock the wardrobe actions
jest.mock('@/lib/wardrobe-actions', () => ({
  addWardrobeItem: jest.fn(),
  deleteWardrobeItem: jest.fn(),
  getWardrobeItems: jest.fn()
}))

// Mock the toast hook
jest.mock('@/hooks/use-toast', () => ({
  useToast: () => ({
    toast: jest.fn()
  })
}))

describe('WardrobeSection', () => {
  const mockLogin = jest.fn()
  const mockItems = [
    { itemId: '1', description: 'Test item 1' },
    { itemId: '2', description: 'Test item 2' }
  ]

  beforeEach(() => {
    jest.clearAllMocks()
    ;(useAuth as jest.Mock).mockReturnValue({
      isAuthenticated: true,
      login: mockLogin
    })
    ;(getWardrobeItems as jest.Mock).mockResolvedValue(mockItems)
  })

  it('should render login prompt when not authenticated', () => {
    ;(useAuth as jest.Mock).mockReturnValue({
      isAuthenticated: false,
      login: mockLogin
    })

    render(<WardrobeSection />)
    
    expect(screen.getByText('Please log in to manage your wardrobe.')).toBeInTheDocument()
    expect(screen.getByText('Log in')).toBeInTheDocument()
  })

  it('should load and display wardrobe items when authenticated', async () => {
    render(<WardrobeSection />)

    await waitFor(() => {
      expect(screen.getByText('Test item 1')).toBeInTheDocument()
      expect(screen.getByText('Test item 2')).toBeInTheDocument()
    })
  })

  it('should show empty state when no items are present', async () => {
    ;(getWardrobeItems as jest.Mock).mockResolvedValue([])

    render(<WardrobeSection />)

    await waitFor(() => {
      expect(screen.getByText('Your wardrobe is empty. Add some items to get started.')).toBeInTheDocument()
    })
  })

  it('should add a new item when form is submitted', async () => {
    const newItemId = '3'
    ;(addWardrobeItem as jest.Mock).mockResolvedValue(newItemId)

    render(<WardrobeSection />)

    const input = screen.getByPlaceholderText('Add a clothing item (e.g., brown sweatshirt)')
    const addButton = screen.getByRole('button', { name: '' }) // The Plus icon button

    fireEvent.change(input, { target: { value: 'New item' } })
    fireEvent.click(addButton)

    await waitFor(() => {
      expect(addWardrobeItem).toHaveBeenCalledWith('New item')
    })
  })

  it('should delete an item when delete button is clicked', async () => {
    render(<WardrobeSection />)

    await waitFor(() => {
      expect(screen.getByText('Test item 1')).toBeInTheDocument()
    })

    const deleteButtons = screen.getAllByRole('button', { name: '' }) // The Trash2 icon buttons
    const firstDeleteButton = deleteButtons[1] // The first delete button (index 1 because index 0 is the add button)
    fireEvent.click(firstDeleteButton)

    await waitFor(() => {
      expect(deleteWardrobeItem).toHaveBeenCalledWith('1')
    })
  })

  it('should handle errors when loading items fails', async () => {
    const consoleError = jest.spyOn(console, 'error').mockImplementation(() => {})
    ;(getWardrobeItems as jest.Mock).mockRejectedValue(new Error('Failed to load items'))

    render(<WardrobeSection />)

    await waitFor(() => {
      expect(consoleError).toHaveBeenCalled()
    })

    consoleError.mockRestore()
  })

  it('should handle errors when adding item fails', async () => {
    const consoleError = jest.spyOn(console, 'error').mockImplementation(() => {})
    ;(addWardrobeItem as jest.Mock).mockRejectedValue(new Error('Failed to add item'))

    render(<WardrobeSection />)

    const input = screen.getByPlaceholderText('Add a clothing item (e.g., brown sweatshirt)')
    const addButton = screen.getByRole('button', { name: '' })

    fireEvent.change(input, { target: { value: 'New item' } })
    fireEvent.click(addButton)

    await waitFor(() => {
      expect(consoleError).toHaveBeenCalled()
    })

    consoleError.mockRestore()
  })

  it('should handle errors when deleting item fails', async () => {
    const consoleError = jest.spyOn(console, 'error').mockImplementation(() => {})
    ;(deleteWardrobeItem as jest.Mock).mockRejectedValue(new Error('Failed to delete item'))

    render(<WardrobeSection />)

    await waitFor(() => {
      expect(screen.getByText('Test item 1')).toBeInTheDocument()
    })

    const deleteButtons = screen.getAllByRole('button', { name: '' })
    const firstDeleteButton = deleteButtons[1] // The first delete button (index 1 because index 0 is the add button)
    fireEvent.click(firstDeleteButton)

    await waitFor(() => {
      expect(consoleError).toHaveBeenCalled()
    })

    consoleError.mockRestore()
  })
}) 
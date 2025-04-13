import { render, screen } from '@testing-library/react'
import Home from '../Home'

describe('Home', () => {
  it('renders "Hello Dorian" text', () => {
    render(<Home />)
    const heading = screen.getByText(/Hello Dorian/i)
    expect(heading).toBeInTheDocument()
  })
}) 
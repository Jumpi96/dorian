import { render, screen } from '@testing-library/react'

describe('Example Test', () => {
  it('should pass a basic test', () => {
    expect(true).toBe(true)
  })

  it('should render a simple component', () => {
    render(<div>Hello, World!</div>)
    expect(screen.getByText('Hello, World!')).toBeInTheDocument()
  })
}) 
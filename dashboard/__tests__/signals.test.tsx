import { render, screen } from '@testing-library/react'
import Signals from '../pages/signals'

global.fetch = jest.fn(() =>
  Promise.resolve({ json: () => Promise.resolve([]) })
) as any

it('renders Signals heading', () => {
  render(<Signals />)
  expect(screen.getByText('Signals')).toBeInTheDocument()
})

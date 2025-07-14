import { render, screen } from '@testing-library/react'
import Home from '../pages/index'

jest.mock('../pages/index', () => {
  const actual = jest.requireActual('../pages/index')
  return {
    __esModule: true,
    default: actual.default,
  }
})

global.fetch = jest.fn(() =>
  Promise.resolve({ json: () => Promise.resolve([]) })
) as any

it('renders heading', async () => {
  render(<Home />)
  expect(screen.getByText('Live Positions')).toBeInTheDocument()
})

import type { NextApiRequest, NextApiResponse } from 'next'

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const positions = [
    { id: 1, symbol: 'AAPL', quantity: 10, price: 150 },
    { id: 2, symbol: 'GOOG', quantity: 5, price: 2800 },
  ]
  res.status(200).json(positions)
}

import type { NextApiRequest, NextApiResponse } from 'next'

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const now = Date.now()
  const signals = Array.from({ length: 10 }).map((_, i) => ({
    time: now - (9 - i) * 60000,
    confidence: Math.random(),
  }))
  res.status(200).json(signals)
}

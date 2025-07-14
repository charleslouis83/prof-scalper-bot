import type { NextApiRequest, NextApiResponse } from 'next'

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const metrics = {
    var: 0.12,
  }
  res.status(200).json(metrics)
}

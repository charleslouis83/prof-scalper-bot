import type { NextApiRequest, NextApiResponse } from 'next'

let config = `threshold: 0.5
maxRisk: 1000`

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'PATCH') {
    config = typeof req.body === 'string' ? req.body : config
    return res.status(200).end()
  }
  res.status(200).send(config)
}

import { useEffect, useState } from 'react'
import Head from 'next/head'

interface Position {
  id: number
  symbol: string
  quantity: number
  price: number
}

export default function Home() {
  const [positions, setPositions] = useState<Position[]>([])

  useEffect(() => {
    fetch('/api/positions')
      .then(res => res.json())
      .then(setPositions)
      .catch(() => {})

    const ws = new WebSocket('ws://localhost:3001')
    ws.onmessage = evt => {
      try {
        const data = JSON.parse(evt.data)
        if (Array.isArray(data)) {
          setPositions(data)
        }
      } catch (err) {
        console.error(err)
      }
    }
    return () => ws.close()
  }, [])

  return (
    <div className="p-8">
      <Head>
        <title>Live Board</title>
      </Head>
      <h1 className="text-2xl font-bold mb-4">Live Positions</h1>
      <table className="min-w-full border border-gray-300">
        <thead>
          <tr>
            <th className="border px-2 py-1">Symbol</th>
            <th className="border px-2 py-1">Qty</th>
            <th className="border px-2 py-1">Price</th>
          </tr>
        </thead>
        <tbody>
          {positions.map((p) => (
            <tr key={p.id}>
              <td className="border px-2 py-1">{p.symbol}</td>
              <td className="border px-2 py-1">{p.quantity}</td>
              <td className="border px-2 py-1">{p.price}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

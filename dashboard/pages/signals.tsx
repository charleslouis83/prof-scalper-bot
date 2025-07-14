import { useEffect, useState } from 'react'
import { Line } from 'react-chartjs-2'
import 'chart.js/auto'

interface Signal {
  time: number
  confidence: number
}

export default function Signals() {
  const [signals, setSignals] = useState<Signal[]>([])

  useEffect(() => {
    fetch('/api/signals')
      .then(res => res.json())
      .then(setSignals)
      .catch(() => {})
  }, [])

  const chartData = {
    labels: signals.map(s => new Date(s.time).toLocaleTimeString()),
    datasets: [
      {
        label: 'Confidence',
        data: signals.map(s => s.confidence),
        borderColor: 'rgb(99, 102, 241)',
        backgroundColor: 'rgba(99, 102, 241, 0.5)',
      },
    ],
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Signals</h1>
      <Line data={chartData} />
    </div>
  )
}

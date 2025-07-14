import { useEffect, useState } from 'react'
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar'
import 'react-circular-progressbar/dist/styles.css'

export default function Risk() {
  const [varValue, setVarValue] = useState(0)

  useEffect(() => {
    fetch('/api/metrics')
      .then(res => res.json())
      .then(data => setVarValue(data.var || 0))
      .catch(() => {})
  }, [])

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Risk</h1>
      <div style={{ width: 200 }}>
        <CircularProgressbar
          value={varValue * 100}
          text={`${(varValue * 100).toFixed(1)}%`}
          maxValue={100}
          styles={buildStyles({ pathColor: '#dc2626', textColor: '#000' })}
        />
      </div>
    </div>
  )
}

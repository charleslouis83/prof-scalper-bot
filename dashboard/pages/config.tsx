import { useEffect, useState } from 'react'

export default function Config() {
  const [yaml, setYaml] = useState('')

  useEffect(() => {
    fetch('/api/config')
      .then(res => res.text())
      .then(setYaml)
      .catch(() => {})
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await fetch('/api/config', { method: 'PATCH', body: yaml })
    alert('Saved')
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Config</h1>
      <form onSubmit={handleSubmit} className="flex flex-col space-y-4 max-w-xl">
        <textarea
          className="border p-2 font-mono h-48"
          value={yaml}
          onChange={e => setYaml(e.target.value)}
        />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          Save
        </button>
      </form>
    </div>
  )
}

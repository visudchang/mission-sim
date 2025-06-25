import { useEffect } from 'react'

export default function TimeControls({ missionTime, setMissionTime, setTimeScale }) {
  useEffect(() => {
    setMissionTime(0)
  }, [])

  const formatMissionTime = (seconds) => {
    const totalSeconds = Math.floor(seconds)
    const hrs = Math.floor(totalSeconds / 3600)
    const mins = Math.floor((totalSeconds % 3600) / 60)
    const secs = totalSeconds % 60

    const pad = (n) => String(n).padStart(2, '0')
    return `T+${pad(hrs)}:${pad(mins)}:${pad(secs)}`
  }

  return (
    <div className="bg-zinc-900 p-3 rounded-lg shadow-lg text-sm space-y-2 border border-zinc-700">
      <div className="flex justify-between items-center">
        <h2 className="text-md font-semibold text-blue-300">Mission Time</h2>
        <span className="font-mono text-gray-300">{formatMissionTime(missionTime)}</span>
      </div>

      <div className="flex justify-between space-x-2">
        <button onClick={() => setTimeScale(0)} className="bg-slate-700 hover:bg-slate-600 text-white px-3 py-1 rounded">⏸ Pause</button>
        <button onClick={() => setTimeScale(1)} className="bg-slate-700 hover:bg-slate-600 text-white px-3 py-1 rounded">▶️ 1x</button>
        <button onClick={() => setTimeScale(10)} className="bg-slate-700 hover:bg-slate-600 text-white px-3 py-1 rounded">⏩ 10x</button>
        <button onClick={() => setTimeScale(100)} className="bg-slate-700 hover:bg-slate-600 text-white px-3 py-1 rounded">🚀 100x</button>
        <button onClick={() => setTimeScale(1000)} className="bg-slate-700 hover:bg-slate-600 text-white px-3 py-1 rounded">💥 1000x</button>
      </div>
    </div>
  )
}

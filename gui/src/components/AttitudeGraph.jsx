import { useEffect, useRef, useState } from "react"

export default function AttitudeGraph() {
  const [data, setData] = useState({ pitch: [], yaw: [], roll: [] })
  const tRef = useRef(0)

  useEffect(() => {
    const interval = setInterval(() => {
      tRef.current += 0.02

      const pitch = 20 + 5 * Math.sin(tRef.current)
      const yaw = 25 + 3 * Math.cos(tRef.current / 2)
      const roll = 15 + 2 * Math.sin(tRef.current / 3 + 1)

      setData(prev => {
        const maxPoints = 50
        return {
          pitch: [...prev.pitch, pitch].slice(-maxPoints),
          yaw: [...prev.yaw, yaw].slice(-maxPoints),
          roll: [...prev.roll, roll].slice(-maxPoints),
        }
      })
    }, 100)

    return () => clearInterval(interval)
  }, [])

  const makePoints = (values) =>
    values.map((v, i) => `${(i * 2)},${40 - v}`).join(" ")

  return (
    <div className="bg-zinc-800 p-4 rounded-lg shadow-lg h-76">
      <h2 className="text-md font-semibold text-blue-300 mb-2">Pitch / Yaw / Roll</h2>
      <svg className="w-full h-[80%] bg-zinc-900 rounded" viewBox="0 0 100 40">
        <polyline fill="none" stroke="#93c5fd" strokeWidth="0.5" points={makePoints(data.pitch)} />
        <polyline fill="none" stroke="#a5f3fc" strokeWidth="0.5" points={makePoints(data.yaw)} />
        <polyline fill="none" stroke="#e2e8f0" strokeWidth="0.5" points={makePoints(data.roll)} />
      </svg>
    </div>
  )
}

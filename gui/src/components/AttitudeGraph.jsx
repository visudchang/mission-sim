export default function AttitudeGraph() {
  return (
    <div className="bg-zinc-800 p-4 rounded-lg shadow-lg h-48">
      <h2 className="text-lg font-semibold text-indigo-400 mb-2">Pitch / Yaw / Roll</h2>

      <svg className="w-full h-full bg-zinc-900 rounded" viewBox="0 0 100 40">
        <polyline
          fill="none"
          stroke="lime"
          strokeWidth="0.5"
          points="0,20 10,22 20,18 30,25 40,19 50,21 60,23 70,20 80,18 90,19 100,21"
        />
        <polyline
          fill="none"
          stroke="cyan"
          strokeWidth="0.5"
          points="0,25 10,23 20,24 30,26 40,22 50,27 60,25 70,26 80,24 90,23 100,25"
        />
        <polyline
          fill="none"
          stroke="orange"
          strokeWidth="0.5"
          points="0,15 10,14 20,16 30,13 40,14 50,16 60,14 70,15 80,16 90,17 100,15"
        />
      </svg>
    </div>
  )
}

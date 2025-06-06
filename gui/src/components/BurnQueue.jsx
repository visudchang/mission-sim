export default function BurnQueue() {
  const dummyBurns = [
    {
      tPlus: 'T+00:05',
      vector: [10, 0, 0],
      magnitude: '10.0 km/s',
    },
    {
      tPlus: 'T+00:45',
      vector: [5, 5, 0],
      magnitude: '7.1 km/s',
    },
    {
      tPlus: 'T+01:30',
      vector: [-2, 3, 4],
      magnitude: '5.4 km/s',
    },
  ]

  return (
    <div className="bg-zinc-900 p-4 rounded-lg shadow-lg border border-zinc-700 text-sm">
      <h2 className="text-md font-semibold text-blue-300 mb-3">Burn Queue</h2>
      <div className="font-mono text-gray-300 space-y-2">
        {dummyBurns.map((burn, idx) => (
          <div key={idx} className="bg-zinc-800 px-3 py-2 rounded border border-zinc-700">
            <div className="flex justify-between">
              <span>{burn.tPlus}</span>
              <span>{burn.magnitude}</span>
            </div>
            <div className="text-xs text-blue-200 mt-1">
              Δv = [{burn.vector.join(', ')}] km/s
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

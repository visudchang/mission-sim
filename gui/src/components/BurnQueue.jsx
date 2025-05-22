export default function BurnQueue() {
  const dummyBurns = [
    { time: 'T+00:05', dv: '25 m/s', direction: 'Prograde' },
    { time: 'T+00:45', dv: '12 m/s', direction: 'Normal' },
    { time: 'T+01:30', dv: '40 m/s', direction: 'Radial Out' },
  ]

  return (
    <div className="bg-zinc-800 p-4 rounded-lg shadow-lg">
      <h2 className="text-lg font-semibold text-orange-400 mb-4">Burn Queue</h2>

      <div className="text-sm font-mono text-gray-200 space-y-2">
        {dummyBurns.map((burn, idx) => (
          <div
            key={idx}
            className="flex justify-between bg-zinc-900 px-3 py-2 rounded border border-zinc-700"
          >
            <span>{burn.time}</span>
            <span>{burn.dv}</span>
            <span>{burn.direction}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

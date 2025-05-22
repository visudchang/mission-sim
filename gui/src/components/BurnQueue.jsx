export default function BurnQueue() {
  const dummyBurns = [
    { time: 'T+00:05', dv: '25 m/s', direction: 'Prograde' },
    { time: 'T+00:45', dv: '12 m/s', direction: 'Normal' },
    { time: 'T+01:30', dv: '40 m/s', direction: 'Radial Out' },
  ]

  return (
    <div className="bg-zinc-900 p-4 rounded-lg shadow-lg border border-zinc-700 text-sm">
      <h2 className="text-md font-semibold text-blue-300 mb-3">Burn Queue</h2>
      <div className="font-mono text-gray-300 space-y-2">
        {dummyBurns.map((burn, idx) => (
          <div key={idx} className="flex justify-between bg-zinc-800 px-3 py-2 rounded border border-zinc-700">
            <span>{burn.time}</span>
            <span>{burn.dv}</span>
            <span>{burn.direction}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

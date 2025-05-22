export default function MissionLog() {
  const logs = [
    '[T+00:00] Mission initialized.',
    '[T+00:02] Systems nominal.',
    '[T+00:05] Burn executed: Δv = 25 m/s, Direction = Prograde.',
    '[T+00:15] Altitude stable at 410 km.',
    '[T+00:30] Preparing for orbit circularization burn.',
  ]

  return (
    <div className="bg-zinc-900 p-4 rounded-lg shadow-lg h-48 overflow-y-auto border border-zinc-700 text-sm">
      <h2 className="text-md font-semibold text-blue-300 mb-2">Mission Log</h2>
      <div className="font-mono text-gray-300 space-y-1">
        {logs.map((line, idx) => (
          <div key={idx} className="bg-zinc-800 px-2 py-1 rounded border border-zinc-700">
            {line}
          </div>
        ))}
      </div>
    </div>
  )
}

export default function MissionLog() {
  const logs = [
    '[T+00:00] Mission initialized.',
    '[T+00:02] Systems nominal.',
    '[T+00:05] Burn executed: Δv = 25 m/s, Direction = Prograde.',
    '[T+00:15] Altitude stable at 410 km.',
    '[T+00:30] Preparing for orbit circularization burn.',
  ]

  return (
    <div className="bg-zinc-800 p-4 rounded-lg shadow-lg h-48 overflow-y-auto">
      <h2 className="text-lg font-semibold text-yellow-400 mb-2">Mission Log</h2>

      <div className="text-sm font-mono text-gray-300 space-y-1">
        {logs.map((line, idx) => (
          <div key={idx} className="bg-zinc-900 px-2 py-1 rounded">
            {line}
          </div>
        ))}
      </div>
    </div>
  )
}

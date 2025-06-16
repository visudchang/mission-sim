export default function TelemetryPanel({ telemetry }) {
  return (
    <div className="bg-zinc-900 p-4 rounded-lg shadow-lg border border-zinc-700 text-sm">
      <h2 className="text-md font-semibold text-blue-300 mb-2">Telemetry</h2>
      <div className="space-y-2">
        <div className="flex justify-between text-gray-400">
          <span>Battery:</span>
          <span className="font-mono text-white">{(telemetry.BAT ?? 0).toFixed(2)}%</span>
        </div>
        <div className="flex justify-between text-gray-400">
          <span>Temperature:</span>
          <span className="font-mono text-white">{(telemetry.TEMP ?? 25).toFixed(2)} °C</span>
        </div>
        <div className="flex justify-between text-gray-400">
          <span>Altitude:</span>
          <span className="font-mono text-white">{(telemetry.ALT ?? 0).toFixed(2)} km</span>
        </div>
      </div>
    </div>
  )
}

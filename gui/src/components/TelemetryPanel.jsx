export default function TelemetryPanel() {
  // Dummy values for now
  const telemetry = {
    BAT: 94,
    TEMP: 36.5,
    ALT: 412.2
  };

  return (
    <div className="bg-zinc-800 p-4 rounded-lg shadow-lg">
      <h2 className="text-xl font-bold mb-4 text-blue-400">Telemetry</h2>
      <div className="space-y-2">
        <div className="flex justify-between">
          <span className="text-gray-400">Battery:</span>
          <span className="font-mono text-green-400">{telemetry.BAT}%</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-400">Temperature:</span>
          <span className="font-mono text-yellow-300">{telemetry.TEMP} °C</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-400">Altitude:</span>
          <span className="font-mono text-cyan-300">{telemetry.ALT} m</span>
        </div>
      </div>
    </div>
  );
}

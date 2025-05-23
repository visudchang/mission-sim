export default function FlightDataPanel() {
  const data = {
    pitch: '-2.3°',
    yaw: '14.1°',
    roll: '1.5°',
    velocity: '7.62 km/s',
    acceleration: '0.002 m/s²',
  }

  return (
    <div className="bg-zinc-900 p-4 rounded-lg shadow-lg border border-zinc-700 text-sm space-y-2">
      <h2 className="text-md font-semibold text-blue-300 mb-1">Flight Data</h2>

      <div className="text-gray-400 font-mono space-y-1">
        <div className="flex justify-between">
          <span>Pitch:</span>
          <span className="text-white">{data.pitch}</span>
        </div>
        <div className="flex justify-between">
          <span>Yaw:</span>
          <span className="text-white">{data.yaw}</span>
        </div>
        <div className="flex justify-between">
          <span>Roll:</span>
          <span className="text-white">{data.roll}</span>
        </div>
        <div className="flex justify-between pt-2">
          <span>Velocity:</span>
          <span className="text-white">{data.velocity}</span>
        </div>
        <div className="flex justify-between">
          <span>Acceleration:</span>
          <span className="text-white">{data.acceleration}</span>
        </div>
      </div>
    </div>
  )
}

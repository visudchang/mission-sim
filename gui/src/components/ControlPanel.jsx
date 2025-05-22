export default function ControlPanel() {
  return (
    <div className="bg-zinc-800 p-4 rounded-lg shadow-lg">
      <h2 className="text-lg font-semibold text-emerald-400 mb-4">Control Panel</h2>

      <div className="space-y-4">
        {/* Burn input */}
        <div>
          <label className="block text-sm text-gray-300 mb-1" htmlFor="burn">
            Burn Δv (m/s)
          </label>
          <input
            id="burn"
            type="number"
            placeholder="Enter delta-v"
            className="w-full px-3 py-2 bg-zinc-900 text-white border border-zinc-700 rounded focus:outline-none focus:ring-2 focus:ring-emerald-500"
          />
        </div>

        {/* Buttons */}
        <div className="flex flex-col space-y-2">
          <button className="bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-2 px-4 rounded">
            Execute Burn
          </button>
          <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded">
            Set Orbit
          </button>
          <button className="bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded">
            Stop Thrusters
          </button>
        </div>
      </div>
    </div>
  )
}

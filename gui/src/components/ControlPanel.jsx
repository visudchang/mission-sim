export default function ControlPanel() {
  return (
    <div className="bg-zinc-900 p-3 rounded-lg shadow-lg border border-zinc-700 text-sm space-y-3">
      <h2 className="text-md font-semibold text-blue-300">Control Panel</h2>

      <div>
        <label className="block text-gray-400 mb-1" htmlFor="burn">
          Burn Δv (m/s)
        </label>
        <input
          id="burn"
          type="number"
          placeholder="e.g. 42"
          className="w-full px-2 py-1 bg-zinc-800 text-white border border-zinc-700 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 text-sm"
        />
      </div>

      <div className="flex flex-col space-y-1">
        <button className="bg-slate-700 hover:bg-slate-600 text-white py-1 rounded">Execute Burn</button>
        <button className="bg-slate-700 hover:bg-slate-600 text-white py-1 rounded">Set Orbit</button>
        <button className="bg-slate-700 hover:bg-slate-600 text-white py-1 rounded">Stop Thrusters</button>
      </div>
    </div>
  )
}

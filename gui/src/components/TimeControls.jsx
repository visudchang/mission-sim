export default function TimeControls() {
  return (
    <div className="bg-zinc-900 p-3 rounded-lg shadow-lg text-sm space-y-2 border border-zinc-700">
      {/* Top line: title + mission time */}
      <div className="flex justify-between items-center">
        <h2 className="text-md font-semibold text-blue-300">Mission Time</h2>
        <span className="font-mono text-gray-300">T+00:42</span>
      </div>

      {/* Bottom line: buttons */}
      <div className="flex justify-between space-x-2">
        <button className="bg-slate-700 hover:bg-slate-600 text-white px-3 py-1 rounded">
          ⏸ Pause
        </button>
        <button className="bg-slate-700 hover:bg-slate-600 text-white px-3 py-1 rounded">
          ▶️ 1x
        </button>
        <button className="bg-slate-700 hover:bg-slate-600 text-white px-3 py-1 rounded">
          ⏩ 5x
        </button>
        <button className="bg-slate-700 hover:bg-slate-600 text-white px-3 py-1 rounded">
          🚀 10x
        </button>
      </div>
    </div>
  )
}

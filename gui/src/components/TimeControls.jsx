export default function TimeControls() {
  return (
    <div className="bg-zinc-800 p-4 rounded-lg shadow-lg flex justify-between items-center">
      <h2 className="text-lg font-semibold text-blue-400">Mission Time</h2>

      <div className="space-x-2 flex items-center">
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm">
          ⏸ Pause
        </button>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm">
          ▶️ 1x
        </button>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm">
          ⏩ 5x
        </button>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm">
          🚀 10x
        </button>
        <span className="ml-4 text-sm font-mono text-gray-300">
          T+00:42
        </span>
      </div>
    </div>
  )
}

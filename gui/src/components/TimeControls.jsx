export default function TimeControls() {
  return (
    <div className="bg-zinc-800 p-4 rounded-lg flex justify-between items-center">
      <h2 className="text-lg font-semibold">Mission Time</h2>
      <div className="space-x-2">
        <button className="bg-blue-600 px-3 py-1 rounded">⏸ Pause</button>
        <button className="bg-blue-600 px-3 py-1 rounded">▶️ 1x</button>
        <button className="bg-blue-600 px-3 py-1 rounded">⏩ 5x</button>
        <button className="bg-blue-600 px-3 py-1 rounded">🚀 10x</button>
      </div>
    </div>
  );
}

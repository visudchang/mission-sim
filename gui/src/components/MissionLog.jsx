export default function MissionLog({ logs }) {
 
  return (
    <div className="bg-zinc-900 p-4 rounded-lg shadow-lg h-52.5 overflow-y-auto border border-zinc-700 text-sm">
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

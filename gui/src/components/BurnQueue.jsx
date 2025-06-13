export default function BurnQueue({ burnQueue = [] }) {
  return (
    <div className="bg-zinc-900 p-4 rounded-lg shadow-lg border border-zinc-700 text-sm">
      <h2 className="text-md font-semibold text-blue-300 mb-3">Burn Queue</h2>

      {burnQueue.length === 0 ? (
        <p className="text-gray-500 font-mono">No upcoming burns.</p>
      ) : (
        <div className="font-mono text-gray-300 space-y-2">
          {burnQueue.map((burn, idx) => (
            <div
              key={idx}
              className="bg-zinc-800 px-3 py-2 rounded border border-zinc-700"
            >
              <div className="flex justify-between">
                <span>{burn.tPlus ?? 'T+??:??'}</span>
                <span>{burn.magnitude ?? '?.? km/s'}</span>
              </div>
              <div className="text-xs text-blue-200 mt-1">
                Δv = [{(burn.vector ?? []).join(', ')}] km/s
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

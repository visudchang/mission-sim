export default function MissionLog({ logs }) {
  const formatTPlus = (tPlusStr) => {
    if (!tPlusStr || typeof tPlusStr !== 'string') return 'T+??:??';

    const cleaned = tPlusStr.startsWith('T+') ? tPlusStr.slice(2) : tPlusStr;
    const parts = cleaned.split(':');
    if (parts.length !== 2) return 'T+??:??';

    const mm = Number(parts[0]);
    const ss = Number(parts[1]);
    if (isNaN(mm) || isNaN(ss)) return 'T+??:??';

    const totalSeconds = mm * 60 + ss;
    const hrs = Math.floor(totalSeconds / 3600);
    const mins = Math.floor((totalSeconds % 3600) / 60);
    const secs = totalSeconds % 60;

    const pad = (n) => String(n).padStart(2, '0');
    return `T+${pad(hrs)}:${pad(mins)}:${pad(secs)}`;
  };

  const formatLogLine = (line) => {
    const timeMatch = line.match(/T\+\d+:\d+/);
    if (!timeMatch) return line; 

    const original = timeMatch[0];
    const formatted = formatTPlus(original);
    return line.replace(original, formatted);
  };

  return (
    <div className="bg-zinc-900 p-4 rounded-lg shadow-lg h-52.5 overflow-y-auto border border-zinc-700 text-sm">
      <h2 className="text-md font-semibold text-blue-300 mb-2">Mission Log</h2>
      <div className="font-mono text-gray-300 space-y-1">
        {logs.map((line, idx) => (
          <div key={idx} className="bg-zinc-800 px-2 py-1 rounded border border-zinc-700">
            {formatLogLine(line)}
          </div>
        ))}
      </div>
    </div>
  );
}

import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function DynamicsGraph({ velocityHistory, missionTime }) {
  return (
    <div className="bg-zinc-800 p-4 rounded-lg shadow-lg h-76">
      <h2 className="text-md font-semibold text-blue-300 mb-2">Velocity</h2>

      <div className="relative left-[-12px] top-[20px]"> {}
        <ResponsiveContainer width="100%" height={220}>
          <LineChart data={velocityHistory}>
            <XAxis
              dataKey="time"
              stroke="#aaa"
              tick={{ fontSize: 10 }}
              type="number"
              domain={[Math.max(0, missionTime - 30000), missionTime]}
              minTickGap={10}
              tickFormatter={(t) =>
                missionTime < 1000 ? `T+${t.toFixed(0)}s` : `T+${Math.floor(t / 100) * 100}s`
              }
            />
            <YAxis
              allowDataOverflow={true}
              stroke="#aaa"
              domain={[0, 12]}
              tickFormatter={(v) => `${v.toFixed(1)}`}
              tick={{ fontSize: 10 }}
              unit=" km/s"
            />
            <Tooltip
              formatter={(value) => `${value.toFixed(2)} km/s`}
              labelFormatter={(label) => `T+${Math.floor(label)}s`}
            />
            <Line
              type="monotone"
              dataKey="velocity"
              stroke="#38bdf8"
              strokeWidth={2}
              dot={false}
              isAnimationActive={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>

  );
}

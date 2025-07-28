import { useEffect, useRef, useState } from "react";

export default function AttitudeGraph({ pitch, yaw, roll }) {
  const [data, setData] = useState({ pitch: [], roll: [], yaw: [] });
  const latestRef = useRef({ pitch: 0, roll: 0, yaw: 0 });

  const maxPoints = 50;
  const graphHeight = 40;
  const graphWidth = 100;
  const yAxisMargin = 11;

  const scaleValue = (v, min, max, height) => {
    const clamped = Math.max(min, Math.min(max, v));
    return height - ((clamped - min) / (max - min)) * height;
  };

  const makePoints = (values) =>
    values.map((v, i) => `${yAxisMargin + i * 2},${v}`).join(" ");

  useEffect(() => {
    latestRef.current = { pitch, roll, yaw };
  }, [pitch, roll, yaw]);

  useEffect(() => {
    const interval = setInterval(() => {
      const latest = latestRef.current;
      setData(prev => ({
        pitch: [...prev.pitch, scaleValue(latest.pitch, -185, 185, graphHeight)].slice(-maxPoints),
        roll: [...prev.roll, scaleValue(latest.roll, -185, 185, graphHeight)].slice(-maxPoints),
        yaw:   [...prev.yaw, scaleValue(latest.yaw, -185, 185, graphHeight)].slice(-maxPoints),
      }));
    }, 100);

    return () => clearInterval(interval);
  }, []);

  const yTicks = [-180, -90, 0, 90, 180];
  const scaledY = yTicks.map(y =>
    ({
      y: scaleValue(y, -185, 185, graphHeight),
      label: y
    })
  );

  return (
    <div className="bg-zinc-800 p-4 rounded-lg shadow-lg h-76 relative">
      <h2 className="text-md font-semibold text-blue-300 mb-2">Pitch / Roll / Yaw</h2>

      {/* Legend */}
      <div className="absolute top-5 right-4 text-xs text-gray-300 space-x-2 font-sans">
        <span className="text-[#93c5fd]">■ Pitch</span>
        <span className="text-[#e2e8f0]">■ Roll</span>
        <span className="text-[#a5f3fc]">■ Yaw</span>
      </div>

      <svg
        className="w-full h-[80%] bg-zinc-900 rounded"
        viewBox={`0 0 ${graphWidth + yAxisMargin} ${graphHeight}`}
      >
        {/* Y-axis ticks on the left, outside graph */}
        {scaledY.map(({ y, label }, idx) => (
          <g key={idx}>
            <line x1={yAxisMargin - 4} y1={y} x2={yAxisMargin - 1} y2={y} stroke="#888" strokeWidth="0.3" />
            <text x={4} y={y + 1} textAnchor="middle" fontSize="2.5" fill="#888">{label} </text>
          </g>
        ))}

        {/* PRY Lines */}
        <polyline fill="none" stroke="#93c5fd" strokeWidth="0.5" points={makePoints(data.pitch)} />
        <polyline fill="none" stroke="#e2e8f0" strokeWidth="0.5" points={makePoints(data.roll)} />
        <polyline fill="none" stroke="#a5f3fc" strokeWidth="0.5" points={makePoints(data.yaw)} />
      </svg>
    </div>
  );
}

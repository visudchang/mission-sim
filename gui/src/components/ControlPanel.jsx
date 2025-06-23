import { useState, useEffect, useRef } from 'react';

export default function ControlPanel({ missionTime, setMissionTime, onReset }) {
  const [dvX, setDvX] = useState(0.1);
  const [dvY, setDvY] = useState(0);
  const [dvZ, setDvZ] = useState(0);
  const [rp, setRp] = useState(6678);
  const [ra, setRa] = useState(6678);
  const [inclination, setInclination] = useState(28.5);
  const socketRef = useRef(null);

  useEffect(() => {
    socketRef.current = new WebSocket('ws://localhost:8765');
    socketRef.current.onopen = () => console.log('[ControlPanel] WebSocket connected');
    socketRef.current.onclose = () => console.log('[ControlPanel] WebSocket disconnected');
    socketRef.current.onerror = (err) => console.error('[ControlPanel] WebSocket error:', err);
    return () => socketRef.current.close();
  }, []);

  const handleExecuteBurn = () => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      const message = `BURN:${dvX},${dvY},${dvZ},${missionTime.toFixed(2)}`;
      socketRef.current.send(message);
      console.log('[ControlPanel] Sent:', message);
    }
  };

  const handleSetOrbit = () => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      const message = `SET_ORBIT:${rp},${ra},${inclination}`;
      socketRef.current.send(message);
      console.log('[ControlPanel] Sent:', message);
    }
  };

  const inputClass = "w-full px-1 py-1 bg-zinc-800 text-white border border-zinc-700 rounded text-xs";

  return (
    <div className="bg-zinc-900 p-3 rounded-lg shadow-lg border border-zinc-700 text-sm space-y-1">
      <h2 className="text-md font-semibold text-blue-300 mb-1">Control Panel</h2>

      {/* Δv Inputs + Burn Button */}
      <div className="space-y-1">
        <div className="grid grid-cols-3 gap-2">
          <div>
            <label htmlFor="dvX" className="text-gray-400 text-xs">Δv X (km/s)</label>
            <input id="dvX" type="number" value={dvX} onChange={e => setDvX(parseFloat(e.target.value))} className={inputClass} />
          </div>
          <div>
            <label htmlFor="dvY" className="text-gray-400 text-xs">Δv Y (km/s)</label>
            <input id="dvY" type="number" value={dvY} onChange={e => setDvY(parseFloat(e.target.value))} className={inputClass} />
          </div>
          <div>
            <label htmlFor="dvZ" className="text-gray-400 text-xs">Δv Z (km/s)</label>
            <input id="dvZ" type="number" value={dvZ} onChange={e => setDvZ(parseFloat(e.target.value))} className={inputClass} />
          </div>
        </div>
        <button onClick={handleExecuteBurn} className="w-full bg-slate-700 hover:bg-slate-600 text-white py-1.5 rounded text-sm mt-1">Execute Burn</button>
      </div>

      {/* Orbit Inputs + Set Orbit Button */}
      <div className="space-y-1">
        <div className="grid grid-cols-3 gap-2">
          <div>
            <label htmlFor="rp" className="text-gray-400 text-xs">Periapsis (km)</label>
            <input id="rp" type="number" value={rp} onChange={e => setRp(parseFloat(e.target.value))} className={inputClass} />
          </div>
          <div>
            <label htmlFor="ra" className="text-gray-400 text-xs">Apoapsis (km)</label>
            <input id="ra" type="number" value={ra} onChange={e => setRa(parseFloat(e.target.value))} className={inputClass} />
          </div>
          <div>
            <label htmlFor="inclination" className="text-gray-400 text-xs">Inclination (°)</label>
            <input id="inclination" type="number" value={inclination} onChange={e => setInclination(parseFloat(e.target.value))} className={inputClass} />
          </div>
        </div>
        <button onClick={handleSetOrbit} className="w-full bg-slate-700 hover:bg-slate-600 text-white py-1.5 rounded text-sm mt-1">Set Orbit</button>
      </div>

      {/* Reset Button */}
      <button onClick={onReset} className="w-full bg-slate-700 hover:bg-slate-600 text-white py-1.5 rounded text-sm">Reset Mission</button>
    </div>
  );
}

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

    socketRef.current.onopen = () => {
      console.log('[ControlPanel] WebSocket connected');
    };

    socketRef.current.onclose = () => {
      console.log('[ControlPanel] WebSocket disconnected');
    };

    socketRef.current.onerror = (err) => {
      console.error('[ControlPanel] WebSocket error:', err);
    };

    return () => {
      socketRef.current.close();
    };
  }, []);

  const handleExecuteBurn = () => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      const message = `BURN:${dvX},${dvY},${dvZ},${missionTime.toFixed(2)}`;
      socketRef.current.send(message);
      console.log('[ControlPanel] Sent:', message);
    } else {
      console.warn('[ControlPanel] WebSocket not ready');
    }
  };

  const handleSetOrbit = () => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      const message = `SET_ORBIT:${rp},${ra},${inclination}`;
      socketRef.current.send(message);
      console.log('[ControlPanel] Sent:', message);
    } else {
      console.warn('[ControlPanel] WebSocket not ready');
    }
  };

  return (
    <div className="bg-zinc-900 p-3 rounded-lg shadow-lg border border-zinc-700 text-sm space-y-4">
      <h2 className="text-md font-semibold text-blue-300">Control Panel</h2>

      <div className="grid grid-cols-3 gap-2">
        <div>
          <label className="block text-gray-400 mb-1" htmlFor="dvX">Δv X (km/s)</label>
          <input id="dvX" type="number" value={dvX} onChange={(e) => setDvX(parseFloat(e.target.value))}
            className="w-full px-2 py-1 bg-zinc-800 text-white border border-zinc-700 rounded text-sm" />
        </div>
        <div>
          <label className="block text-gray-400 mb-1" htmlFor="dvY">Δv Y (km/s)</label>
          <input id="dvY" type="number" value={dvY} onChange={(e) => setDvY(parseFloat(e.target.value))}
            className="w-full px-2 py-1 bg-zinc-800 text-white border border-zinc-700 rounded text-sm" />
        </div>
        <div>
          <label className="block text-gray-400 mb-1" htmlFor="dvZ">Δv Z (km/s)</label>
          <input id="dvZ" type="number" value={dvZ} onChange={(e) => setDvZ(parseFloat(e.target.value))}
            className="w-full px-2 py-1 bg-zinc-800 text-white border border-zinc-700 rounded text-sm" />
        </div>
      </div>

      <div className="space-y-2">
        <h3 className="text-gray-300 font-medium mt-2">Set Target Orbit</h3>
        <div className="grid grid-cols-3 gap-2">
          <div>
            <label className="block text-gray-400 mb-1" htmlFor="rp">Periapsis Radius (km)</label>
            <input id="rp" type="number" value={rp} onChange={(e) => setRp(parseFloat(e.target.value))}
              className="w-full px-2 py-1 bg-zinc-800 text-white border border-zinc-700 rounded text-sm" />
          </div>
          <div>
            <label className="block text-gray-400 mb-1" htmlFor="ra">Apoapsis Radius (km)</label>
            <input id="ra" type="number" value={ra} onChange={(e) => setRa(parseFloat(e.target.value))}
              className="w-full px-2 py-1 bg-zinc-800 text-white border border-zinc-700 rounded text-sm" />
          </div>
          <div>
            <label className="block text-gray-400 mb-1" htmlFor="inclination">Inclination (°)</label>
            <input id="inclination" type="number" value={inclination} onChange={(e) => setInclination(parseFloat(e.target.value))}
              className="w-full px-2 py-1 bg-zinc-800 text-white border border-zinc-700 rounded text-sm" />
          </div>
        </div>
      </div>

      <div className="flex flex-col space-y-1 mt-3">
        <button onClick={handleExecuteBurn}
          className="bg-slate-700 hover:bg-slate-600 text-white py-2 rounded">
          Execute Burn
        </button>
        <button onClick={handleSetOrbit}
          className="bg-slate-700 hover:bg-slate-600 text-white py-2 rounded">
          Set Orbit
        </button>
        <button onClick={onReset}
          className="bg-slate-700 hover:bg-slate-600 text-white py-2 rounded">
          Reset Mission
        </button>
      </div>
    </div>
  );
}

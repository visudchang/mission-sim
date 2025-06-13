import Header from './components/Header';
import TelemetryPanel from './components/TelemetryPanel';
import ControlPanel from './components/ControlPanel';
import OrbitDisplay from './components/OrbitDisplay';
import BurnQueue from './components/BurnQueue';
import MissionLog from './components/MissionLog';
import AttitudeGraph from './components/AttitudeGraph';
import DynamicsGraph from './components/DynamicsGraph';
import TimeControls from './components/TimeControls';
import FlightDataPanel from './components/FlightDataPanel';
import "tailwindcss";
import { useEffect, useState, useRef } from 'react';

function App() {
  const [telemetry, setTelemetry] = useState({ BAT: 0, TEMP: 0, ALT: 0, VEL: 0, orbital_energy: 0 });
  const [logEntries, setLogEntries] = useState([]);
  const [missionTime, setMissionTime] = useState(0);
  const [timeScale, setTimeScale] = useState(1);
  const [velocityHistory, setVelocityHistory] = useState([]);
  const lastUpdateRef = useRef(Date.now());

  const handleReset = async () => {
    try {
      const response = await fetch("http://localhost:5000/reset", {
        method: "POST"
      });
      const result = await response.json();
      console.log("[App] Reset result:", result);

      // Reset frontend time
      setMissionTime(0);
      lastUpdateRef.current = Date.now();  // <== IMPORTANT
    } catch (err) {
      console.error("[App] Reset failed:", err);
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      const elapsed = (now - lastUpdateRef.current) / 1000;
      lastUpdateRef.current = now;

      setMissionTime(prev => {
        const updated = prev + elapsed * timeScale;
        // console.log("[App] Advancing missionTime to:", updated.toFixed(2));
        fetch(`http://localhost:5000/propagate?missionTime=${updated}`)
          .then(res => res.json())
          .then(data => {
            setTelemetry({
              BAT: data.BAT,
              TEMP: data.TEMP,
              ALT: data.ALT,
              VEL: data.VEL,
              orbital_energy: data.orbital_energy
            });

            setVelocityHistory(prev => {
              const next = [
                ...prev,
                {
                  time: data.missionTime,
                  velocity: data.VEL
                }
              ];
              return next.filter(d => d.time >= Math.max(0, data.missionTime - 30000));
            });
            console.log("Velocity entry sample:", {
              time: data.missionTime,
              velocity: data.VEL
            });
          })
          .catch(err => console.error("[Telemetry Fetch Error]", err));
        return updated;
      });
    }, 1000 / 24); // Target ~24 FPS

    return () => clearInterval(interval);
  }, [timeScale]);

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8765');

    socket.onopen = () => {
      console.log('[Frontend] Connected to the WebSocket server');
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        setTelemetry({
          BAT: data.BAT,
          TEMP: data.TEMP,
          ALT: data.ALT,
          VEL: data.VEL,
          orbital_energy: data.orbital_energy,
          missionTime: data.missionTime
        });

        setLogEntries(prev => [
          `[BAT: ${data.BAT}% | TEMP: ${data.TEMP}°C | ALT: ${data.ALT}km | VEL: ${(data.VEL ?? 0).toFixed(2)} km/s | Orbital Energy: ${(data.orbital_energy ?? 0).toFixed(2)} MJ/kg]`,
          ...prev
        ].slice(0, 10));

      } catch (err) {
        console.error('[Frontend] Invalid telemetry:', err);
      }
    };

    socket.onerror = (err) => console.error('[Frontend] WebSocket error:', err);
    socket.onclose = () => console.log('[Frontend] WebSocket closed');

    return () => socket.close();
  }, []);

  return (
    <div className="min-h-screen w-screen bg-zinc-900 text-white p-4 space-y-4">
      <Header />
      <div className="grid grid-cols-4 gap-4 items-stretch">
        {/* Left column */}
        <div className="col-span-1 space-y-4">
          <TelemetryPanel telemetry={telemetry} />
          <ControlPanel missionTime={missionTime} setMissionTime={setMissionTime} onReset={handleReset} />
        </div>

        {/* Center visualization */}
        <div className="col-span-2">
          <OrbitDisplay missionTime={missionTime} timeScale={timeScale} />
        </div>

        {/* Right column */}
        <div className="col-span-1 space-y-4">
          <BurnQueue />
          <MissionLog logs={logEntries} />
        </div>
      </div>

      {/* Bottom row: Time Controls + Graphs */}
      <div className="grid grid-cols-12 gap-4 pt-4">
        <div className="col-span-3 space-y-2 flex flex-col justify-between">
          <FlightDataPanel velocity={telemetry.VEL || 0} orbital_energy={telemetry.orbital_energy || 0} />
          <TimeControls missionTime={missionTime} setMissionTime={setMissionTime} setTimeScale={setTimeScale} />
        </div>
        <div className="col-span-9 grid grid-cols-2 gap-4">
          <AttitudeGraph />
          <DynamicsGraph velocityHistory={velocityHistory} missionTime={missionTime} />
        </div>
      </div>
    </div>
  );
}

export default App;

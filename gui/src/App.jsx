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
import { useEffect, useState } from 'react';

function App() {
  const [telemetry, setTelemetry] = useState({ BAT: 0, TEMP: 0, ALT: 0 });
  const [logEntries, setLogEntries] = useState([]);

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
          ALT: data.ALT
        });

        setLogEntries(prev => [
          `[${new Date(data.timestamp).toLocaleTimeString()}] BAT: ${data.BAT}% TEMP: ${data.TEMP}°C ALT: ${data.ALT}km`,
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
          <ControlPanel />
        </div>

        {/* Center visualization */}
        <div className="col-span-2">
          <OrbitDisplay />
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
          <FlightDataPanel />
          <TimeControls />
        </div>
        <div className="col-span-9 grid grid-cols-2 gap-4">
          <AttitudeGraph />
          <DynamicsGraph />
        </div>
      </div>
    </div>
  );
}

export default App;

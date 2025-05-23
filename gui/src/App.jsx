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

function App() {
  return (
    <div className="min-h-screen w-screen bg-zinc-900 text-white p-4 space-y-4">
      <Header />
      <div className="grid grid-cols-4 gap-4 items-stretch">
        {/* Left column */}
        <div className="col-span-1 space-y-4">
          <TelemetryPanel />
          <ControlPanel />
        </div>

        {/* Center visualization */}
        <div className="col-span-2">
          <OrbitDisplay />
        </div>

        {/* Right column */}
        <div className="col-span-1 space-y-4">
          <BurnQueue />
          <MissionLog />
        </div>
      </div>

      {/* Bottom row: Time Controls + Graphs */}
      <div className="grid grid-cols-12 gap-4 pt-4">
        {/* Left column (stacked FlightData + TimeControls) */}
        <div className="col-span-3 space-y-2 flex flex-col justify-between">
          <FlightDataPanel />
          <TimeControls />
        </div>

        {/* Right two-thirds (graphs) */}
        <div className="col-span-9 grid grid-cols-2 gap-4">
          <AttitudeGraph />
          <DynamicsGraph />
        </div>
      </div>
    </div>
  );
}

export default App;

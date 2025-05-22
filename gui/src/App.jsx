import Header from './components/Header';
import TelemetryPanel from './components/TelemetryPanel';
import ControlPanel from './components/ControlPanel';
import OrbitDisplay from './components/OrbitDisplay';
import BurnQueue from './components/BurnQueue';
import MissionLog from './components/MissionLog';
import AttitudeGraph from './components/AttitudeGraph';
import DynamicsGraph from './components/DynamicsGraph';
import TimeControls from './components/TimeControls';

function App() {
  return (
    <div className="min-h-screen bg-zinc-900 text-white p-4 space-y-4">
      <Header />
      <div className="grid grid-cols-4 gap-4">
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

      {/* Bottom row: Graphs + Time Controls */}
      <div className="grid grid-cols-2 gap-4 pt-4">
        <AttitudeGraph />
        <DynamicsGraph />
      </div>
      <div className="pt-4">
        <TimeControls />
      </div>
    </div>
  );
}

export default App;

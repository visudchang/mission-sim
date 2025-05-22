export default function DynamicsGraph() {
  return (
    <div className="bg-zinc-800 p-4 rounded-lg shadow-lg h-48">
      <h2 className="text-lg font-semibold text-pink-400 mb-2">Velocity / Acceleration</h2>

      <svg className="w-full h-full bg-zinc-900 rounded" viewBox="0 0 100 40">
        <polyline
          fill="none"
          stroke="skyblue"
          strokeWidth="0.5"
          points="0,30 10,28 20,25 30,27 40,26 50,24 60,23 70,21 80,19 90,18 100,17"
        />
        <polyline
          fill="none"
          stroke="red"
          strokeWidth="0.5"
          points="0,20 10,19 20,21 30,20 40,22 50,23 60,22 70,21 80,20 90,19 100,20"
        />
      </svg>
    </div>
  )
}

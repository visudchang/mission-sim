import { Canvas, useFrame, useLoader } from '@react-three/fiber'
import { OrbitControls, Stars } from '@react-three/drei'
import { TextureLoader } from 'three/src/loaders/TextureLoader'
import { Suspense, useRef, useEffect, useState } from 'react'
import * as THREE from 'three'

const EARTH_RADIUS_KM = 6371

function Earth() {
  const texture = useLoader(TextureLoader, '/src/assets/earth.jpg')
  const earthRef = useRef()

  useFrame(() => {
    earthRef.current.rotation.y += 0.001
  })

  return (
    <mesh ref={earthRef}>
      <sphereGeometry args={[1, 64, 64]} />
      <meshStandardMaterial map={texture} />
    </mesh>
  )
}

function OrbitTrail({ trail }) {
  if (!trail || trail.length < 2) return null

  const points = trail.map(
    ([x, y, z]) => new THREE.Vector3(x / EARTH_RADIUS_KM, y / EARTH_RADIUS_KM, z / EARTH_RADIUS_KM)
  )
  const geometry = new THREE.BufferGeometry().setFromPoints(points)

  return (
    <line geometry={geometry}>
      <lineBasicMaterial attach="material" color="white" linewidth={2} />
    </line>
  )
}

function Satellite({ position }) {
  const meshRef = useRef()
  const lastPos = useRef(null)

  useFrame(() => {
    if (meshRef.current && position) {
      const scaled = position.map(coord => coord / EARTH_RADIUS_KM)
      meshRef.current.position.set(...scaled)

      const rounded = scaled.map(x => x.toFixed(5))
      const same = lastPos.current?.every((val, i) => val === rounded[i])
      if (!same) {
        console.log("[Satellite] Updated position to:", rounded)
        lastPos.current = rounded
      }
    }
  })

  return (
    <mesh ref={meshRef}>
      <sphereGeometry args={[0.02, 32, 32]} />
      <meshBasicMaterial color="red" transparent opacity={0.7} />
    </mesh>
  )
}

export default function OrbitDisplay({ missionTime, timeScale }) {
  const [position, setPosition] = useState(null)
  const [trail, setTrail] = useState([])

  const missionTimeRef = useRef(missionTime)
  useEffect(() => {
    missionTimeRef.current = missionTime
  }, [missionTime])

  useEffect(() => {
    const interval = setInterval(() => {
      const t = missionTimeRef.current
      fetch('http://localhost:5000/propagate?missionTime=' + t)
        .then(res => res.json())
        .then(data => {
          if (data.position) {
            const pos = [...data.position]
            setPosition(pos)
            setTrail(prev => [...prev, pos])
          }
        })
        .catch(err => console.error('[OrbitDisplay] Fetch error:', err))
    }, 1000 / 24)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="bg-zinc-800 p-2 rounded-lg shadow-lg h-[400px] overflow-hidden">
      <h2 className="text-lg font-semibold text-blue-300 mb-2">Orbit Visualization</h2>
      <div className="w-full h-[360px] rounded-lg overflow-hidden">
        <Canvas camera={{ position: [0, 0, 20], fov: 45 }}>
          <ambientLight intensity={1.0} />
          <directionalLight position={[3, 2, 1]} intensity={1.5} />
          <pointLight position={[-3, -2, -1]} intensity={1} />

          <Suspense fallback={null}>
            <Earth />
            <OrbitTrail trail={trail} />
            <Satellite position={position} />
          </Suspense>

          <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade />
          <OrbitControls target={[0, 0, 0]} minDistance={1} maxDistance={100} />
        </Canvas>
      </div>
    </div>
  )
}

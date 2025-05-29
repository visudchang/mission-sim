import { Canvas, useFrame, useLoader } from '@react-three/fiber'
import { OrbitControls, Stars } from '@react-three/drei'
import { TextureLoader } from 'three/src/loaders/TextureLoader'
import { Suspense, useRef, useEffect, useState } from 'react'
import * as THREE from 'three'

const EARTH_RADIUS_KM = 6371
const DEFAULT_RADIUS = 1.47 // fallback

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

function OrbitRing({ position }) {
  let radius = DEFAULT_RADIUS
  if (position) {
    const r_km = Math.sqrt(position[0]**2 + position[1]**2 + position[2]**2)
    radius = r_km / EARTH_RADIUS_KM
  }

  const points = []
  for (let i = 0; i <= 360; i++) {
    const angle = (i * Math.PI) / 180
    points.push(new THREE.Vector3(Math.cos(angle) * radius, 0, Math.sin(angle) * radius))
  }

  const orbitPath = new THREE.BufferGeometry().setFromPoints(points)

  return (
    <line geometry={orbitPath}>
      <lineBasicMaterial attach="material" color="white" linewidth={2} />
    </line>
  )
}

function Satellite({ position }) {
  const meshRef = useRef()

  useFrame(() => {
    if (meshRef.current && position) {
      const [x_km, y_km, z_km] = position
      const x = x_km / EARTH_RADIUS_KM
      const z = y_km / EARTH_RADIUS_KM // y → z
      const y = z_km / EARTH_RADIUS_KM // z → y
      meshRef.current.position.set(x, y, z)
    }
  })

  return (
    <mesh ref={meshRef}>
      <sphereGeometry args={[0.03, 32, 32]} />
      <meshBasicMaterial color="red" transparent opacity={0.7} />
    </mesh>
  )
}

export default function OrbitDisplay() {
  const [position, setPosition] = useState(null)

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8765')
    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        if (data.position) {
          setPosition(data.position)
        }
      } catch (err) {
        console.error('[OrbitDisplay] Telemetry parse error:', err)
      }
    }
    return () => socket.close()
  }, [])

  return (
    <div className="bg-zinc-800 p-2 rounded-lg shadow-lg h-[400px] overflow-hidden">
      <h2 className="text-lg font-semibold text-blue-300 mb-2">Orbit Visualization</h2>
      <div className="w-full h-[360px] rounded-lg overflow-hidden">
        <Canvas className="rounded-lg">
          <ambientLight intensity={1.0} />
          <directionalLight position={[3, 2, 1]} intensity={1.5} />
          <pointLight position={[-3, -2, -1]} intensity={1} />

          <Suspense fallback={null}>
            <Earth />
            <OrbitRing position={position} />
            <Satellite position={position} />
          </Suspense>

          <Stars radius={1000} depth={50} count={5000} factor={4} saturation={0} fade />
          <OrbitControls />
        </Canvas>
      </div>
    </div>
  )
}

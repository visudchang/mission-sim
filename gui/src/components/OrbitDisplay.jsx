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

function OrbitRing({ path }) {
  if (!path || path.length === 0) return null

  const points = path.map(
    ([x, y, z]) => new THREE.Vector3(x / EARTH_RADIUS_KM, y / EARTH_RADIUS_KM, z / EARTH_RADIUS_KM)
  )
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
      const [x, y, z] = position.map(coord => coord / EARTH_RADIUS_KM)
      meshRef.current.position.set(x, y, z)
    }
  })

  return (
    <mesh ref={meshRef}>
      <sphereGeometry args={[0.02, 32, 32]} />
      <meshBasicMaterial color="red" transparent opacity={0.7} />
    </mesh>
  )
}

export default function OrbitDisplay() {
  const [position, setPosition] = useState(null)
  const [orbitPath, setOrbitPath] = useState([])

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8765')
    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        if (data.position) setPosition(data.position)
        if (data.orbitPath) setOrbitPath(data.orbitPath)
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
            <OrbitRing path={orbitPath} />
            <Satellite position={position} />
          </Suspense>

          <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade />
          <OrbitControls />
        </Canvas>
      </div>
    </div>
  )
}

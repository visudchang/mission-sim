import { Canvas, useFrame, useLoader } from '@react-three/fiber'
import { OrbitControls, Stars } from '@react-three/drei'
import { TextureLoader } from 'three/src/loaders/TextureLoader'
import { Suspense, useRef } from 'react'
import * as THREE from 'three'

function Earth() {
  const texture = useLoader(TextureLoader, '/src/assets/earth.jpg')
  const earthRef = useRef()

  // Rotate the Earth slowly
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

function OrbitRing() {
  const points = []
  const radius = 2
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

function Satellite() {
  return (
    <mesh position={[2, 0, 0]}>
      <sphereGeometry args={[0.02, 32, 32]} />
      <meshBasicMaterial color="red" transparent opacity={0.7} />
    </mesh>
  )
}

export default function OrbitDisplay() {
  return (
    <div className="bg-zinc-800 p-2 rounded-lg shadow-lg h-[400px] overflow-hidden">
      <h2 className="text-lg font-semibold text-cyan-400 mb-2">Orbit Visualization</h2>
      <div className="w-full h-[360px] rounded-lg overflow-hidden">
        <Canvas className="rounded-lg">
          {/* Balanced lighting */}
          <ambientLight intensity={1.0} />
          <directionalLight position={[3, 2, 1]} intensity={1.5} />
          <pointLight position={[-3, -2, -1]} intensity={1} />

          <Suspense fallback={null}>
            <Earth />
            <OrbitRing />
            <Satellite />
          </Suspense>

          <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade />
          <OrbitControls />
        </Canvas>
      </div>
    </div>
  )
}

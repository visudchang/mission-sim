import { Canvas, useFrame, useLoader } from '@react-three/fiber'
import { OrbitControls, Stars } from '@react-three/drei'
import { TextureLoader } from 'three/src/loaders/TextureLoader'
import { Suspense, useRef, useEffect, useState } from 'react'
import * as THREE from 'three'

const EARTH_RADIUS_KM = 6371

function Earth({ missionTime, timeScale }) {
  const texture = useLoader(TextureLoader, '/earth.jpg')
  const earthRef = useRef()

  useFrame(() => {
    if (earthRef.current) {
      const rotationSpeed = 0.00007292115 // rad/sec, 360 deg / 24 hr
      earthRef.current.rotation.y = missionTime * rotationSpeed
    }
  })

  return (
    <mesh ref={earthRef} rotation={[Math.PI / 2, 0, 0]}>
      <sphereGeometry args={[1, 64, 64]} />
      <meshStandardMaterial map={texture} side={THREE.FrontSide} />
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

function Satellite({ position, missionTime, latestBurnTime, timeScale }) {
  const meshRef = useRef()
  const lastPos = useRef(null)
  const flashedBurnRef = useRef(null)
  const [flash, setFlash] = useState(false)

  useEffect(() => {
    if (latestBurnTime === null) return;

    console.log("[Satellite] Detected burn time:", latestBurnTime);
    console.log("[Satellite] Last flashed burn time:", flashedBurnRef.current);

    if (flashedBurnRef.current !== null && Math.abs(flashedBurnRef.current - latestBurnTime) < 11.0) {
      console.log("[Satellite] Burn already flashed (within 11s), skipping");
      return;
    }

    console.log("[Satellite] Flashing burn now");
    setFlash(true);
    flashedBurnRef.current = latestBurnTime;

    const timer = setTimeout(() => {
      setFlash(false);
      console.log("[Satellite] Flash off");
    }, 500);

    return () => {
      clearTimeout(timer);
      console.log("[Satellite] Cleared previous timer");
    };
  }, [latestBurnTime]);

  useFrame(() => {
    if (meshRef.current && position) {
      const scaled = position.map(coord => coord / EARTH_RADIUS_KM)
      meshRef.current.position.set(...scaled)

      const rounded = scaled.map(x => x.toFixed(5))
      const same = lastPos.current?.every((val, i) => val === rounded[i])
      if (!same) lastPos.current = rounded
    }
  })

  return (
    <mesh ref={meshRef}>
      <sphereGeometry args={[0.02, 32, 32]} />
      <meshBasicMaterial color={flash ? 'orange' : 'red'} transparent opacity={flash ? 1.0 : 0.7} />
    </mesh>
  )
}

export default function OrbitDisplay({ missionTime, timeScale, latestBurnTime, setLatestBurnTime }) {
  const [position, setPosition] = useState(null)
  const [trail, setTrail] = useState([])

  const missionTimeRef = useRef(missionTime)

  useEffect(() => {
    missionTimeRef.current = missionTime
  }, [missionTime])

  useEffect(() => {
    if (missionTime === 0) {
      setTrail([])
      setPosition(null)
    }
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
          if (data.lastBurnTime !== undefined && data.lastBurnTime !== null) {
            setLatestBurnTime(data.lastBurnTime)
          }
        })
        .catch(err => console.error('[OrbitDisplay] Fetch error:', err))
    }, 1000 / 24)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="bg-zinc-800 p-2 rounded-lg shadow-lg h-[416px] overflow-hidden">
      <h2 className="text-lg font-semibold text-blue-300 mb-2">Orbit Visualization</h2>
      <div className="w-full h-[376px] rounded-lg overflow-hidden">
        <Canvas camera={{ position: [0, 10, 5], up: [0, 0, 1], fov: 45 }}>
          <ambientLight intensity={1.0} />
          <directionalLight position={[3, 2, 1]} intensity={1.5} />
          <pointLight position={[-3, -2, -1]} intensity={1} />

          <Suspense fallback={null}>
            <Earth missionTime={missionTime} timeScale={timeScale} />
            <OrbitTrail trail={trail} />
            <Satellite position={position} missionTime={missionTime} latestBurnTime={latestBurnTime} timeScale={timeScale} />
          </Suspense>

          <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade />
          <OrbitControls target={[0, 0, 0]} minDistance={1} maxDistance={100} />
        </Canvas>
      </div>
    </div>
  )
}

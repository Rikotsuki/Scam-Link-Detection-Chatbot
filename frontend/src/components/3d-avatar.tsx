"use client"

import React, { Suspense, useRef, useState, useCallback, useEffect } from 'react'
import { Canvas, useFrame, useLoader } from '@react-three/fiber'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
import { OrbitControls, ContactShadows, Html } from '@react-three/drei'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Shield, Bot, Loader2, AlertCircle, RefreshCw, Heart } from 'lucide-react'
import * as THREE from 'three'

interface AvatarModelProps {
  modelPath: string
  onClick?: () => void
  isHovered?: boolean
}

// 3D Model Component with proper error handling
const AvatarModel: React.FC<AvatarModelProps & { onError?: () => void }> = ({ 
  modelPath, 
  onClick,
  isHovered = false,
  onError
}) => {
  const meshRef = useRef<THREE.Group>(null)
  
  const gltf = useLoader(GLTFLoader, modelPath)
  
  // Auto-rotate animation with performance optimization
  useFrame((state) => {
    if (meshRef.current && gltf) {
      meshRef.current.rotation.y += isHovered ? 0.008 : 0.003
      meshRef.current.position.y = Math.sin(state.clock.elapsedTime * 0.3) * 0.08
    }
  })

  useEffect(() => {
    if (gltf?.scene) {
      try {
      // Optimize materials for better performance
      gltf.scene.traverse((child) => {
        if (child instanceof THREE.Mesh) {
          child.castShadow = true
          child.receiveShadow = true
          if (child.material) {
            child.material.envMapIntensity = 0.8
            // Ensure materials are properly configured
            if (child.material.map) {
              child.material.map.flipY = false
            }
          }
        }
      })
      console.log('3D model loaded and configured successfully')
      } catch (error) {
        console.error('Error configuring 3D model:', error)
        onError?.()
      }
    }
  }, [gltf, onError])

  if (!gltf?.scene) {
    return null
  }

  return (
    <group
      ref={meshRef}
      scale={0.7}
      position={[0, -0.2, 0]}
      onClick={onClick}
    >
      <primitive object={gltf.scene} />
    </group>
  )
}

// Simple 3D geometric avatar as fallback
const GeometricAvatar: React.FC<{
  isHovered: boolean
  onClick: () => void
}> = ({ isHovered, onClick }) => {
  const meshRef = useRef<THREE.Group>(null)
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += isHovered ? 0.02 : 0.01
      meshRef.current.position.y = Math.sin(state.clock.elapsedTime * 0.5) * 0.2
    }
  })

  return (
    <group ref={meshRef} onClick={onClick}>
      {/* AI (Pink) Character */}
      <group position={[-0.6, 0, 0]}>
        <mesh position={[0, 1.0, 0]}>
          <sphereGeometry args={[0.3, 32, 32]} />
          <meshStandardMaterial color="#ec4899" metalness={0.3} roughness={0.4} />
        </mesh>
        <mesh position={[0, 0.3, 0]}>
          <cylinderGeometry args={[0.25, 0.4, 0.6, 8]} />
          <meshStandardMaterial color="#f472b6" metalness={0.2} roughness={0.6} />
        </mesh>
        <mesh position={[0, 1.0, 0.4]}>
          <ringGeometry args={[0.12, 0.2, 6]} />
          <meshStandardMaterial color="#ffffff" emissive="#ec4899" emissiveIntensity={0.2} />
        </mesh>
      </group>

      {/* Haru (Blue) Character */}
      <group position={[0.6, 0, 0]}>
        <mesh position={[0, 1.0, 0]}>
          <sphereGeometry args={[0.3, 32, 32]} />
          <meshStandardMaterial color="#3b82f6" metalness={0.3} roughness={0.4} />
        </mesh>
        <mesh position={[0, 0.3, 0]}>
          <cylinderGeometry args={[0.25, 0.4, 0.6, 8]} />
          <meshStandardMaterial color="#60a5fa" metalness={0.2} roughness={0.6} />
        </mesh>
        <mesh position={[0, 1.0, 0.4]}>
          <sphereGeometry args={[0.1, 16, 16]} />
          <meshStandardMaterial color="#ffffff" emissive="#3b82f6" emissiveIntensity={0.2} />
        </mesh>
      </group>

      {/* Connecting Energy */}
      <mesh position={[0, 0.6, 0]} rotation={[0, 0, Math.PI / 2]}>
        <cylinderGeometry args={[0.03, 0.03, 1.2, 8]} />
        <meshStandardMaterial 
          color="#a855f7" 
          emissive="#a855f7" 
          emissiveIntensity={0.3}
          transparent
          opacity={0.7}
        />
      </mesh>
    </group>
  )
}

// Enhanced loading fallback
const LoadingFallback = ({ mascotName = "Ai and Haru" }: { mascotName?: string }) => (
  <Html center>
    <motion.div 
      className="flex flex-col items-center gap-3 p-4 bg-background/95 backdrop-blur-sm rounded-xl border shadow-lg min-w-48"
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div className="relative">
        <div className="w-12 h-12 rounded-full bg-gradient-to-br from-pink-500 to-blue-500 flex items-center justify-center">
          <Bot className="w-6 h-6 text-white" />
        </div>
        <Loader2 className="absolute -top-1 -right-1 w-5 h-5 animate-spin text-primary" />
      </div>
      <div className="text-center">
        <p className="text-sm font-medium mb-1">Loading {mascotName}...</p>
        <p className="text-xs text-muted-foreground">Preparing 3D experience</p>
      </div>
    </motion.div>
  </Html>
)

// Error fallback component
const ErrorFallback = ({ onRetry }: { onRetry?: () => void }) => (
  <Html center>
    <motion.div 
      className="flex flex-col items-center gap-3 p-4 bg-background/95 backdrop-blur-sm rounded-xl border shadow-lg"
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
    >
      <div className="w-12 h-12 rounded-full bg-gradient-to-br from-pink-500 to-blue-500 flex items-center justify-center">
        <AlertCircle className="w-6 h-6 text-white" />
      </div>
      <div className="text-center">
        <p className="text-sm font-medium mb-1">Model unavailable</p>
        <p className="text-xs text-muted-foreground">Using fallback design</p>
        {onRetry && (
          <Button 
            size="sm" 
            onClick={onRetry}
            className="mt-2"
          >
            <RefreshCw className="w-3 h-3 mr-1" />
            Retry
          </Button>
        )}
      </div>
    </motion.div>
  </Html>
)

interface Avatar3DProps {
  onClick: () => void
  className?: string
  autoRotate?: boolean
  quality?: 'low' | 'medium' | 'high'
}

export const Avatar3D: React.FC<Avatar3DProps> = ({
  onClick,
  className = "",
  autoRotate = true,
  quality = 'medium'
}) => {
  const [isHovered, setIsHovered] = useState(false)
  const [useFallback, setUseFallback] = useState(false)

  // Performance settings based on quality
  const qualitySettings = {
    low: { dpr: 1, antialias: false, shadows: false },
    medium: { dpr: [1, 1.5] as [number, number], antialias: true, shadows: true },
    high: { dpr: [1, 2] as [number, number], antialias: true, shadows: true }
  }

  const settings = qualitySettings[quality]

  return (
    <div 
      className={`relative w-full h-full rounded-2xl overflow-hidden bg-gradient-to-br from-pink-500/5 to-blue-500/5 transition-all duration-300 ${className}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <Canvas
        camera={{ position: [0, 0.2, 10], fov: 30 }}
        style={{ background: 'transparent' }}
        gl={{ 
          alpha: true, 
          antialias: settings.antialias,
          powerPreference: 'high-performance'
        }}
        dpr={settings.dpr}
        performance={{ min: 0.5 }}
        onCreated={({ gl }) => {
          gl.setClearColor(0x000000, 0)
        }}
      >
        {/* Optimized lighting setup */}
        <ambientLight intensity={0.6} />
        <directionalLight 
          position={[10, 10, 5]} 
          intensity={1.2} 
          castShadow={settings.shadows}
          shadow-mapSize={settings.shadows ? [2048, 2048] : undefined}
        />
        <pointLight position={[-10, -10, -5]} intensity={0.4} />
        
        {/* Contact shadows */}
        {settings.shadows && (
          <ContactShadows 
            position={[0, -1.4, 0]} 
            opacity={0.4} 
            scale={10} 
            blur={1.5} 
            far={4} 
          />
        )}

        {/* 3D Model with fallback */}
        <Suspense fallback={<LoadingFallback mascotName="Ai and Haru" />}>
          {!useFallback ? (
            <AvatarModel
              modelPath="/3d_Model/fuyu_winter_robots.glb"
              onClick={onClick}
              isHovered={isHovered}
              onError={() => setUseFallback(true)}
            />
          ) : (
            <GeometricAvatar 
              isHovered={isHovered}
              onClick={onClick}
            />
          )}
        </Suspense>

        {/* Controls */}
        {autoRotate && (
          <OrbitControls
            enableZoom={true}
            enablePan={true}
            maxPolarAngle={Math.PI / 1.8}
            minPolarAngle={Math.PI / 4}
            autoRotate={!isHovered}
            autoRotateSpeed={0.5}
            enableDamping
            dampingFactor={0.1}
            minDistance={6}
            maxDistance={25}
            zoomSpeed={0.8}
            target={[0, 1.5, 0]}
          />
        )}
      </Canvas>

      {/* Overlay UI */}
      <div className="absolute inset-0 pointer-events-none">


        {/* Bottom Content */}
        <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 pointer-events-auto">
          <motion.div
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            <Button
              variant="outline"
              size="sm"
              onClick={onClick}
              className="bg-background/80 backdrop-blur-sm hover:bg-background/90 border-primary/20"
            >
              <Bot className="w-4 h-4 mr-2" />
              Chat with Ai & Haru
            </Button>
          </motion.div>
        </div>




      </div>

      {/* Click area for mobile */}
      <div 
        className="absolute inset-0 cursor-pointer md:hidden"
        onClick={onClick}
        aria-label="Chat with Ai and Haru"
      />
    </div>
  )
} 
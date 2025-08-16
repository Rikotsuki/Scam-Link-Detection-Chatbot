"use client"

import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Shield, Bot, MessageCircle, Heart } from 'lucide-react'
import Image from 'next/image'

interface ImageAvatarProps {
  mascotType: 'ai' | 'haru'
  onClick: () => void
  className?: string
  showControls?: boolean
}

export const ImageAvatar: React.FC<ImageAvatarProps> = ({
  mascotType,
  onClick,
  className = "",
  showControls = true
}) => {
  const [isHovered, setIsHovered] = useState(false)
  const [imageError, setImageError] = useState(false)

  const mascotInfo = {
    ai: {
      name: 'Ai',
      description: 'Your friendly scam-check assistant',
      color: 'from-pink-500/80 to-pink-600',
      bgColor: 'pink-500/5',
      badge: 'Scanner Assistant',
      icon: Shield,
      imagePath: '/images/ai.png',
      fallbackColor: 'bg-gradient-to-br from-pink-500 to-pink-600'
    },
    haru: {
      name: 'Haru',
      description: 'Your guardian for account recovery',
      color: 'from-blue-500/80 to-blue-600',
      bgColor: 'blue-500/5',
      badge: 'Recovery Guide',
      icon: Heart,
      imagePath: '/images/haru.png',
      fallbackColor: 'bg-gradient-to-br from-blue-500 to-blue-600'
    }
  }

  const currentMascot = mascotInfo[mascotType]
  const Icon = currentMascot.icon

  const handleImageError = () => {
    setImageError(true)
  }

  return (
    <div 
      className={`relative w-full h-64 rounded-2xl overflow-hidden bg-gradient-to-br from-primary/5 to-secondary/5 border-2 border-primary/10 hover:border-primary/20 transition-all duration-300 ${className}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Background Pattern */}
      <div className={`absolute inset-0 bg-${currentMascot.bgColor} transition-opacity duration-300`} />
      
      {/* Avatar Image or Fallback */}
      <div className="relative w-full h-full flex items-center justify-center">
        {!imageError ? (
          <motion.div
            className="relative w-32 h-40 rounded-xl overflow-hidden shadow-2xl"
            animate={{
              scale: isHovered ? 1.05 : 1,
              rotateY: isHovered ? 5 : 0,
            }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
          >
            <Image
              src={currentMascot.imagePath}
              alt={`${currentMascot.name} Avatar`}
              fill
              className="object-cover"
              onError={handleImageError}
              priority
            />
            {/* Gradient overlay */}
            <div className={`absolute inset-0 bg-gradient-to-t ${currentMascot.color} opacity-0 hover:opacity-20 transition-opacity duration-300`} />
          </motion.div>
        ) : (
          <motion.div
            className={`w-32 h-40 rounded-xl ${currentMascot.fallbackColor} flex items-center justify-center shadow-2xl`}
            animate={{
              scale: isHovered ? 1.05 : 1,
              rotateY: isHovered ? 5 : 0,
            }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
          >
            <Icon className="w-16 h-16 text-white" />
          </motion.div>
        )}

        {/* Floating elements */}
        <motion.div
          className="absolute top-4 right-4 w-4 h-4 bg-green-500 rounded-full shadow-lg"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.7, 1, 0.7]
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
        
        {/* Sparkle effects */}
        <motion.div
          className="absolute top-6 left-8 w-2 h-2 bg-yellow-400 rounded-full"
          animate={{
            scale: [0, 1, 0],
            opacity: [0, 1, 0]
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            delay: Math.random() * 2
          }}
        />
        <motion.div
          className="absolute bottom-8 right-6 w-1.5 h-1.5 bg-blue-400 rounded-full"
          animate={{
            scale: [0, 1, 0],
            opacity: [0, 1, 0]
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            delay: Math.random() * 2
          }}
        />
      </div>

      {/* Overlay UI */}
      {showControls && (
        <div className="absolute inset-0 pointer-events-none">







        </div>
      )}

      {/* Click area for mobile */}
      <div 
        className="absolute inset-0 cursor-pointer md:hidden"
        onClick={onClick}
        aria-label={`Chat with ${currentMascot.name}`}
      />
    </div>
  )
}

// Dual Avatar Component for showing both Ai and Haru
interface DualImageAvatarProps {
  onAiClick: () => void
  onHaruClick: () => void
  className?: string
}

export const DualImageAvatar: React.FC<DualImageAvatarProps> = ({
  onAiClick,
  onHaruClick,
  className = ""
}) => {
  return (
    <div className={`space-y-6 ${className}`}>
      {/* Labels outside the cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center"
        >
          <div className="flex items-center justify-center gap-2 mb-2">
            <div className="w-3 h-3 rounded-full bg-gradient-to-r from-pink-500 to-pink-600" />
            <h3 className="font-semibold text-sm text-foreground">Ai Scanner Assistant</h3>
          </div>
          <p className="text-xs text-muted-foreground">Your friendly scam-check assistant</p>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="text-center"
        >
          <div className="flex items-center justify-center gap-2 mb-2">
            <div className="w-3 h-3 rounded-full bg-gradient-to-r from-blue-500 to-blue-600" />
            <h3 className="font-semibold text-sm text-foreground">Haru Recovery Guide</h3>
          </div>
          <p className="text-xs text-muted-foreground">Your guardian for account recovery</p>
        </motion.div>
      </div>

      {/* 3D Model Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
          className="space-y-6"
        >
          <ImageAvatar 
            mascotType="ai" 
            onClick={onAiClick}
          />
          <div className="text-center">
            <Button
              variant="outline"
              size="sm"
              onClick={onAiClick}
              className="bg-gradient-to-r from-pink-500 to-pink-600 text-white border-pink-500 hover:bg-pink-600"
            >
              <Bot className="w-4 h-4 mr-2" />
              Chat with Ai
            </Button>
          </div>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="space-y-6"
        >
          <ImageAvatar 
            mascotType="haru" 
            onClick={onHaruClick}
          />
          <div className="text-center">
            <Button
              variant="outline"
              size="sm"
              onClick={onHaruClick}
              className="bg-gradient-to-r from-blue-500 to-blue-600 text-white border-blue-500 hover:bg-blue-600"
            >
              <Heart className="w-4 h-4 mr-2" />
              Chat with Haru
            </Button>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

// Simple Hero Avatar Component
export const HeroImageAvatar: React.FC<{ mascotType: 'ai' | 'haru', onClick: () => void }> = ({ 
  mascotType, 
  onClick 
}) => {
  return (
    <div className="relative w-full h-64 rounded-2xl overflow-hidden bg-gradient-to-br from-primary/10 to-secondary/10 border border-primary/20">
      <ImageAvatar
        mascotType={mascotType}
        onClick={onClick}
        showControls={false}
        className="border-0 bg-transparent"
      />
      
      {/* Simple overlay for hero */}
      <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2">
        <Button
          variant="outline"
          size="sm"
          onClick={onClick}
          className="bg-background/80 backdrop-blur-sm"
        >
          <Bot className="w-4 h-4 mr-2" />
          Chat with {mascotType === 'ai' ? 'Ai' : 'Haru'}
        </Button>
      </div>
      
      <div className="absolute top-4 right-4">
        <Badge variant="default" className="bg-green-500">
          Online
        </Badge>
      </div>
    </div>
  )
} 
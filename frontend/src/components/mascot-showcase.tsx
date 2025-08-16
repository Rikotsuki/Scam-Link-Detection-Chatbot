"use client"

import React from 'react'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { ImageAvatar } from '@/components/image-avatar'
import { Avatar3D } from '@/components/3d-avatar'
import { 
  Shield, 
  Heart, 
  MessageCircle, 
  ArrowRight,
  Bot,
  Users,
  TrendingUp,
  Clock
} from 'lucide-react'
import Image from 'next/image'

// Simplified mascot info without selection state
const mascotFeatures = {
  ai: {
    name: 'Ai',
    description: 'Your analytical companion specialized in identifying phishing links and online threats.',
    icon: Shield,
    color: 'from-pink-500 to-pink-600',
    bgColor: 'pink-500/5',
    accent: 'pink-500',
    capabilities: [
      'Real-time link analysis',
      'Pattern recognition',
      'Risk assessment',
      'Simple explanations'
    ]
  },
  haru: {
    name: 'Haru',
    description: 'Your empathetic guide through account recovery and security procedures.',
    icon: Heart,
    color: 'from-blue-500 to-blue-600', 
    bgColor: 'blue-500/5',
    accent: 'blue-500',
    capabilities: [
      'Step-by-step recovery guidance',
      'Emotional support during crises',
      'Security best practices',
      'Account monitoring tips'
    ]
  }
}

// Simplified mascot card without selection functionality
const MascotCard: React.FC<{ 
  mascot: 'ai' | 'haru'
  onChat: () => void 
}> = ({ mascot, onChat }) => {
  const info = mascotFeatures[mascot]
  const Icon = info.icon

  return (
    <motion.div
      layout
      className="h-full" 
      whileHover={{ scale: 1.02 }} 
      transition={{ type: "spring", stiffness: 300, damping: 30 }}
    >
      <Card className="h-full border border-border/40 transition-all duration-300 cursor-pointer relative overflow-hidden hover:border-primary/30 hover:shadow-md">
        <div className={`absolute inset-0 bg-${info.bgColor} opacity-50`} />
        
        <CardHeader className="relative z-10 pb-3">
          <div className="flex items-center justify-between mb-3">
            <div className={`p-2 rounded-lg bg-gradient-to-br ${info.color} shadow-md`}>
              <Icon className="w-5 h-5 text-white" />
            </div>
            <Badge variant="outline" className="border-border/40 text-xs">
              {mascot === 'ai' ? 'AI Assistant' : 'Recovery Guide'}
              </Badge>
          </div>
          <CardTitle className="text-lg font-bold">{info.name}</CardTitle>
        </CardHeader>

        <CardContent className="relative z-10 space-y-4">
          <p className="text-muted-foreground text-sm leading-relaxed">{info.description}</p>
          
          <div className="space-y-3">
            <h4 className="font-medium text-sm flex items-center gap-2">
              <span className="w-1 h-1 bg-current rounded-full" />
              Core Capabilities
            </h4>
            <ul className="space-y-1.5">
              {info.capabilities.map((capability, index) => (
                <li key={index} className="text-xs text-muted-foreground flex items-start gap-2">
                  <span className="w-1 h-1 bg-current rounded-full mt-1.5 flex-shrink-0" />
                  {capability}
                </li>
              ))}
            </ul>
          </div>

          <Button 
            onClick={(e) => { e.stopPropagation(); onChat(); }} 
            className={`w-full transition-all duration-300 bg-gradient-to-r ${info.color} text-white shadow-md hover:shadow-lg`}
            size="sm" 
          >
            <MessageCircle className="w-4 h-4 mr-2" />
            Chat with {info.name}
            <ArrowRight className="w-4 h-4 ml-auto" />
          </Button>
        </CardContent>
      </Card>
    </motion.div>
  )
}

export const MascotShowcase = () => {
  const openAiChat = () => {
    console.log('Opening AI chat...')
  }

  const openHaruChat = () => {
    console.log('Opening Haru chat...')
  }

  return (
    <section className="py-20 px-4 relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-background to-secondary/5" />
      
      <div className="relative max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: false, margin: "-100px" }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <motion.h2 
            className="text-4xl lg:text-5xl font-bold mb-6 text-center relative"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: false, margin: "-100px" }}
          >
            Meet Your{' '}
            <span className="text-foreground relative inline-block">
              Digital Guardians
              <div className="absolute -bottom-1 left-0 w-full h-0.5 bg-gradient-to-r from-primary via-secondary to-primary rounded-full"></div>
            </span>
          </motion.h2>
          
          <p className="text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            Two AI-powered companions, each with unique personalities and specialized skills to protect 
            you from online threats and guide you through any security challenges.
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-3 gap-8 items-start">
          {/* Mascot Cards - Smaller */}
          <motion.div 
            className="lg:col-span-1 space-y-4"
            initial={{ opacity: 0, x: -50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: false, margin: "-100px" }}
            transition={{ duration: 0.6 }}
          >
            <MascotCard mascot="ai" onChat={openAiChat} />
            <MascotCard mascot="haru" onChat={openHaruChat} />
          </motion.div>

          {/* Combined Display */}
          <motion.div
            className="lg:col-span-2 space-y-6"
            initial={{ opacity: 0, x: 50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: false, margin: "-100px" }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            {/* Combined Image */}
            <Card className="p-6 shadow-xl">
              <div className="text-center mb-4">
                <h3 className="text-lg font-semibold mb-2">Your Guardian Team</h3>
                  <p className="text-sm text-muted-foreground">
                  AI-powered protection working together for your safety
                  </p>
                </div>
                
              <div className="relative w-full h-80 rounded-xl overflow-hidden bg-gradient-to-br from-pink-500/10 to-blue-500/10 flex items-center justify-center">
                <Image
                  src="/images/AiandHaru.png"
                  alt="Ai and Haru - Your Digital Guardians"
                  fill
                  className="object-contain"
                  priority
                />
                {/* Overlay with names */}
                <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex items-center gap-8">
                  <div className="text-center">
                    <div className="w-12 h-12 rounded-full bg-gradient-to-br from-pink-500 to-pink-600 flex items-center justify-center mb-2 shadow-lg">
                      <Shield className="w-6 h-6 text-white" />
                    </div>
                    <span className="text-sm font-bold text-foreground bg-background/80 px-2 py-1 rounded-full">Ai</span>
                  </div>
                  <div className="text-center">
                    <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center mb-2 shadow-lg">
                      <Heart className="w-6 h-6 text-white" />
                    </div>
                    <span className="text-sm font-bold text-foreground bg-background/80 px-2 py-1 rounded-full">Haru</span>
                  </div>
                </div>
              </div>
            </Card>

            {/* 3D Model Display */}
            <Card className="p-6">
              <div className="text-center mb-4">
                <h3 className="text-lg font-semibold mb-2">Interactive 3D Experience</h3>
                <p className="text-sm text-muted-foreground mb-2">
                  Click and drag to interact with your guardians
                </p>
                <div className="flex items-center justify-center gap-4 text-xs text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <div className="w-2 h-2 bg-primary rounded-full"></div>
                    <span>Scroll to zoom</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <div className="w-2 h-2 bg-secondary rounded-full"></div>
                    <span>Drag to rotate</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <div className="w-2 h-2 bg-primary/60 rounded-full"></div>
                    <span>Click to chat</span>
                  </div>
                </div>
              </div>
              <div className="w-full h-96 rounded-xl overflow-hidden">
                <Avatar3D onClick={() => console.log('3D model clicked')} className="w-full h-full" />
              </div>
            </Card>

            {/* Quick Stats */}
            <div className="grid grid-cols-2 gap-4">
              <Card className="p-4 text-center">
                <div className="flex items-center justify-center gap-2 mb-2">
                  <Users className="w-5 h-5 text-primary" />
                  <span className="font-semibold">24/7</span>
                </div>
                <p className="text-sm text-muted-foreground">Available</p>
              </Card>
              <Card className="p-4 text-center">
                <div className="flex items-center justify-center gap-2 mb-2">
                  <TrendingUp className="w-5 h-5 text-secondary" />
                  <span className="font-semibold">AI Powered</span>
                </div>
                <p className="text-sm text-muted-foreground">Protection</p>
              </Card>
            </div>

            {/* CTA */}
            <motion.div
              className="bg-gradient-to-br from-primary/5 to-secondary/5 rounded-2xl p-6 border border-primary/10"
              whileHover={{ scale: 1.02 }}
              transition={{ type: "spring", stiffness: 300, damping: 30 }}
            >
              <div className="text-center">
                <h3 className="text-lg font-semibold mb-2">Ready to get protected?</h3>
                  <p className="text-sm text-muted-foreground mb-4">
                  Start your conversation with Ai or Haru and experience next-level security assistance.
                </p>
                <div className="flex gap-3 justify-center">
                  <Button onClick={openAiChat} className="bg-gradient-to-r from-pink-500 to-pink-600 text-white">
                    <Bot className="w-4 h-4 mr-2" />
                    Chat with Ai
                    </Button>
                  <Button onClick={openHaruChat} className="bg-gradient-to-r from-blue-500 to-blue-600 text-white">
                    <Heart className="w-4 h-4 mr-2" />
                    Chat with Haru
                    </Button>
                </div>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </section>
  )
} 
"use client"

import React from 'react'
import { motion } from 'framer-motion'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { DarkModeToggle } from '@/components/dark-mode-toggle'
import { 
  Shield, 
  Heart, 
  Sparkles,
  ArrowRight,
  MessageCircle,
  Zap,
  Eye,
  Bot,
  User,
  Wifi,
  ArrowLeft,
  Star,
  Activity,
  Crown,
  Sword,
  Gem,
  Flame,
  Droplets,
  Moon,
  Sun,
  Sparkles as SparklesIcon
} from 'lucide-react'
import Link from 'next/link'

const characters = [
  {
    id: 'ai-chan',
    name: 'AI-chan',
    title: 'Phishing Detection Expert',
    description: 'Your cheerful AI companion for detecting online threats and analyzing suspicious links.',
    personality: 'Cheerful and energetic anime girl who loves protecting users from online dangers.',
    color: 'bg-secondary text-secondary-foreground',
    icon: <Shield className="w-6 h-6" />,
    greeting: "Hello! I'm AI-chan, your cheerful AI companion for detecting online threats! 🛡️",
    image: '/images/ai.png',
    status: 'online',
    capabilities: ['URL Analysis', 'Image Analysis', 'Threat Detection', 'Voice Warnings'],
    features: [
      'Real-time URL threat analysis',
      'Screenshot and image examination',
      'Advanced phishing detection',
      'Voice-powered warnings',
      'Confidence scoring system'
    ],
    element: 'fire',
    elementIcon: <Flame className="w-4 h-4" />,
    elementColor: 'text-orange-500'
  },
  {
    id: 'haru',
    name: 'Haru',
    title: 'Recovery Assistant',
    description: 'Your gentle companion for recovery assistance and step-by-step guidance.',
    personality: 'Gentle and caring character who helps users recover from security incidents.',
    color: 'bg-primary text-primary-foreground',
    icon: <Heart className="w-6 h-6" />,
    greeting: "Hello there! I'm Haru, your gentle recovery assistant. 💙",
    image: '/images/haru.png',
    status: 'online',
    capabilities: ['Recovery Guidance', 'Step-by-step Help', 'Screenshot Analysis', 'Voice Support'],
    features: [
      'Step-by-step recovery guidance',
      'Account compromise assistance',
      'Scam recovery support',
      'Gentle emotional support',
      'Voice-powered guidance'
    ],
    element: 'water',
    elementIcon: <Droplets className="w-4 h-4" />,
    elementColor: 'text-blue-500'
  }
]

export default function GuardiansPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary/5 via-background to-secondary/5 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute top-20 left-10 w-32 h-32 bg-primary/10 rounded-full blur-xl"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.3, 0.6, 0.3],
          }}
          transition={{
            duration: 4,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
        <motion.div
          className="absolute bottom-20 right-10 w-40 h-40 bg-secondary/10 rounded-full blur-xl"
          animate={{
            scale: [1.2, 1, 1.2],
            opacity: [0.4, 0.7, 0.4],
          }}
          transition={{
            duration: 5,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 1
          }}
        />
        <motion.div
          className="absolute top-1/2 left-1/2 w-24 h-24 bg-gradient-to-r from-primary/20 to-secondary/20 rounded-full blur-lg"
          animate={{
            scale: [1, 1.5, 1],
            opacity: [0.2, 0.5, 0.2],
          }}
          transition={{
            duration: 6,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 2
          }}
        />
      </div>

      {/* Header */}
      <div className="container mx-auto px-4 py-8 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <div className="flex items-center justify-center gap-3 mb-4">
            <motion.div 
              className="w-16 h-16 bg-gradient-to-br from-primary to-secondary rounded-2xl flex items-center justify-center shadow-2xl"
              animate={{ 
                rotate: [0, 5, -5, 0],
                scale: [1, 1.05, 1]
              }}
              transition={{ 
                duration: 3, 
                repeat: Infinity,
                ease: "easeInOut"
              }}
            >
              <Crown className="w-8 h-8 text-white" />
            </motion.div>
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-primary via-secondary to-primary bg-clip-text text-transparent">
                AI Guardians
              </h1>
              <p className="text-muted-foreground text-lg">
                Choose your digital protector
              </p>
            </div>
          </div>
          
          {/* Dark Mode Toggle */}
          <div className="flex justify-center mb-6">
            <DarkModeToggle />
          </div>
        </motion.div>

        {/* System Status */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8"
        >
          <Card className="border-0 shadow-2xl bg-background/80 backdrop-blur-sm max-w-2xl mx-auto">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-2">
                    <motion.div 
                      className="w-3 h-3 rounded-full bg-green-500"
                      animate={{ scale: [1, 1.2, 1] }}
                      transition={{ duration: 2, repeat: Infinity }}
                    />
                    <span className="text-sm font-medium">System Status</span>
                  </div>
                  <div className="flex items-center gap-4 text-xs">
                    <div className="flex items-center gap-1">
                      <Wifi className="w-3 h-3 text-green-600" />
                      <span>TTS</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Shield className="w-3 h-3 text-green-600" />
                      <span>URLhaus</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <Eye className="w-3 h-3 text-green-600" />
                      <span>Vision</span>
                    </div>
                  </div>
                </div>
                <Badge variant="outline" className="text-xs">
                  v2.0.0
                </Badge>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Character Selection */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-6xl mx-auto">
          {characters.map((character, index) => (
            <motion.div
              key={character.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 + index * 0.1 }}
              whileHover={{ y: -5 }}
            >
              <Card className="border-0 shadow-2xl hover:shadow-3xl transition-all duration-300 group bg-background/80 backdrop-blur-sm overflow-hidden relative">
                {/* Element Background */}
                <div className={`absolute inset-0 opacity-5 ${character.elementColor.replace('text-', 'bg-')}`} />
                
                <CardHeader className="text-center pb-4 relative">
                  <div className="flex justify-center mb-4">
                    <motion.div 
                      className="relative"
                      whileHover={{ scale: 1.05 }}
                      transition={{ type: "spring", stiffness: 300 }}
                    >
                      <Avatar className="w-28 h-28 ring-4 ring-background shadow-xl">
                        <AvatarImage src={character.image} alt={character.name} />
                        <AvatarFallback className={`${character.color} text-3xl`}>
                          {character.name.charAt(0)}
                        </AvatarFallback>
                      </Avatar>
                      <div className={`absolute -bottom-1 -right-1 w-7 h-7 rounded-full border-3 border-background ${
                        character.status === 'online' ? 'bg-green-500' : 'bg-red-500'
                      } shadow-lg`} />
                      <div className={`absolute -top-2 -left-2 w-8 h-8 rounded-full ${character.elementColor} bg-background/80 backdrop-blur-sm flex items-center justify-center shadow-lg`}>
                        {character.elementIcon}
                      </div>
                    </motion.div>
                  </div>
                  <div className="flex items-center justify-center gap-2 mb-2">
                    {character.icon}
                    <h2 className="text-3xl font-bold">{character.name}</h2>
                  </div>
                  <Badge variant="secondary" className={`${character.color} text-sm px-4 py-1`}>
                    {character.title}
                  </Badge>
                </CardHeader>
                
                <CardContent className="space-y-6 relative">
                  <p className="text-muted-foreground text-center text-lg leading-relaxed">
                    {character.description}
                  </p>
                  
                  <div className="space-y-4">
                    <h4 className="font-semibold text-sm flex items-center gap-2">
                      <SparklesIcon className="w-4 h-4" />
                      Capabilities:
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {character.capabilities.map((capability, idx) => (
                        <Badge key={idx} variant="outline" className="text-xs">
                          {capability}
                        </Badge>
                      ))}
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <h4 className="font-semibold text-sm flex items-center gap-2">
                      <Star className="w-4 h-4" />
                      Features:
                    </h4>
                    <ul className="space-y-3">
                      {character.features.map((feature, idx) => (
                        <motion.li 
                          key={idx} 
                          className="flex items-start gap-3 text-sm text-muted-foreground"
                          initial={{ opacity: 0, x: -10 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: 0.3 + idx * 0.1 }}
                        >
                          <div className={`w-2 h-2 rounded-full mt-2 flex-shrink-0 ${character.elementColor.replace('text-', 'bg-')}`} />
                          {feature}
                        </motion.li>
                      ))}
                    </ul>
                  </div>
                  
                  <motion.div
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <Button 
                      asChild
                      className={`w-full ${character.color} group-hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl`}
                    >
                      <Link href={`/${character.id}`}>
                        <MessageCircle className="w-5 h-5 mr-2" />
                        Chat with {character.name}
                        <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                      </Link>
                    </Button>
                  </motion.div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Features Overview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mt-12"
        >
          <Card className="border-0 shadow-2xl bg-background/80 backdrop-blur-sm max-w-4xl mx-auto">
            <CardHeader className="text-center">
              <CardTitle className="flex items-center justify-center gap-2 text-2xl">
                <Sword className="w-6 h-6" />
                Guardian Powers
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <motion.div 
                  className="text-center space-y-4"
                  whileHover={{ y: -5 }}
                  transition={{ type: "spring", stiffness: 300 }}
                >
                  <div className="w-16 h-16 bg-secondary/20 rounded-2xl flex items-center justify-center mx-auto shadow-lg">
                    <Zap className="w-8 h-8 text-secondary" />
                  </div>
                  <h4 className="font-semibold text-lg">Real-time Analysis</h4>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    Instant threat detection and analysis with advanced AI algorithms
                  </p>
                </motion.div>
                <motion.div 
                  className="text-center space-y-4"
                  whileHover={{ y: -5 }}
                  transition={{ type: "spring", stiffness: 300 }}
                >
                  <div className="w-16 h-16 bg-primary/20 rounded-2xl flex items-center justify-center mx-auto shadow-lg">
                    <MessageCircle className="w-8 h-8 text-primary" />
                  </div>
                  <h4 className="font-semibold text-lg">Voice Integration</h4>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    Natural voice responses with Japanese TTS for enhanced user experience
                  </p>
                </motion.div>
                <motion.div 
                  className="text-center space-y-4"
                  whileHover={{ y: -5 }}
                  transition={{ type: "spring", stiffness: 300 }}
                >
                  <div className="w-16 h-16 bg-green-500/20 rounded-2xl flex items-center justify-center mx-auto shadow-lg">
                    <Activity className="w-8 h-8 text-green-600" />
                  </div>
                  <h4 className="font-semibold text-lg">24/7 Protection</h4>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    Always available to help with security concerns and recovery guidance
                  </p>
                </motion.div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Back to Home */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="text-center mt-8"
        >
          <Button variant="ghost" asChild>
            <Link href="/" className="flex items-center gap-2 mx-auto">
              <ArrowLeft className="w-4 h-4" />
              Back to Home
            </Link>
          </Button>
        </motion.div>
      </div>
    </div>
  )
} 
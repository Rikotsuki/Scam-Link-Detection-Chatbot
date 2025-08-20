"use client"

import React, { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Textarea } from '@/components/ui/textarea'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Separator } from '@/components/ui/separator'
import { DarkModeToggle } from '@/components/dark-mode-toggle'
import { 
  Shield, 
  Play, 
  Pause, 
  Send,
  MessageCircle,
  Search,
  Link as LinkIcon,
  FileImage,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Loader2,
  Sparkles,
  Zap,
  Eye,
  Bot,
  User,
  Wifi,
  ArrowLeft,
  Upload,
  Mic,
  Settings,
  Info,
  Flame,
  Crown,
  Sword,
  Star,
  Activity,
  Sparkles as SparklesIcon
} from 'lucide-react'
import Link from 'next/link'

interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  voiceFile?: string
  isPlaying?: boolean
  analysis?: {
    type: 'url' | 'image' | 'general'
    result?: any
  }
}

export default function AIChanPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [systemStatus, setSystemStatus] = useState({
    tts: 'active',
    urlhaus: 'active',
    vision: 'active',
    overall: 'online'
  })
  const audioRef = useRef<HTMLAudioElement>(null)
  const chatEndRef = useRef<HTMLDivElement>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    // Auto-scroll to bottom of chat
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    // Initialize with AI-chan greeting
    if (messages.length === 0) {
      const greetingMessage: ChatMessage = {
        id: '1',
        role: 'assistant',
        content: "Hello! I'm AI-chan, your cheerful AI companion for detecting online threats! 🛡️ I can analyze URLs, examine screenshots, and help keep you safe from phishing attacks. What would you like me to help you with today?",
        timestamp: new Date(),
        voiceFile: `tts_ai_chan_greeting_${Date.now()}.wav`
      }
      setMessages([greetingMessage])
    }
  }, [])

  const handleSendMessage = async () => {
    if (!input.trim() && !selectedFile) return

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim() || `Analyzing uploaded image: ${selectedFile?.name}`,
      timestamp: new Date(),
      analysis: selectedFile ? { type: 'image' } : undefined
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    // Simulate AI response
    setTimeout(() => {
      const responses = [
        "I've analyzed the content and it looks safe! However, always stay vigilant and double-check before sharing personal information. 🔍",
        "I detected some suspicious elements here. This could be a phishing attempt. Please be very careful and don't enter any personal details! ⚠️",
        "This appears to be legitimate, but remember to always verify the source and never share sensitive information unless you're absolutely sure. ✅",
        "I found some concerning patterns. This might be a scam. Let me help you understand what to look out for in the future! 🚨",
        "The analysis shows this is safe to proceed, but always trust your instincts. If something feels off, it probably is! 💡"
      ]

      const randomResponse = responses[Math.floor(Math.random() * responses.length)]
      
      const aiMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: randomResponse,
        timestamp: new Date(),
        voiceFile: `tts_ai_chan_response_${Date.now()}.wav`,
        analysis: {
          type: selectedFile ? 'image' : 'url',
          result: {
            is_safe: Math.random() > 0.3,
            confidence: Math.random() * 0.4 + 0.6,
            threats: Math.random() > 0.7 ? ['suspicious_redirect', 'fake_login'] : [],
            risk_level: Math.random() > 0.3 ? 'low' : 'high'
          }
        }
      }
      
      setMessages(prev => [...prev, aiMessage])
      setIsLoading(false)
      setSelectedFile(null)
    }, 2000)
  }

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
    }
  }

  const playVoice = (message: ChatMessage) => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause()
      } else {
        audioRef.current.play()
      }
      setIsPlaying(!isPlaying)
    }
  }

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'high': return 'text-red-600 bg-red-100'
      case 'medium': return 'text-yellow-600 bg-yellow-100'
      case 'low': return 'text-green-600 bg-green-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-secondary/5 via-background to-secondary/10 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute top-20 right-10 w-40 h-40 bg-secondary/10 rounded-full blur-2xl"
          animate={{
            scale: [1, 1.3, 1],
            opacity: [0.2, 0.5, 0.2],
          }}
          transition={{
            duration: 4,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
        <motion.div
          className="absolute bottom-20 left-10 w-32 h-32 bg-orange-500/10 rounded-full blur-xl"
          animate={{
            scale: [1.2, 1, 1.2],
            opacity: [0.3, 0.6, 0.3],
          }}
          transition={{
            duration: 5,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 1
          }}
        />
      </div>

      {/* Header */}
      <div className="border-b bg-background/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button variant="ghost" asChild size="sm">
                <Link href="/guardians" className="flex items-center gap-2">
                  <ArrowLeft className="w-4 h-4" />
                  Back to Guardians
                </Link>
              </Button>
              <div className="flex items-center gap-3">
                <motion.div
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
                  <Avatar className="w-12 h-12 ring-2 ring-secondary/20">
                    <AvatarImage src="/images/ai.png" alt="AI-chan" />
                    <AvatarFallback className="bg-secondary text-secondary-foreground">
                      AI
                    </AvatarFallback>
                  </Avatar>
                </motion.div>
                <div>
                  <h1 className="text-xl font-bold">AI-chan</h1>
                  <p className="text-sm text-muted-foreground">Phishing Detection Expert</p>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-xs">
                <motion.div 
                  className="w-2 h-2 rounded-full bg-green-500"
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ duration: 2, repeat: Infinity }}
                />
                <span>Online</span>
              </div>
              <Badge variant="outline" className="text-xs">
                v2.0.0
              </Badge>
              <DarkModeToggle />
            </div>
          </div>
        </div>
      </div>

      {/* Chat Interface */}
      <div className="container mx-auto px-4 py-6 max-w-4xl">
        <div className="flex flex-col h-[calc(100vh-200px)]">
          {/* Messages */}
          <ScrollArea className="flex-1 mb-4">
            <div className="space-y-6 pb-4">
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex gap-4 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  {message.role === 'assistant' && (
                    <motion.div
                      whileHover={{ scale: 1.05 }}
                      transition={{ type: "spring", stiffness: 300 }}
                    >
                      <Avatar className="w-10 h-10 ring-2 ring-secondary/20">
                        <AvatarImage src="/images/ai.png" alt="AI-chan" />
                        <AvatarFallback className="bg-secondary text-secondary-foreground text-xs">
                          AI
                        </AvatarFallback>
                      </Avatar>
                    </motion.div>
                  )}
                  
                  <div className={`max-w-[80%] ${message.role === 'user' ? 'order-1' : ''}`}>
                    <Card className={`${message.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-muted/80 backdrop-blur-sm'} shadow-lg`}>
                      <CardContent className="p-4">
                        <p className="text-sm leading-relaxed">{message.content}</p>
                        
                        {/* Analysis Results */}
                        {message.analysis?.result && (
                          <motion.div 
                            className="mt-4 pt-4 border-t border-border/20"
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            transition={{ delay: 0.2 }}
                          >
                            <div className="space-y-3">
                              <div className="flex items-center justify-between">
                                <span className="text-xs opacity-80">Safety:</span>
                                <Badge 
                                  variant={message.analysis.result.is_safe ? "default" : "destructive"}
                                  className="text-xs"
                                >
                                  {message.analysis.result.is_safe ? 'Safe' : 'Dangerous'}
                                </Badge>
                              </div>
                              <div className="flex items-center justify-between">
                                <span className="text-xs opacity-80">Risk Level:</span>
                                <Badge 
                                  variant="outline"
                                  className={`text-xs ${getRiskColor(message.analysis.result.risk_level)}`}
                                >
                                  {message.analysis.result.risk_level.toUpperCase()}
                                </Badge>
                              </div>
                              <div className="space-y-1">
                                <div className="flex items-center justify-between">
                                  <span className="text-xs opacity-80">Confidence:</span>
                                  <span className="text-xs font-medium">
                                    {Math.round(message.analysis.result.confidence * 100)}%
                                  </span>
                                </div>
                                <Progress 
                                  value={message.analysis.result.confidence * 100} 
                                  className="h-1"
                                />
                              </div>
                            </div>
                          </motion.div>
                        )}
                        
                        {/* Voice Button */}
                        {message.voiceFile && (
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => playVoice(message)}
                            className="mt-3 h-8 px-2 text-xs"
                          >
                            {isPlaying ? <Pause className="w-3 h-3" /> : <Play className="w-3 h-3" />}
                            Voice
                          </Button>
                        )}
                      </CardContent>
                    </Card>
                    <p className="text-xs text-muted-foreground mt-2">
                      {message.timestamp.toLocaleTimeString()}
                    </p>
                  </div>
                  
                  {message.role === 'user' && (
                    <Avatar className="w-10 h-10">
                      <AvatarFallback className="bg-muted text-xs">
                        <User className="w-5 h-5" />
                      </AvatarFallback>
                    </Avatar>
                  )}
                </motion.div>
              ))}
              
              {/* Loading Indicator */}
              {isLoading && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex gap-4"
                >
                  <Avatar className="w-10 h-10 ring-2 ring-secondary/20">
                    <AvatarImage src="/images/ai.png" alt="AI-chan" />
                    <AvatarFallback className="bg-secondary text-secondary-foreground text-xs">
                      AI
                    </AvatarFallback>
                  </Avatar>
                  <Card className="bg-muted/80 backdrop-blur-sm">
                    <CardContent className="p-4">
                      <div className="flex gap-1">
                        <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" />
                        <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                        <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              )}
              
              <div ref={chatEndRef} />
            </div>
          </ScrollArea>

          {/* Input Area */}
          <div className="border-t bg-background/80 backdrop-blur-sm p-4 rounded-lg shadow-lg">
            <div className="flex gap-3">
              {/* File Upload */}
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => fileInputRef.current?.click()}
                  className="flex-shrink-0"
                >
                  <Upload className="w-4 h-4" />
                </Button>
              </motion.div>
              
              {/* Text Input */}
              <div className="flex-1 relative">
                <Textarea
                  placeholder="Ask AI-chan to analyze a URL or upload a screenshot..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage()}
                  className="min-h-[60px] resize-none pr-12"
                />
                <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                  <Button
                    onClick={handleSendMessage}
                    disabled={(!input.trim() && !selectedFile) || isLoading}
                    className="absolute right-2 bottom-2 h-8 w-8 p-0 bg-secondary text-secondary-foreground hover:bg-secondary/80"
                  >
                    <Send className="w-4 h-4" />
                  </Button>
                </motion.div>
              </div>
            </div>
            
            {/* File Preview */}
            {selectedFile && (
              <motion.div 
                className="mt-3 flex items-center gap-2 p-2 bg-muted/50 rounded-lg"
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <FileImage className="w-4 h-4" />
                <span className="text-sm">{selectedFile.name}</span>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setSelectedFile(null)}
                  className="h-6 w-6 p-0 ml-auto"
                >
                  <XCircle className="w-4 h-4" />
                </Button>
              </motion.div>
            )}
            
            {/* Quick Actions */}
            <div className="mt-3 flex flex-wrap gap-2">
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setInput('Can you analyze this URL for me?')}
                  className="text-xs"
                >
                  <LinkIcon className="w-3 h-3 mr-1" />
                  URL Analysis
                </Button>
              </motion.div>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setInput('What are the signs of a phishing attack?')}
                  className="text-xs"
                >
                  <Shield className="w-3 h-3 mr-1" />
                  Safety Tips
                </Button>
              </motion.div>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setInput('I think I clicked a suspicious link, what should I do?')}
                  className="text-xs"
                >
                  <AlertTriangle className="w-3 h-3 mr-1" />
                  Emergency Help
                </Button>
              </motion.div>
            </div>
          </div>
        </div>
      </div>

      {/* Hidden Elements */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleFileUpload}
        className="hidden"
      />
      <audio ref={audioRef} onEnded={() => setIsPlaying(false)} />
    </div>
  )
} 
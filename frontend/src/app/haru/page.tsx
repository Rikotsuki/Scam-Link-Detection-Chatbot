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
import { 
  Heart, 
  Play, 
  Pause, 
  Send,
  MessageCircle,
  Search,
  FileImage,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Loader2,
  Sparkles,
  Zap,
  Bot,
  User,
  Wifi,
  ArrowLeft,
  Upload,
  Mic,
  Settings,
  Info,
  Shield,
  LifeBuoy,
  HelpCircle
} from 'lucide-react'
import Link from 'next/link'

interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  voiceFile?: string
  isPlaying?: boolean
  recoverySteps?: string[]
}

export default function HaruPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [systemStatus, setSystemStatus] = useState({
    tts: 'active',
    recovery: 'active',
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
    // Initialize with Haru greeting
    if (messages.length === 0) {
      const greetingMessage: ChatMessage = {
        id: '1',
        role: 'assistant',
        content: "Hello there! I'm Haru, your gentle recovery assistant. 💙 I'm here to help you recover from security incidents, provide step-by-step guidance, and support you through any online safety concerns. Don't worry, we'll get through this together! What's troubling you today?",
        timestamp: new Date(),
        voiceFile: `tts_haru_greeting_${Date.now()}.wav`
      }
      setMessages([greetingMessage])
    }
  }, [])

  const handleSendMessage = async () => {
    if (!input.trim() && !selectedFile) return

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim() || `Need help with: ${selectedFile?.name}`,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    // Simulate Haru response
    setTimeout(() => {
      const responses = [
        "I understand how stressful this can be. Let's take this step by step. First, try to stay calm - we'll work through this together. 💙",
        "That sounds really concerning. Don't worry, I'm here to help you recover from this. Let me guide you through the recovery process. 🤗",
        "I can see you're going through a difficult situation. Let's approach this methodically to get you back to safety. You're not alone in this! ✨",
        "This is definitely something we can work through together. I'll help you understand what happened and guide you to recovery. Stay strong! 💪",
        "I hear you, and I want you to know that recovery is absolutely possible. Let's start with the basics and build from there. 🌟"
      ]

      const recoverySteps = [
        "1. Immediately change your passwords",
        "2. Enable two-factor authentication",
        "3. Contact your bank if financial info was involved",
        "4. Monitor your accounts for suspicious activity",
        "5. Report the incident to relevant authorities"
      ]

      const randomResponse = responses[Math.floor(Math.random() * responses.length)]
      
      const haruMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: randomResponse,
        timestamp: new Date(),
        voiceFile: `tts_haru_response_${Date.now()}.wav`,
        recoverySteps: Math.random() > 0.5 ? recoverySteps : undefined
      }
      
      setMessages(prev => [...prev, haruMessage])
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary/5 via-background to-primary/10">
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
                <Avatar className="w-10 h-10">
                  <AvatarImage src="/images/haru.png" alt="Haru" />
                  <AvatarFallback className="bg-primary text-primary-foreground">
                    H
                  </AvatarFallback>
                </Avatar>
                <div>
                  <h1 className="text-lg font-semibold">Haru</h1>
                  <p className="text-sm text-muted-foreground">Recovery Assistant</p>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 text-xs">
                <div className="w-2 h-2 rounded-full bg-green-500" />
                <span>Online</span>
              </div>
              <Badge variant="outline" className="text-xs">
                v2.0.0
              </Badge>
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
                    <Avatar className="w-8 h-8">
                      <AvatarImage src="/images/haru.png" alt="Haru" />
                      <AvatarFallback className="bg-primary text-primary-foreground text-xs">
                        H
                      </AvatarFallback>
                    </Avatar>
                  )}
                  
                  <div className={`max-w-[80%] ${message.role === 'user' ? 'order-1' : ''}`}>
                    <Card className={`${message.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-muted'}`}>
                      <CardContent className="p-4">
                        <p className="text-sm leading-relaxed">{message.content}</p>
                        
                        {/* Recovery Steps */}
                        {message.recoverySteps && (
                          <div className="mt-4 pt-4 border-t border-border/20">
                            <h4 className="text-sm font-medium mb-2">Recovery Steps:</h4>
                            <div className="space-y-2">
                              {message.recoverySteps.map((step, index) => (
                                <div key={index} className="flex items-start gap-2">
                                  <div className="w-2 h-2 rounded-full bg-primary mt-2 flex-shrink-0" />
                                  <p className="text-xs opacity-80">{step}</p>
                                </div>
                              ))}
                            </div>
                          </div>
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
                    <Avatar className="w-8 h-8">
                      <AvatarFallback className="bg-muted text-xs">
                        <User className="w-4 h-4" />
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
                  <Avatar className="w-8 h-8">
                    <AvatarImage src="/images/haru.png" alt="Haru" />
                    <AvatarFallback className="bg-primary text-primary-foreground text-xs">
                      H
                    </AvatarFallback>
                  </Avatar>
                  <Card className="bg-muted">
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
          <div className="border-t bg-background/80 backdrop-blur-sm p-4 rounded-lg">
            <div className="flex gap-3">
              {/* File Upload */}
              <Button
                variant="outline"
                size="sm"
                onClick={() => fileInputRef.current?.click()}
                className="flex-shrink-0"
              >
                <Upload className="w-4 h-4" />
              </Button>
              
              {/* Text Input */}
              <div className="flex-1 relative">
                <Textarea
                  placeholder="Tell Haru what happened and get recovery guidance..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage()}
                  className="min-h-[60px] resize-none pr-12"
                />
                <Button
                  onClick={handleSendMessage}
                  disabled={(!input.trim() && !selectedFile) || isLoading}
                  className="absolute right-2 bottom-2 h-8 w-8 p-0 bg-primary text-primary-foreground hover:bg-primary/80"
                >
                  <Send className="w-4 h-4" />
                </Button>
              </div>
            </div>
            
            {/* File Preview */}
            {selectedFile && (
              <div className="mt-3 flex items-center gap-2 p-2 bg-muted/50 rounded-lg">
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
              </div>
            )}
            
            {/* Quick Actions */}
            <div className="mt-3 flex flex-wrap gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setInput('I clicked a suspicious link, what should I do?')}
                className="text-xs"
              >
                <AlertTriangle className="w-3 h-3 mr-1" />
                Clicked Bad Link
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setInput('I think my account was compromised')}
                className="text-xs"
              >
                <Shield className="w-3 h-3 mr-1" />
                Account Compromised
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setInput('I need help recovering from a scam')}
                className="text-xs"
              >
                <LifeBuoy className="w-3 h-3 mr-1" />
                Scam Recovery
              </Button>
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
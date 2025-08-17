"use client"

import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { 
  MessageCircle, 
  Bot,
  Heart,
  Send,
  Paperclip,
  Shield,
  ArrowRight
} from 'lucide-react'

// Mock chat messages for Ai (dark mode)
const mockChatMessagesAi = [
  {
    id: 1,
    sender: 'ai',
    message: "Hi! I'm Ai, your scam detection assistant. How can I help you stay safe today?",
    timestamp: '2:30 PM'
  },
  {
    id: 2,
    sender: 'user',
    message: "I received this suspicious link: bit.ly/free-phone-win",
    timestamp: '2:31 PM'
  },
  {
    id: 3,
    sender: 'ai',
    message: "⚠️ This looks suspicious! Let me analyze it for you...",
    timestamp: '2:31 PM'
  },
  {
    id: 4,
    sender: 'ai',
    message: "Analysis complete: This is a known phishing scam. The domain was registered recently and mimics legitimate giveaways. Would you like me to show you how to report it?",
    timestamp: '2:32 PM'
  }
]

// Mock chat messages for Haru (light mode)
const mockChatMessagesHaru = [
  {
    id: 1,
    sender: 'haru',
    message: "Hello! I'm Haru, your recovery and support guide. How can I help you stay safe today?",
    timestamp: '2:30 PM'
  },
  {
    id: 2,
    sender: 'user',
    message: "I received this suspicious link: bit.ly/free-phone-win",
    timestamp: '2:31 PM'
  },
  {
    id: 3,
    sender: 'haru',
    message: "💙 Let me help you check this link safely. I'll analyze it for you...",
    timestamp: '2:31 PM'
  },
  {
    id: 4,
    sender: 'haru',
    message: "I've found some concerning patterns with this link. It appears to be a scam. Would you like me to guide you through the steps to protect yourself and report it?",
    timestamp: '2:32 PM'
  }
]

export const ChatSection = () => {
  const [chatMessage, setChatMessage] = useState("")
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [selectedAssistant, setSelectedAssistant] = useState<'ai' | 'haru'>('ai')

  // Detect dark mode
  useEffect(() => {
    const checkDarkMode = () => {
      const htmlHasDark = document.documentElement.classList.contains('dark')
      const bodyHasDark = document.body.classList.contains('dark')
      const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      
      const isDark = htmlHasDark || bodyHasDark || systemPrefersDark
      setIsDarkMode(isDark)
    }

    checkDarkMode()

    const observer = new MutationObserver(checkDarkMode)
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class']
    })

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQuery.addEventListener('change', checkDarkMode)

    return () => {
      observer.disconnect()
      mediaQuery.removeEventListener('change', checkDarkMode)
    }
  }, [])

  // Get the appropriate chat messages and assistant info
  const isAi = selectedAssistant === 'ai'
  const mockChatMessages = isAi ? mockChatMessagesAi : mockChatMessagesHaru
  const assistantName = isAi ? 'Ai' : 'Haru'
  const assistantIcon = isAi ? Bot : Heart
  const assistantColor = isAi ? 'text-pink-500' : 'text-blue-500'
  const assistantBgColor = isAi ? 'bg-pink-500/10' : 'bg-blue-500/10'

  const ChatInterface = () => {
    const AssistantIcon = assistantIcon

    return (
      <div className="h-96 flex flex-col">
        {/* Chat messages */}
        <div className="flex-1 p-4 space-y-4 overflow-y-auto bg-muted/20 rounded-lg mb-4">
          {mockChatMessages.map((msg) => (
            <motion.div
              key={msg.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-[80%] p-3 rounded-lg ${
                msg.sender === 'user' 
                  ? 'bg-primary text-primary-foreground' 
                    : `bg-background border ${assistantBgColor}`
              }`}>
                  {(msg.sender === 'ai' || msg.sender === 'haru') && (
                  <div className="flex items-center gap-2 mb-1">
                      <AssistantIcon className={`w-4 h-4 ${assistantColor}`} />
                      <span className="text-xs font-medium">{assistantName}</span>
                  </div>
                )}
                <p className="text-sm">{msg.message}</p>
                <p className="text-xs opacity-70 mt-1">{msg.timestamp}</p>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Chat input */}
        <div className="flex gap-2">
          <Input
              placeholder={`Type your message to ${assistantName}...`}
            value={chatMessage}
            onChange={(e) => setChatMessage(e.target.value)}
            className="flex-1"
          />
          <Button size="icon" variant="outline">
            <Paperclip className="w-4 h-4" />
          </Button>
          <Button size="icon" className="gradient-bg text-white">
            <Send className="w-4 h-4" />
          </Button>
        </div>
      </div>
    )
  }

  return (
    <section id="chat" className="py-24 px-4 bg-gradient-to-b from-background to-muted/20">
      <div className="max-w-6xl mx-auto">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: false, margin: "-100px" }}
          className="text-center mb-16"
        >
          <div className="flex items-center justify-center gap-2 mb-6">
            <MessageCircle className="w-6 h-6 text-primary" />
            <Badge variant="outline">Live Chat</Badge>
          </div>
          
          <h2 className="text-4xl lg:text-5xl font-bold mb-6 relative">
            <span className="text-primary relative inline-block">
              Chat with AI
              <div className="absolute -bottom-1 left-0 w-full h-0.5 bg-gradient-to-r from-primary to-secondary rounded-full"></div>
            </span>{' '}
            Guardians
          </h2>
          
          <p className="text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            Get instant help from our AI assistants. Ask questions, report scams, or get step-by-step guidance for staying safe online.
          </p>
        </motion.div>

        {/* Assistant Selection */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          viewport={{ once: false, margin: "-100px" }}
          className="flex justify-center mb-8"
        >
          <div className="flex gap-4 p-2 bg-muted/30 rounded-xl">
            <Button
              variant={selectedAssistant === 'ai' ? 'default' : 'ghost'}
              onClick={() => setSelectedAssistant('ai')}
              className={`flex items-center gap-2 ${selectedAssistant === 'ai' ? 'gradient-bg text-white' : ''}`}
            >
              <Bot className="w-4 h-4" />
              Ai - Scam Detection
            </Button>
            <Button
              variant={selectedAssistant === 'haru' ? 'default' : 'ghost'}
              onClick={() => setSelectedAssistant('haru')}
              className={`flex items-center gap-2 ${selectedAssistant === 'haru' ? 'gradient-bg text-white' : ''}`}
            >
              <Heart className="w-4 h-4" />
              Haru - Recovery Support
            </Button>
          </div>
        </motion.div>

        {/* Main Chat Interface */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          viewport={{ once: false, margin: "-50px" }}
        >
          <Card className="shadow-2xl max-w-4xl mx-auto">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-2xl flex items-center gap-3">
                  <div className={`w-8 h-8 rounded-lg ${assistantBgColor} flex items-center justify-center`}>
                    {React.createElement(assistantIcon, { className: `w-5 h-5 ${assistantColor}` })}
                  </div>
                  Chat with {assistantName}
                </CardTitle>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                  <span className="text-sm text-muted-foreground">Online</span>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <ChatInterface />
            </CardContent>
          </Card>
        </motion.div>

        {/* Bottom CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          viewport={{ once: false, margin: "-100px" }}
          className="text-center mt-12"
        >
          <p className="text-muted-foreground mb-4">
            Need more help? Try our full scanner or recovery tools.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" variant="outline" className="gradient-border">
              <Shield className="w-4 h-4 mr-2" />
              Try Scanner
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
            <Button size="lg" className="gradient-bg text-white">
              <MessageCircle className="w-4 h-4 mr-2" />
              Get Recovery Help
              <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </div>
        </motion.div>
      </div>
    </section>
  )
} 
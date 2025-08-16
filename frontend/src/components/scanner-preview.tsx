"use client"

import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Link2, 
  MessageSquare, 
  Upload, 
  Bot,
  Shield,
  AlertTriangle,
  CheckCircle,
  ArrowRight,
  Send,
  Paperclip
} from 'lucide-react'

// Mock chat messages
const mockChatMessages = [
  {
    id: 1,
    sender: 'ai',
    message: "Hi! I'm Ai, your scam detection assistant. Paste a suspicious link or tell me what happened.",
    timestamp: '2:30 PM'
  },
  {
    id: 2,
    sender: 'user',
    message: "I received this link on Facebook: bit.ly/free-phone-win",
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

const mockScanResult = {
  url: "bit.ly/suspicious-link",
  score: 92,
  verdict: "malicious" as const,
  confidence: 96,
  reasons: [
    "Domain registered less than 24 hours ago",
    "URL structure matches known phishing patterns", 
    "No valid SSL certificate",
    "Flagged by 3+ security vendors"
  ],
  recommendations: [
    "Do not click this link",
    "Report to Facebook/platform where you found it",
    "Delete the message containing this link",
    "Warn friends who may have received similar messages"
  ]
}

export const ScannerPreview = () => {
  const [activeTab, setActiveTab] = useState("scan")
  const [chatMessage, setChatMessage] = useState("")

  const ChatInterface = () => (
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
                : 'bg-background border'
            }`}>
              {msg.sender === 'ai' && (
                <div className="flex items-center gap-2 mb-1">
                  <Bot className="w-4 h-4" />
                  <span className="text-xs font-medium">Ai</span>
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
          placeholder="Type your message..."
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

  const ScanInterface = () => (
    <div className="space-y-6">
      {/* URL Input */}
      <div className="space-y-4">
        <div className="flex gap-2">
          <Input
            placeholder="https://suspicious-link.com"
            className="flex-1"
          />
          <Button className="gradient-bg text-white">
            Analyze
          </Button>
        </div>
      </div>

      {/* Mock Result */}
      <Card className="border-2 border-red-200 bg-red-50">
        <CardHeader className="pb-3">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-red-600" />
            <CardTitle className="text-lg text-red-600">
              Malicious Link Detected
            </CardTitle>
            <Badge variant="outline" className="ml-auto text-red-600 border-red-300">
              {mockScanResult.confidence}% confident
            </Badge>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* Risk Score */}
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium">Risk Score</span>
                <span className="text-sm text-red-600 font-bold">{mockScanResult.score}/100</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="h-2 bg-red-500 rounded-full transition-all duration-1000"
                  style={{ width: `${mockScanResult.score}%` }}
                />
              </div>
            </div>

            {/* Analysis */}
            <div>
              <h4 className="font-medium text-sm mb-2">Why this link is dangerous:</h4>
              <ul className="space-y-1">
                {mockScanResult.reasons.map((reason, index) => (
                  <li key={index} className="text-sm text-red-700 flex items-start gap-2">
                    <span className="w-1 h-1 bg-red-500 rounded-full mt-2 flex-shrink-0" />
                    {reason}
                  </li>
                ))}
              </ul>
            </div>

            {/* Actions */}
            <div className="flex gap-2 pt-2">
              <Button variant="destructive" size="sm">
                Report Scam
              </Button>
              <Button variant="outline" size="sm">
                Send to Haru
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )

  return (
    <section id="scanner" className="py-24 px-4 bg-gradient-to-b from-background to-muted/20">
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
            <Shield className="w-6 h-6 text-primary" />
            <Badge variant="outline">Try It Now</Badge>
          </div>
          
          <h2 className="text-4xl lg:text-5xl font-bold mb-6 relative">
            <span className="text-primary relative inline-block">
              Interactive Scanner
              <div className="absolute -bottom-1 left-0 w-full h-0.5 bg-gradient-to-r from-primary to-secondary rounded-full"></div>
            </span>{' '}
            Preview
          </h2>
          
          <p className="text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            Experience our AI-powered scam detection in action. Test suspicious links 
            or chat with our virtual assistants for instant help.
          </p>
        </motion.div>

        {/* Main Interface */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          viewport={{ once: false, margin: "-50px" }}
        >
          <Card className="shadow-2xl">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-2xl">PhishGuard Scanner</CardTitle>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                  <span className="text-sm text-muted-foreground">Live</span>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                <TabsList className="grid w-full grid-cols-4">
                  <TabsTrigger value="scan" className="flex items-center gap-2">
                    <Link2 className="w-4 h-4" />
                    <span className="hidden sm:inline">Scan Link</span>
                  </TabsTrigger>
                  <TabsTrigger value="message" className="flex items-center gap-2">
                    <MessageSquare className="w-4 h-4" />
                    <span className="hidden sm:inline">Paste Message</span>
                  </TabsTrigger>
                  <TabsTrigger value="upload" className="flex items-center gap-2">
                    <Upload className="w-4 h-4" />
                    <span className="hidden sm:inline">Upload Screenshot</span>
                  </TabsTrigger>
                  <TabsTrigger value="chat" className="flex items-center gap-2">
                    <Bot className="w-4 h-4" />
                    <span className="hidden sm:inline">Chat (Ai/Haru)</span>
                  </TabsTrigger>
                </TabsList>
                
                <TabsContent value="scan" className="mt-6">
                  <ScanInterface />
                </TabsContent>
                
                <TabsContent value="message" className="mt-6">
                  <div className="space-y-4">
                    <textarea 
                      className="w-full h-32 p-3 border rounded-md resize-none"
                      placeholder="Paste the suspicious message you received here..."
                    />
                    <Button className="gradient-bg text-white">
                      Analyze Message
                    </Button>
                  </div>
                </TabsContent>
                
                <TabsContent value="upload" className="mt-6">
                  <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-8 text-center">
                    <Upload className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                    <p className="text-muted-foreground mb-4">
                      Drop screenshot here or click to upload
                    </p>
                    <Button variant="outline">
                      Choose File
                    </Button>
                  </div>
                </TabsContent>
                
                <TabsContent value="chat" className="mt-6">
                  <ChatInterface />
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        </motion.div>

        {/* Bottom CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          viewport={{ once: false, margin: "-100px" }}
          className="text-center mt-12"
        >
          <p className="text-muted-foreground mb-4">
            Ready to protect yourself from scams?
          </p>
          <Button size="lg" className="gradient-bg text-white">
            Start Free Protection
            <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
        </motion.div>
      </div>
    </section>
  )
} 
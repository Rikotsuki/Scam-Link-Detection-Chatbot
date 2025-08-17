"use client"

import React, { useState, useEffect } from 'react'
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
  Paperclip,
  Heart,
  Loader2,
  Copy,
  Share2,
  Bookmark,
  Clock
} from 'lucide-react'
import { useLoading } from '@/hooks/use-loading'
import { phishguardApi } from '@/lib/api'

// Mock chat messages for Ai (dark mode)
const mockChatMessagesAi = [
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
    message: "I received this link on Facebook: bit.ly/free-phone-win",
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
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [url, setUrl] = useState("")
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisResult, setAnalysisResult] = useState<any>(null)
  const [chatHistory, setChatHistory] = useState<any[]>([])
  const [error, setError] = useState<string | null>(null)
  const { isLoading } = useLoading()

  // Detect dark mode
  useEffect(() => {
    const checkDarkMode = () => {
      // Check multiple ways to detect dark mode
      const htmlHasDark = document.documentElement.classList.contains('dark')
      const bodyHasDark = document.body.classList.contains('dark')
      const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      
      // Check for other common theme class names
      const htmlHasDarkTheme = document.documentElement.classList.contains('dark-theme')
      const bodyHasDarkTheme = document.body.classList.contains('dark-theme')
      const htmlHasDarkMode = document.documentElement.classList.contains('dark-mode')
      const bodyHasDarkMode = document.body.classList.contains('dark-mode')
      
      // Check data attributes
      const htmlDataTheme = document.documentElement.getAttribute('data-theme')
      const bodyDataTheme = document.body.getAttribute('data-theme')
      
      // Check computed styles
      const computedStyle = getComputedStyle(document.documentElement)
      const backgroundColor = computedStyle.backgroundColor
      const isDarkByColor = backgroundColor.includes('rgb(10, 16, 26)') || 
                           backgroundColor.includes('rgb(17, 25, 39)') ||
                           backgroundColor.includes('black')
      
      // Combine all checks
      const isDark = htmlHasDark || bodyHasDark || systemPrefersDark || 
                    htmlHasDarkTheme || bodyHasDarkTheme || 
                    htmlHasDarkMode || bodyHasDarkMode ||
                    htmlDataTheme === 'dark' || bodyDataTheme === 'dark' ||
                    isDarkByColor
      
      console.log('Theme check:', { 
        htmlHasDark, bodyHasDark, systemPrefersDark,
        htmlHasDarkTheme, bodyHasDarkTheme,
        htmlHasDarkMode, bodyHasDarkMode,
        htmlDataTheme, bodyDataTheme,
        backgroundColor, isDarkByColor,
        isDark 
      })
      
      // Only update if the value actually changed to prevent unnecessary re-renders
      setIsDarkMode(prev => {
        if (prev !== isDark) {
          console.log('Theme changed from', prev, 'to', isDark)
          return isDark
        }
        return prev
      })
    }

    // Check immediately
    checkDarkMode()

    // Listen for theme changes on the html element
    const observer = new MutationObserver(checkDarkMode)
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['class', 'data-theme']
    })

    // Also listen for body class changes
    observer.observe(document.body, {
      attributes: true,
      attributeFilter: ['class', 'data-theme']
    })

    // Listen for system theme changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQuery.addEventListener('change', checkDarkMode)

    return () => {
      observer.disconnect()
      mediaQuery.removeEventListener('change', checkDarkMode)
    }
  }, [])

  // Get the appropriate chat messages and assistant info based on theme
  const isAi = isDarkMode // Ai in dark mode, Haru in light mode
  const mockChatMessages = isAi ? mockChatMessagesAi : mockChatMessagesHaru
  const assistantName = isAi ? 'Ai' : 'Haru'
  const assistantIcon = isAi ? Bot : Heart
  const assistantColor = isAi ? 'text-pink-500' : 'text-blue-500'
  const assistantBgColor = isAi ? 'bg-pink-500/10' : 'bg-blue-500/10'

  console.log('Current state:', { isDarkMode, isAi, assistantName, htmlClass: document.documentElement.className })

  const handleAnalyzeUrl = async () => {
    if (!url.trim()) return;

    setIsAnalyzing(true);
    setAnalysisResult(null);
    setError(null);

    try {
      const result = await phishguardApi.analyzeUrl(url);
      
      if (result.error) {
        setError(result.error);
      } else {
        setAnalysisResult(result.data);
      }
    } catch (error) {
      setError('Network error. Please try again.');
      console.error('Analysis error:', error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleChat = async () => {
    if (!chatMessage.trim()) return;

    const userMessage = chatMessage;
    setChatMessage('');

    try {
      const result = await phishguardApi.chatWithBot(userMessage);
      
      if (result.data) {
        const newChatMessage = {
          id: Date.now().toString(),
          sender: 'user',
          message: userMessage,
          timestamp: new Date().toLocaleTimeString()
        };
        
        const aiResponse = {
          id: (Date.now() + 1).toString(),
          sender: isAi ? 'ai' : 'haru',
          message: result.data.response,
          timestamp: new Date().toLocaleTimeString(),
          confidence: result.data.confidence,
          suggestions: result.data.suggestions
        };
        
        setChatHistory(prev => [aiResponse, newChatMessage, ...prev]);
      }
    } catch (error) {
      console.error('Chat error:', error);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    // You could show a toast notification here
  };

  const getThreatLevelColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'high': return 'destructive';
      case 'medium': return 'secondary';
      case 'low': return 'default';
      default: return 'default';
    }
  };

  const getThreatLevelIcon = (level: string) => {
    switch (level.toLowerCase()) {
      case 'high': return <AlertTriangle className="w-4 h-4" />;
      case 'medium': return <Clock className="w-4 h-4" />;
      case 'low': return <CheckCircle className="w-4 h-4" />;
      default: return <Shield className="w-4 h-4" />;
    }
  };

  const ChatInterface = () => {
    const AssistantIcon = assistantIcon

    return (
    <div className="h-96 flex flex-col">
      {/* Chat messages */}
      <div className="flex-1 p-4 space-y-4 overflow-y-auto bg-muted/20 rounded-lg mb-4">
        {/* Show initial message */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex justify-start"
        >
          <div className={`max-w-[80%] p-3 rounded-lg bg-background border ${assistantBgColor}`}>
            <div className="flex items-center gap-2 mb-1">
              <AssistantIcon className={`w-4 h-4 ${assistantColor}`} />
              <span className="text-xs font-medium">{assistantName}</span>
            </div>
            <p className="text-sm">
              Hi! I'm {assistantName}, your scam detection assistant. Paste a suspicious link or tell me what happened.
            </p>
            <p className="text-xs opacity-70 mt-1">{new Date().toLocaleTimeString()}</p>
          </div>
        </motion.div>

        {/* Show chat history */}
        {chatHistory.map((msg) => (
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
              {msg.suggestions && msg.suggestions.length > 0 && (
                <div className="mt-2">
                  <p className="text-xs text-muted-foreground mb-1">Suggestions:</p>
                  <div className="flex flex-wrap gap-1">
                    {msg.suggestions.map((suggestion: string, index: number) => (
                      <Badge key={index} variant="secondary" className="text-xs">
                        {suggestion}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
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
          onKeyPress={(e) => e.key === 'Enter' && handleChat()}
          className="flex-1"
        />
        <Button size="icon" variant="outline">
          <Paperclip className="w-4 h-4" />
        </Button>
        <Button 
          size="icon" 
          className="gradient-bg text-white"
          onClick={handleChat}
          disabled={!chatMessage.trim()}
        >
          <Send className="w-4 h-4" />
        </Button>
      </div>
    </div>
  )
  }

  const ScanInterface = () => (
    <div className="space-y-6">
      {/* URL Input */}
      <div className="space-y-4">
        <div className="flex gap-2">
          <Input
            placeholder="https://suspicious-link.com"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleAnalyzeUrl()}
            className="flex-1"
          />
          <Button 
            className="gradient-bg text-white"
            onClick={handleAnalyzeUrl}
            disabled={isAnalyzing || !url.trim()}
          >
            {isAnalyzing ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Analyzing...
              </>
            ) : (
              'Analyze'
            )}
          </Button>
        </div>

        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="p-3 bg-destructive/10 border border-destructive/20 rounded-lg flex items-center gap-2 text-destructive"
          >
            <AlertTriangle className="w-4 h-4" />
            <span className="text-sm">{error}</span>
          </motion.div>
        )}
      </div>

      {/* Analysis Result */}
      {analysisResult && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          <Card className={`border-2 ${
            analysisResult.is_suspicious 
              ? 'border-red-200 bg-red-50' 
              : 'border-green-200 bg-green-50'
          }`}>
            <CardHeader className="pb-3">
              <div className="flex items-center gap-2">
                {getThreatLevelIcon(analysisResult.threat_level)}
                <CardTitle className={`text-lg ${
                  analysisResult.is_suspicious ? 'text-red-600' : 'text-green-600'
                }`}>
                  {analysisResult.is_suspicious ? 'Suspicious Link Detected' : 'Safe Link'}
                </CardTitle>
                <Badge 
                  variant={getThreatLevelColor(analysisResult.threat_level) as any} 
                  className="ml-auto"
                >
                  {(analysisResult.confidence * 100).toFixed(1)}% confident
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {/* Analysis Message */}
                <div>
                  <p className="font-medium mb-2">{analysisResult.message}</p>
                  <div className="text-sm text-muted-foreground">
                    Analysis completed in {analysisResult.analysis_time.toFixed(2)}s
                  </div>
                </div>

                {/* Warnings */}
                {analysisResult.warnings && analysisResult.warnings.length > 0 && (
                  <div>
                    <h4 className="font-medium text-sm mb-2 text-destructive">Warnings:</h4>
                    <ul className="space-y-1">
                      {analysisResult.warnings.map((warning: string, index: number) => (
                        <li key={index} className="text-sm text-destructive flex items-start gap-2">
                          <span className="w-1 h-1 bg-red-500 rounded-full mt-2 flex-shrink-0" />
                          {warning}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Actions */}
                <div className="flex gap-2 pt-2">
                  <Button variant="outline" size="sm" onClick={() => copyToClipboard(url)}>
                    <Copy className="w-3 h-3 mr-1" />
                    Copy URL
                  </Button>
                  <Button variant="outline" size="sm">
                    <Share2 className="w-3 h-3 mr-1" />
                    Share Report
                  </Button>
                  <Button variant="outline" size="sm">
                    <Bookmark className="w-3 h-3 mr-1" />
                    Save
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}
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
                    <span className="hidden sm:inline">Chat (AI)</span>
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
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="gradient-bg text-white" asChild>
              <a href="/register">
                Get Started Free
                <ArrowRight className="w-4 h-4 ml-2" />
              </a>
            </Button>
            <Button size="lg" variant="outline" asChild>
              <a href="/login">
                Sign In
              </a>
            </Button>
          </div>
        </motion.div>
      </div>
    </section>
  )
} 
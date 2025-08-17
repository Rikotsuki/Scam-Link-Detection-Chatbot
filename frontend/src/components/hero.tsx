"use client"

import React, { useState, Suspense } from 'react'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import { Shield, Search, MessageCircle, AlertTriangle, CheckCircle, XCircle, Bot, Heart, Loader2, ArrowRight } from 'lucide-react'

import { DualImageAvatar } from '@/components/image-avatar'
import { GradientAnimatedDottedLine } from '@/components/animated-dotted-line'
import { useLoading } from '@/hooks/use-loading'

// Scanner Result Component
interface ScanResult {
  score: number
  verdict: 'safe' | 'suspicious' | 'malicious'
  reasons: string[]
  confidence: number
}

const ScanResultCard = ({ result }: { result: ScanResult }) => {
  const getVerdictColor = (verdict: string) => {
    switch (verdict) {
      case 'safe': return 'text-green-600 border-green-200 bg-green-50 dark:text-green-400 dark:border-green-800 dark:bg-green-950'
      case 'suspicious': return 'text-yellow-600 border-yellow-200 bg-yellow-50 dark:text-yellow-400 dark:border-yellow-800 dark:bg-yellow-950'
      case 'malicious': return 'text-red-600 border-red-200 bg-red-50 dark:text-red-400 dark:border-red-800 dark:bg-red-950'
      default: return 'text-gray-600 border-gray-200 bg-gray-50 dark:text-gray-400 dark:border-gray-800 dark:bg-gray-950'
    }
  }

  const getVerdictIcon = (verdict: string) => {
    switch (verdict) {
      case 'safe': return <CheckCircle className="w-5 h-5" />
      case 'suspicious': return <AlertTriangle className="w-5 h-5" />
      case 'malicious': return <XCircle className="w-5 h-5" />
      default: return <AlertTriangle className="w-5 h-5" />
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      role="status"
      aria-live="polite"
    >
      <Card className={`border-2 ${getVerdictColor(result.verdict)}`}>
        <CardHeader className="pb-3">
          <div className="flex items-center gap-2">
            {getVerdictIcon(result.verdict)}
            <CardTitle className="text-lg capitalize">
              {result.verdict} Link
            </CardTitle>
            <Badge variant="outline" className="ml-auto">
              {result.confidence}% confident
            </Badge>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div>
              <h4 className="font-medium text-sm mb-2">Risk Score</h4>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full transition-all duration-500 ${
                    result.score <= 30 ? 'bg-green-500' : 
                    result.score <= 70 ? 'bg-yellow-500' : 'bg-red-500'
                  }`}
                  style={{ width: `${result.score}%` }}
                />
              </div>
              <p className="text-xs text-muted-foreground mt-1">{result.score}/100</p>
            </div>
            
            <div>
              <h4 className="font-medium text-sm mb-2">Analysis</h4>
              <ul className="space-y-1">
                {result.reasons.map((reason, index) => (
                  <li key={index} className="text-sm text-muted-foreground flex items-start gap-2">
                    <span className="w-1 h-1 bg-current rounded-full mt-2 flex-shrink-0" />
                    {reason}
                  </li>
                ))}
              </ul>
            </div>

            {result.verdict === 'malicious' && (
              <div className="flex gap-2 pt-2">
                <Button variant="destructive" size="sm">
                  Report Scam
                </Button>
                <Button variant="outline" size="sm">
                  Get Recovery Steps
                </Button>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}

// Main Hero Component
export const Hero = () => {
  const [scanUrl, setScanUrl] = useState('')
  const [isScanning, setIsScanning] = useState(false)
  const [scanResult, setScanResult] = useState<ScanResult | null>(null)
  const [showChatAi, setShowChatAi] = useState(false)
  const [showChatHaru, setShowChatHaru] = useState(false)
  const { isLoading } = useLoading()

  const handleScan = async () => {
    if (!scanUrl.trim()) return
    
    setIsScanning(true)
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Mock result based on URL patterns
    const mockResult: ScanResult = scanUrl.includes('suspicious') || scanUrl.includes('scam') ? {
      score: 85,
      verdict: 'malicious',
      reasons: [
        'Domain recently registered (less than 30 days)',
        'Suspicious URL structure detected',
        'Similar to known phishing patterns',
        'No HTTPS security certificate'
      ],
      confidence: 94
    } : {
      score: 15,
      verdict: 'safe',
      reasons: [
        'Legitimate domain with long history',
        'Valid SSL certificate',
        'No malware detected',
        'Clean reputation score'
      ],
      confidence: 96
    }

    setScanResult(mockResult)
    setIsScanning(false)
  }

  const openAiChat = () => {
    setShowChatAi(true)
    console.log('Analytics: hero_ai_chat_opened')
  }

  const openHaruChat = () => {
    setShowChatHaru(true)
    console.log('Analytics: hero_haru_chat_opened')
  }

  const handleScanClick = () => {
    handleScan()
    console.log('Analytics: hero_scan_clicked')
  }

  return (
    <section className="relative min-h-screen flex items-center justify-center px-4 py-16 overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-background to-secondary/5" />
      
      {/* Hero-specific background animations */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          className="absolute top-1/4 left-1/4 w-32 h-32 bg-blue-500/5 rounded-full blur-3xl"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.3, 0.6, 0.3],
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
        <motion.div
          className="absolute bottom-1/4 right-1/4 w-40 h-40 bg-pink-500/5 rounded-full blur-3xl"
          animate={{
            scale: [1.2, 1, 1.2],
            opacity: [0.4, 0.7, 0.4],
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 2
          }}
        />
        <motion.div
          className="absolute top-1/2 left-1/2 w-24 h-24 bg-purple-500/5 rounded-full blur-2xl"
          animate={{
            scale: [1, 1.1, 1],
            opacity: [0.2, 0.5, 0.2],
          }}
          transition={{
            duration: 12,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 4
          }}
        />
      </div>
      
      <div className="relative z-10 max-w-7xl mx-auto grid lg:grid-cols-2 gap-12 items-center">
        {/* Left Content */}
        <motion.div 
          initial={{ opacity: 0, x: -50 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: false, margin: "-100px" }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="space-y-8 order-1 lg:order-1"
        >
          <div className="space-y-6">
            <motion.h1 
              className="text-4xl sm:text-5xl lg:text-7xl font-bold tracking-tight animate-fade-in-up relative text-center lg:text-left"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: false, margin: "-100px" }}
              transition={{ duration: 0.8, delay: 0.2 }}
            >
              <span className="text-foreground relative">
                PhishGuard
                <div className="absolute -bottom-2 left-0 w-full h-1 bg-gradient-to-r from-primary via-secondary to-primary rounded-full"></div>
              </span>
            </motion.h1>
            
            <motion.p 
              className="text-lg sm:text-xl lg:text-2xl text-muted-foreground max-w-2xl text-center lg:text-left mx-auto lg:mx-0"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: false, margin: "-100px" }}
              transition={{ duration: 0.8, delay: 0.4 }}
            >
              Instantly check links. Recover accounts. Stay safe.
            </motion.p>
            
            <motion.p 
              className="text-sm sm:text-base lg:text-lg text-muted-foreground max-w-2xl text-center lg:text-left mx-auto lg:mx-0"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: false, margin: "-100px" }}
              transition={{ duration: 0.8, delay: 0.6 }}
            >
              AI-powered scam detection and step-by-step recovery guidance for Myanmar. 
              Simple English. Free & anonymous.
            </motion.p>
          </div>

          {/* Interactive Dashboard */}
          <motion.div 
            className="space-y-6"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: false, margin: "-100px" }}
            transition={{ duration: 0.8, delay: 0.8 }}
          >
            {/* Protection Stats Dashboard */}
            <Card className="p-6 border-border/40 dark:border-border/60 bg-gradient-to-br from-background via-background/95 to-primary/5 backdrop-blur-sm">
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-xl font-bold text-foreground">Protection Dashboard</h3>
                    <p className="text-muted-foreground text-sm">Real-time security insights</p>
                  </div>
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                    className="w-10 h-10 rounded-full bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center"
                  >
                    <Shield className="w-5 h-5 text-white" />
                  </motion.div>
                </div>
                
                {/* Stats Grid */}
                <div className="grid grid-cols-3 gap-4">
                  <motion.div 
                    className="text-center p-4 rounded-xl bg-gradient-to-br from-green-500/10 to-green-600/10 border border-green-500/20"
                    whileHover={{ scale: 1.05 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    <motion.div 
                      className="text-2xl font-bold text-green-600 mb-1"
                      animate={{ scale: [1, 1.1, 1] }}
                      transition={{ duration: 2, repeat: Infinity }}
                    >
                      99.9%
                    </motion.div>
                    <div className="text-xs text-muted-foreground">Detection Rate</div>
                  </motion.div>
                  
                  <motion.div 
                    className="text-center p-4 rounded-xl bg-gradient-to-br from-blue-500/10 to-blue-600/10 border border-blue-500/20"
                    whileHover={{ scale: 1.05 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    <motion.div 
                      className="text-2xl font-bold text-blue-600 mb-1"
                      animate={{ scale: [1, 1.1, 1] }}
                      transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
                    >
                      &lt;1s
                    </motion.div>
                    <div className="text-xs text-muted-foreground">Response Time</div>
                  </motion.div>
                  
                  <motion.div 
                    className="text-center p-4 rounded-xl bg-gradient-to-br from-purple-500/10 to-purple-600/10 border border-purple-500/20"
                    whileHover={{ scale: 1.05 }}
                    transition={{ type: "spring", stiffness: 300 }}
                  >
                    <motion.div 
                      className="text-2xl font-bold text-purple-600 mb-1"
                      animate={{ scale: [1, 1.1, 1] }}
                      transition={{ duration: 2, repeat: Infinity, delay: 1 }}
                    >
                      24/7
                    </motion.div>
                    <div className="text-xs text-muted-foreground">Available</div>
                  </motion.div>
                </div>
                
                {/* Quick Actions */}
                <div className="grid grid-cols-2 gap-3">
                  <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                    <Button 
                      onClick={openAiChat} 
                      className="w-full h-16 justify-start bg-gradient-to-r from-pink-500 to-pink-600 text-white shadow-lg hover:shadow-xl group"
                    >
                      <div className="flex items-center gap-3">
                        <div className="w-12 h-12 rounded-xl bg-white/20 flex items-center justify-center group-hover:scale-110 transition-transform">
                          <Bot className="w-6 h-6 text-white" />
                        </div>
                        <div className="text-left">
                          <div className="font-semibold">Start with Ai</div>
                          <div className="text-xs opacity-90">Link Analysis & Detection</div>
                        </div>
                      </div>
                    </Button>
                  </motion.div>
                  
                  <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                    <Button 
                      onClick={openHaruChat} 
                      className="w-full h-16 justify-start bg-gradient-to-r from-blue-500 to-blue-600 text-white shadow-lg hover:shadow-xl group"
                    >
                      <div className="flex items-center gap-3">
                        <div className="w-12 h-12 rounded-xl bg-white/20 flex items-center justify-center group-hover:scale-110 transition-transform">
                          <Heart className="w-6 h-6 text-white" />
                        </div>
                        <div className="text-left">
                          <div className="font-semibold">Talk to Haru</div>
                          <div className="text-xs opacity-90">Recovery & Support</div>
                        </div>
                      </div>
                  </Button>
                  </motion.div>
                </div>
              </div>
            </Card>

            {/* Interactive Feature Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: false, margin: "-50px" }}
                transition={{ delay: 0.2 }}
                whileHover={{ scale: 1.02 }}
              >
                <Card className="p-6 h-full bg-gradient-to-br from-primary/5 to-primary/10 border-primary/20 hover:border-primary/40 transition-all duration-300 cursor-pointer group">
                  <div className="space-y-3">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-primary to-primary/80 flex items-center justify-center group-hover:scale-110 transition-transform">
                        <Search className="w-5 h-5 text-white" />
                      </div>
                      <h4 className="font-semibold text-foreground">Instant Scanning</h4>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      Get immediate threat analysis on any link with our advanced AI detection engine
                    </p>
                    <div className="flex items-center gap-2 text-xs text-primary font-medium">
                      <span>Try it now</span>
                      <ArrowRight className="w-3 h-3" />
                    </div>
                  </div>
                </Card>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, x: 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: false, margin: "-50px" }}
                transition={{ delay: 0.4 }}
                whileHover={{ scale: 1.02 }}
              >
                <Card className="p-6 h-full bg-gradient-to-br from-secondary/5 to-secondary/10 border-secondary/20 hover:border-secondary/40 transition-all duration-300 cursor-pointer group">
                  <div className="space-y-3">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-secondary to-secondary/80 flex items-center justify-center group-hover:scale-110 transition-transform">
                        <MessageCircle className="w-5 h-5 text-white" />
                      </div>
                      <h4 className="font-semibold text-foreground">Expert Guidance</h4>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      Get personalized help and step-by-step recovery assistance from our AI guardians
                    </p>
                    <div className="flex items-center gap-2 text-xs text-secondary font-medium">
                      <span>Get help</span>
                      <ArrowRight className="w-3 h-3" />
                    </div>
                  </div>
                </Card>
              </motion.div>
            </div>

            {/* Live Activity Feed */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: false, margin: "-50px" }}
              transition={{ delay: 0.2 }}
            >
              <Card className="p-4 border-border/40">
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h4 className="font-semibold text-sm">Recent Activity</h4>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                      <span className="text-xs text-muted-foreground">Live</span>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <motion.div 
                      className="flex items-center gap-3 p-2 rounded-lg bg-green-500/10"
                      initial={{ opacity: 0, x: -10 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: false, margin: "-50px" }}
                      transition={{ delay: 0.2 }}
                    >
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">247 threats blocked today</span>
                    </motion.div>
                    
                    <motion.div 
                      className="flex items-center gap-3 p-2 rounded-lg bg-blue-500/10"
                      initial={{ opacity: 0, x: -10 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: false, margin: "-50px" }}
                      transition={{ delay: 0.4 }}
                    >
                      <Bot className="w-4 h-4 text-blue-500" />
                      <span className="text-sm">AI guardians helped 1,234 users</span>
                    </motion.div>
                    
                    <motion.div 
                      className="flex items-center gap-3 p-2 rounded-lg bg-purple-500/10"
                      initial={{ opacity: 0, x: -10 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      viewport={{ once: false, margin: "-50px" }}
                      transition={{ delay: 0.6 }}
                    >
                      <Heart className="w-4 h-4 text-purple-500" />
                      <span className="text-sm">15 accounts successfully recovered</span>
                    </motion.div>
                  </div>
                </div>
              </Card>
            </motion.div>
          </motion.div>

          {/* Trust indicators */}
          <motion.div 
            className="flex items-center gap-4 text-sm text-muted-foreground"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: false, margin: "-100px" }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <div className="flex items-center gap-2">
              <Shield className="w-4 h-4" />
              <span>No personal data stored</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4" />
              <span>Reports are anonymized</span>
            </div>
          </motion.div>
        </motion.div>

        {/* Right Content - AI & Haru Avatars */}
        <motion.div 
          initial={{ opacity: 0, x: 50 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: false, margin: "-100px" }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="order-2 lg:order-2"
        >
          <Card className="p-4 sm:p-6 lg:p-8 shadow-2xl border-border/40 dark:border-border/60">
            <div className="text-center mb-4 sm:mb-6">
              <h3 className="text-base sm:text-lg font-semibold mb-2">Meet Your Guardians</h3>
              <p className="text-xs sm:text-sm text-muted-foreground">
                AI-powered assistants ready to protect and guide you
              </p>
            </div>
            
            <DualImageAvatar
              onAiClick={openAiChat}
              onHaruClick={openHaruChat}
            />

            {/* Guardian Info */}
            <div className="grid grid-cols-2 gap-3 sm:gap-4 mt-4 sm:mt-6">
              <div className="text-center p-2 sm:p-3 rounded-lg bg-pink-500/5 dark:bg-pink-500/10">
                <div className="flex items-center justify-center gap-1 sm:gap-2 mb-1 sm:mb-2">
                  <Bot className="w-3 h-3 sm:w-4 sm:h-4 text-pink-500" />
                  <span className="font-semibold text-xs sm:text-sm">Ai</span>
                </div>
                <p className="text-xs text-muted-foreground">Scam Detection</p>
              </div>
              <div className="text-center p-2 sm:p-3 rounded-lg bg-blue-500/5 dark:bg-blue-500/10">
                <div className="flex items-center justify-center gap-1 sm:gap-2 mb-1 sm:mb-2">
                  <Heart className="w-3 h-3 sm:w-4 sm:h-4 text-blue-500" />
                  <span className="font-semibold text-xs sm:text-sm">Haru</span>
                </div>
                <p className="text-xs text-muted-foreground">Recovery Support</p>
              </div>
            </div>
          </Card>
        </motion.div>
      </div>
    </section>
  )
} 
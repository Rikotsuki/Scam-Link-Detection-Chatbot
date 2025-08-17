'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Separator } from '@/components/ui/separator';
import { 
  Shield, 
  Search, 
  AlertTriangle, 
  CheckCircle, 
  XCircle, 
  Clock, 
  Zap,
  MessageCircle,
  Lightbulb,
  LogOut,
  User,
  Settings,
  BarChart3,
  History,
  ExternalLink,
  Copy,
  Share2,
  Bookmark,
  Flag,
  Eye,
  EyeOff
} from 'lucide-react';
import { phishguardApi } from '@/lib/api';

interface AnalysisResult {
  url: string;
  is_suspicious: boolean;
  threat_level: string;
  message: string;
  confidence: number;
  detection_methods: string[];
  warnings: string[];
  analysis_time: number;
}

interface ChatMessage {
  id: string;
  message: string;
  response: string;
  confidence: number;
  suggestions: string[];
  timestamp: string;
}

interface SafetyTip {
  id: string;
  tip: string;
  category: string;
}

export default function DashboardPage() {
  const [url, setUrl] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [chatMessage, setChatMessage] = useState('');
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [safetyTips, setSafetyTips] = useState<SafetyTip[]>([]);
  const [showTips, setShowTips] = useState(false);
  const [user, setUser] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check authentication
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (!token) {
      router.push('/login');
      return;
    }

    if (userData) {
      setUser(JSON.parse(userData));
    }

    // Load safety tips
    loadSafetyTips();
    setIsLoading(false);
  }, [router]);

  const loadSafetyTips = async () => {
    try {
      const result = await phishguardApi.getSafetyTips();
      if (result.data) {
        const tips = result.data.tips.map((tip, index) => ({
          id: `tip-${index}`,
          tip,
          category: 'General'
        }));
        setSafetyTips(tips);
      }
    } catch (error) {
      console.error('Failed to load safety tips:', error);
    }
  };

  const handleAnalyzeUrl = async () => {
    if (!url.trim()) return;

    setIsAnalyzing(true);
    setAnalysisResult(null);

    try {
      const result = await phishguardApi.analyzeUrl(url);
      
      if (result.error) {
        console.error('Analysis failed:', result.error);
        // You could show a toast notification here
      } else {
        setAnalysisResult(result.data || null);
      }
    } catch (error) {
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
        const newChatMessage: ChatMessage = {
          id: Date.now().toString(),
          message: userMessage,
          response: result.data.response,
          confidence: result.data.confidence,
          suggestions: result.data.suggestions,
          timestamp: new Date().toISOString()
        };
        
        setChatHistory(prev => [newChatMessage, ...prev]);
      }
    } catch (error) {
      console.error('Chat error:', error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    router.push('/');
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

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary/5 via-background to-secondary/5 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary/5 via-background to-secondary/5">
      {/* Header */}
      <header className="border-b bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-primary to-secondary rounded-xl flex items-center justify-center">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold">PhishGuard Dashboard</h1>
                <p className="text-sm text-muted-foreground">
                  Welcome back, {user?.firstName || 'User'}
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <Button variant="ghost" size="icon">
                <Settings className="w-4 h-4" />
              </Button>
              <Button variant="ghost" size="icon" onClick={handleLogout}>
                <LogOut className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* URL Scanner */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <Card className="shadow-lg border-0">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Search className="w-5 h-5" />
                    URL Scanner
                  </CardTitle>
                  <CardDescription>
                    Analyze any URL for phishing threats and security risks
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex gap-2">
                    <Input
                      type="url"
                      placeholder="Enter URL to analyze (e.g., https://example.com)"
                      value={url}
                      onChange={(e) => setUrl(e.target.value)}
                      className="flex-1"
                      onKeyPress={(e) => e.key === 'Enter' && handleAnalyzeUrl()}
                    />
                    <Button 
                      onClick={handleAnalyzeUrl} 
                      disabled={isAnalyzing || !url.trim()}
                      className="gradient-bg text-white"
                    >
                      {isAnalyzing ? (
                        <>
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                          Analyzing...
                        </>
                      ) : (
                        <>
                          <Zap className="w-4 h-4 mr-2" />
                          Scan
                        </>
                      )}
                    </Button>
                  </div>

                  {analysisResult && (
                    <motion.div
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      className="space-y-4 p-4 rounded-lg border"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          {getThreatLevelIcon(analysisResult.threat_level)}
                          <Badge variant={getThreatLevelColor(analysisResult.threat_level) as any}>
                            {analysisResult.threat_level.toUpperCase()} THREAT
                          </Badge>
                        </div>
                        <div className="text-sm text-muted-foreground">
                          Confidence: {(analysisResult.confidence * 100).toFixed(1)}%
                        </div>
                      </div>

                      <div>
                        <p className="font-medium mb-2">{analysisResult.message}</p>
                        <div className="text-sm text-muted-foreground">
                          Analysis completed in {analysisResult.analysis_time.toFixed(2)}s
                        </div>
                      </div>

                      {analysisResult.warnings.length > 0 && (
                        <div>
                          <h4 className="font-medium mb-2 text-destructive">Warnings:</h4>
                          <ul className="space-y-1">
                            {analysisResult.warnings.map((warning, index) => (
                              <li key={index} className="text-sm text-destructive flex items-center gap-2">
                                <AlertTriangle className="w-3 h-3" />
                                {warning}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      <div className="flex gap-2">
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
                    </motion.div>
                  )}
                </CardContent>
              </Card>
            </motion.div>

            {/* Chat Assistant */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <Card className="shadow-lg border-0">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <MessageCircle className="w-5 h-5" />
                    AI Assistant
                  </CardTitle>
                  <CardDescription>
                    Ask questions about phishing protection and get instant help
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex gap-2">
                    <Input
                      placeholder="Ask about phishing protection..."
                      value={chatMessage}
                      onChange={(e) => setChatMessage(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleChat()}
                      className="flex-1"
                    />
                    <Button onClick={handleChat} disabled={!chatMessage.trim()}>
                      Send
                    </Button>
                  </div>

                  {chatHistory.length > 0 && (
                    <div className="space-y-3 max-h-64 overflow-y-auto">
                      {chatHistory.map((chat) => (
                        <div key={chat.id} className="space-y-2">
                          <div className="flex justify-end">
                            <div className="bg-primary text-primary-foreground rounded-lg px-3 py-2 max-w-xs">
                              <p className="text-sm">{chat.message}</p>
                            </div>
                          </div>
                          <div className="flex justify-start">
                            <div className="bg-muted rounded-lg px-3 py-2 max-w-xs">
                              <p className="text-sm">{chat.response}</p>
                              {chat.suggestions.length > 0 && (
                                <div className="mt-2">
                                  <p className="text-xs text-muted-foreground mb-1">Suggestions:</p>
                                  <div className="flex flex-wrap gap-1">
                                    {chat.suggestions.map((suggestion, index) => (
                                      <Badge key={index} variant="secondary" className="text-xs">
                                        {suggestion}
                                      </Badge>
                                    ))}
                                  </div>
                                </div>
                              )}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            </motion.div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Stats */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
            >
              <Card className="shadow-lg border-0">
                <CardHeader>
                  <CardTitle className="text-lg">Quick Stats</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">URLs Scanned</span>
                    <span className="font-semibold">0</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">Threats Detected</span>
                    <span className="font-semibold text-destructive">0</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">Safe URLs</span>
                    <span className="font-semibold text-green-600">0</span>
                  </div>
                </CardContent>
              </Card>
            </motion.div>

            {/* Safety Tips */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
            >
              <Card className="shadow-lg border-0">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Lightbulb className="w-5 h-5" />
                    Safety Tips
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <Button 
                    variant="outline" 
                    className="w-full mb-3"
                    onClick={() => setShowTips(!showTips)}
                  >
                    {showTips ? 'Hide Tips' : 'Show Tips'}
                  </Button>
                  
                  {showTips && (
                    <div className="space-y-3">
                      {safetyTips.slice(0, 3).map((tip) => (
                        <div key={tip.id} className="p-3 bg-muted/50 rounded-lg">
                          <p className="text-sm">{tip.tip}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            </motion.div>

            {/* Quick Actions */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.5 }}
            >
              <Card className="shadow-lg border-0">
                <CardHeader>
                  <CardTitle className="text-lg">Quick Actions</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <Button variant="outline" className="w-full justify-start">
                    <History className="w-4 h-4 mr-2" />
                    View History
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <BarChart3 className="w-4 h-4 mr-2" />
                    Analytics
                  </Button>
                  <Button variant="outline" className="w-full justify-start">
                    <Flag className="w-4 h-4 mr-2" />
                    Report Scam
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
} 
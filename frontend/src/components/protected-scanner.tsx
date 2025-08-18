'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  Shield, 
  Search, 
  AlertTriangle, 
  CheckCircle, 
  Clock, 
  Zap,
  Loader2,
  Copy,
  Share2,
  Bookmark,
  Lock,
  LogIn,
  User
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

export default function ProtectedScanner() {
  const [url, setUrl] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [user, setUser] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check authentication
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (!token) {
      setIsLoading(false);
      return;
    }

    if (userData) {
      setUser(JSON.parse(userData));
    }
    setIsLoading(false);
  }, []);

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
        setAnalysisResult(result.data || null);
      }
    } catch (error) {
      setError('Network error. Please try again.');
      console.error('Analysis error:', error);
    } finally {
      setIsAnalyzing(false);
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

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!user) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-2xl mx-auto p-6"
      >
        <Card className="shadow-lg border-0">
          <CardHeader className="text-center">
            <div className="mx-auto w-16 h-16 bg-gradient-to-br from-primary to-secondary rounded-2xl flex items-center justify-center mb-4">
              <Lock className="w-8 h-8 text-white" />
            </div>
            <CardTitle className="text-2xl">Authentication Required</CardTitle>
            <CardDescription>
              You need to be logged in to access the URL scanner
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Alert>
              <AlertTriangle className="h-4 w-4" />
              <AlertDescription>
                The URL scanner is a protected feature. Please log in or create an account to continue.
              </AlertDescription>
            </Alert>
            
            <div className="flex flex-col sm:flex-row gap-3">
              <Button 
                className="flex-1 gradient-bg text-white" 
                onClick={() => router.push('/login')}
              >
                <LogIn className="w-4 h-4 mr-2" />
                Sign In
              </Button>
              <Button 
                variant="outline" 
                className="flex-1"
                onClick={() => router.push('/register')}
              >
                <User className="w-4 h-4 mr-2" />
                Create Account
              </Button>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-4xl mx-auto p-6"
    >
      <Card className="shadow-lg border-0">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Search className="w-5 h-5" />
                URL Scanner
              </CardTitle>
              <CardDescription>
                Welcome back, {user.firstName}! Analyze any URL for phishing threats and security risks
              </CardDescription>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
              <span className="text-sm text-muted-foreground">Connected</span>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* URL Input */}
          <div className="space-y-4">
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
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
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

            {error && (
              <Alert variant="destructive">
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}
          </div>

          {/* Analysis Result */}
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

              {analysisResult.warnings && analysisResult.warnings.length > 0 && (
                <div>
                  <h4 className="font-medium mb-2 text-destructive">Warnings:</h4>
                  <ul className="space-y-1">
                    {analysisResult.warnings.map((warning: string, index: number) => (
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

          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t">
            <div className="text-center">
              <div className="text-2xl font-bold text-primary">0</div>
              <div className="text-sm text-muted-foreground">URLs Scanned</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-destructive">0</div>
              <div className="text-sm text-muted-foreground">Threats Detected</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">0</div>
              <div className="text-sm text-muted-foreground">Safe URLs</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
} 
'use client';

import { useState } from 'react';
import { phishguardApi } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

export default function ApiExample() {
  const [url, setUrl] = useState('');
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [tips, setTips] = useState<string[]>([]);
  const [chatMessage, setChatMessage] = useState('');
  const [chatResponse, setChatResponse] = useState<any>(null);

  const handleAnalyzeUrl = async () => {
    if (!url.trim()) {
      setError('Please enter a URL to analyze');
      return;
    }

    setLoading(true);
    setError(null);
    setAnalysisResult(null);

    try {
      const result = await phishguardApi.analyzeUrl(url);
      
      if (result.error) {
        setError(result.error);
      } else {
        setAnalysisResult(result.data);
      }
    } catch (err) {
      setError('Failed to analyze URL');
    } finally {
      setLoading(false);
    }
  };

  const handleGetTips = async () => {
    try {
      const result = await phishguardApi.getSafetyTips();
      
      if (result.error) {
        setError(result.error);
      } else {
        setTips(result.data?.tips || []);
      }
    } catch (err) {
      setError('Failed to get safety tips');
    }
  };

  const handleChat = async () => {
    if (!chatMessage.trim()) {
      setError('Please enter a message');
      return;
    }

    try {
      const result = await phishguardApi.chatWithBot(chatMessage);
      
      if (result.error) {
        setError(result.error);
      } else {
        setChatResponse(result.data);
      }
    } catch (err) {
      setError('Failed to send chat message');
    }
  };

  const handleHealthCheck = async () => {
    try {
      const result = await phishguardApi.healthCheck();
      
      if (result.error) {
        setError(result.error);
      } else {
        alert(`Health Check: ${result.data?.status}\nPython Service: ${result.data?.python_service}`);
      }
    } catch (err) {
      setError('Failed to perform health check');
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>PhishGuard API Example</CardTitle>
          <CardDescription>
            Test the connection between your frontend and the Python microservices via Express.js
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Button onClick={handleHealthCheck} variant="outline">
            Health Check
          </Button>
          
          {error && (
            <div className="p-3 bg-red-100 border border-red-300 rounded text-red-700">
              {error}
            </div>
          )}
        </CardContent>
      </Card>

      {/* URL Analysis */}
      <Card>
        <CardHeader>
          <CardTitle>URL Analysis</CardTitle>
          <CardDescription>
            Analyze a URL for phishing threats
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex gap-2">
            <Input
              type="url"
              placeholder="Enter URL to analyze..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="flex-1"
            />
            <Button onClick={handleAnalyzeUrl} disabled={loading}>
              {loading ? 'Analyzing...' : 'Analyze'}
            </Button>
          </div>

          {analysisResult && (
            <div className="space-y-3 p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-2">
                <span className="font-semibold">Result:</span>
                <Badge variant={analysisResult.is_suspicious ? "destructive" : "default"}>
                  {analysisResult.threat_level}
                </Badge>
              </div>
              <p className="text-sm">{analysisResult.message}</p>
              <div className="text-xs text-gray-600">
                Confidence: {(analysisResult.confidence * 100).toFixed(1)}% | 
                Analysis Time: {analysisResult.analysis_time.toFixed(2)}s
              </div>
              {analysisResult.warnings.length > 0 && (
                <div>
                  <span className="text-xs font-semibold">Warnings:</span>
                  <ul className="text-xs text-red-600 mt-1">
                    {analysisResult.warnings.map((warning: string, index: number) => (
                      <li key={index}>• {warning}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Safety Tips */}
      <Card>
        <CardHeader>
          <CardTitle>Safety Tips</CardTitle>
          <CardDescription>
            Get digital safety tips
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Button onClick={handleGetTips} variant="outline">
            Get Safety Tips
          </Button>

          {tips.length > 0 && (
            <div className="space-y-2">
              {tips.map((tip, index) => (
                <div key={index} className="p-3 bg-blue-50 border border-blue-200 rounded">
                  <span className="text-sm">{tip}</span>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Chat */}
      <Card>
        <CardHeader>
          <CardTitle>Chat with Bot</CardTitle>
          <CardDescription>
            Ask the PhishGuard bot for help
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex gap-2">
            <Input
              placeholder="Ask me about phishing protection..."
              value={chatMessage}
              onChange={(e) => setChatMessage(e.target.value)}
              className="flex-1"
            />
            <Button onClick={handleChat}>
              Send
            </Button>
          </div>

          {chatResponse && (
            <div className="space-y-3 p-4 bg-green-50 border border-green-200 rounded-lg">
              <p className="text-sm">{chatResponse.response}</p>
              <div className="text-xs text-gray-600">
                Confidence: {(chatResponse.confidence * 100).toFixed(1)}%
              </div>
              {chatResponse.suggestions.length > 0 && (
                <div>
                  <span className="text-xs font-semibold">Suggestions:</span>
                  <ul className="text-xs text-gray-600 mt-1">
                    {chatResponse.suggestions.map((suggestion: string, index: number) => (
                      <li key={index}>• {suggestion}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
} 
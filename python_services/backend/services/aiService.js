import axios from 'axios';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

class AIService {
  constructor() {
    this.baseURL = process.env.AI_SERVICE_URL || 'http://localhost:8000';
    this.apiKey = process.env.AI_SERVICE_API_KEY;
  }

  // Initialize axios instance with default config
  get axiosInstance() {
    return axios.create({
      baseURL: this.baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`,
      },
    });
  }

  /**
   * Analyze URL for phishing threats
   */
  async analyzeUrl(url, userId = null) {
    try {
      const startTime = Date.now();
      
      // Call Python AI service
      const response = await this.axiosInstance.post('/analyze', {
        url,
        user_id: userId,
        timestamp: new Date().toISOString(),
      });

      const responseTime = Date.now() - startTime;

      // Store detection history in PostgreSQL
      await this.logDetection(url, response.data, responseTime, userId);

      return {
        success: true,
        data: response.data,
        responseTime,
      };
    } catch (error) {
      console.error('AI Service Error:', error.message);
      
      // Log error in database
      await this.logApiError('url_analysis', error.message);
      
      return {
        success: false,
        error: error.response?.data?.detail || 'AI service unavailable',
        fallback: await this.getFallbackAnalysis(url),
      };
    }
  }

  /**
   * Chat with AI chatbot
   */
  async chatWithBot(message, sessionId, userId = null) {
    try {
      const startTime = Date.now();
      
      // Call Python AI service
      const response = await this.axiosInstance.post('/chat', {
        message,
        session_id: sessionId,
        user_id: userId,
        timestamp: new Date().toISOString(),
      });

      const responseTime = Date.now() - startTime;

      // Store chat message in PostgreSQL
      await this.storeChatMessage(sessionId, 'user', message, userId);
      await this.storeChatMessage(sessionId, 'bot', response.data.response, userId, responseTime);

      return {
        success: true,
        data: response.data,
        responseTime,
      };
    } catch (error) {
      console.error('Chat Service Error:', error.message);
      
      // Log error and return fallback response
      await this.logApiError('chat', error.message);
      
      return {
        success: false,
        error: 'Chat service unavailable',
        fallback: await this.getFallbackChatResponse(message),
      };
    }
  }

  /**
   * Report scam URL
   */
  async reportScam(url, description, userId = null) {
    try {
      // Call Python AI service
      const response = await this.axiosInstance.post('/report', {
        url,
        description,
        user_id: userId,
        timestamp: new Date().toISOString(),
      });

      // Store report in PostgreSQL
      await this.storeUserReport(url, description, userId);

      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      console.error('Report Service Error:', error.message);
      
      // Store report locally even if AI service fails
      await this.storeUserReport(url, description, userId);
      
      return {
        success: false,
        error: 'Report service unavailable, but report saved locally',
      };
    }
  }

  /**
   * Get safety tips from AI knowledge base
   */
  async getSafetyTips(category = null) {
    try {
      const response = await this.axiosInstance.get('/tips', {
        params: { category },
      });

      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      console.error('Tips Service Error:', error.message);
      
      // Return cached tips from PostgreSQL
      return {
        success: false,
        error: 'Tips service unavailable',
        fallback: await this.getCachedTips(category),
      };
    }
  }

  /**
   * Get threat intelligence summary
   */
  async getThreatIntelligence() {
    try {
      const response = await this.axiosInstance.get('/intelligence/summary');
      
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      console.error('Intelligence Service Error:', error.message);
      
      return {
        success: false,
        error: 'Intelligence service unavailable',
        fallback: await this.getCachedIntelligence(),
      };
    }
  }

  /**
   * Store detection history in PostgreSQL
   */
  async logDetection(url, analysisResult, responseTime, userId = null) {
    try {
      const urlHash = this.hashUrl(url);
      
      await prisma.detectionHistory.create({
        data: {
          urlHash,
          originalUrl: url,
          threatLevel: analysisResult.threat_level || 'unknown',
          confidence: parseFloat(analysisResult.confidence || 0),
          detectionMethods: analysisResult.detection_methods || [],
          isSuspicious: analysisResult.is_suspicious || false,
          responseTimeMs: responseTime,
          aiPrediction: analysisResult,
        },
      });
    } catch (error) {
      console.error('Error logging detection:', error);
    }
  }

  /**
   * Store user report in PostgreSQL
   */
  async storeUserReport(url, description, userId = null) {
    try {
      const urlHash = this.hashUrl(url);
      
      await prisma.userReport.create({
        data: {
          urlHash,
          originalUrl: url,
          description,
          userId,
          status: 'PENDING',
        },
      });
    } catch (error) {
      console.error('Error storing user report:', error);
    }
  }

  /**
   * Store chat message in PostgreSQL
   */
  async storeChatMessage(sessionId, messageType, content, userId = null, responseTime = null) {
    try {
      await prisma.chatMessage.create({
        data: {
          sessionId,
          messageType: messageType.toUpperCase(),
          content,
          responseTimeMs: responseTime,
        },
      });

      // Update session message count
      await prisma.chatSession.update({
        where: { sessionId },
        data: {
          totalMessages: {
            increment: 1,
          },
        },
      });
    } catch (error) {
      console.error('Error storing chat message:', error);
    }
  }

  /**
   * Log API errors
   */
  async logApiError(apiName, errorMessage) {
    try {
      await prisma.apiStatus.create({
        data: {
          apiName,
          status: 'ERROR',
          errorMessage,
          lastCheck: new Date(),
        },
      });
    } catch (error) {
      console.error('Error logging API status:', error);
    }
  }

  /**
   * Get fallback analysis when AI service is down
   */
  async getFallbackAnalysis(url) {
    // Check if URL exists in local database
    const urlHash = this.hashUrl(url);
    
    try {
      const existingScam = await prisma.scamUrl.findUnique({
        where: { urlHash },
      });

      if (existingScam) {
        return {
          threat_level: 'high',
          confidence: parseFloat(existingScam.confidence),
          message: 'URL found in local scam database',
          detection_methods: ['local_database'],
          is_suspicious: true,
        };
      }

      // Basic pattern analysis
      const domain = new URL(url).hostname;
      const suspiciousPatterns = ['login', 'secure', 'verify', 'account', 'bank'];
      const isSuspicious = suspiciousPatterns.some(pattern => 
        domain.toLowerCase().includes(pattern)
      );

      return {
        threat_level: isSuspicious ? 'medium' : 'low',
        confidence: 0.3,
        message: 'Basic pattern analysis (AI service unavailable)',
        detection_methods: ['pattern_analysis'],
        is_suspicious: isSuspicious,
      };
    } catch (error) {
      console.error('Fallback analysis error:', error);
      return {
        threat_level: 'unknown',
        confidence: 0.0,
        message: 'Unable to analyze URL',
        detection_methods: [],
        is_suspicious: false,
      };
    }
  }

  /**
   * Get fallback chat response
   */
  async getFallbackChatResponse(message) {
    const fallbackResponses = {
      'help': 'I\'m here to help you stay safe online. You can ask me about phishing detection, scam prevention, or report suspicious links.',
      'phishing': 'Phishing attacks try to steal your personal information. Never click suspicious links or enter details on unfamiliar sites.',
      'scam': 'If you think you\'ve encountered a scam, don\'t click any links and report it immediately.',
      'password': 'Use strong, unique passwords and enable two-factor authentication when possible.',
    };

    const lowerMessage = message.toLowerCase();
    for (const [key, response] of Object.entries(fallbackResponses)) {
      if (lowerMessage.includes(key)) {
        return { response };
      }
    }

    return {
      response: 'I\'m currently experiencing technical difficulties. Please try again later or contact support for urgent matters.',
    };
  }

  /**
   * Get cached tips from PostgreSQL
   */
  async getCachedTips(category = null) {
    try {
      const whereClause = category 
        ? { contentType: category, isActive: true }
        : { isActive: true };

      const tips = await prisma.knowledgeBase.findMany({
        where: whereClause,
        select: {
          title: true,
          content: true,
          contentType: true,
          tags: true,
        },
        take: 5,
      });

      return { tips };
    } catch (error) {
      console.error('Error getting cached tips:', error);
      return { tips: [] };
    }
  }

  /**
   * Get cached intelligence data
   */
  async getCachedIntelligence() {
    try {
      const stats = await prisma.detectionHistory.groupBy({
        by: ['threatLevel'],
        _count: {
          id: true,
        },
        where: {
          timestamp: {
            gte: new Date(Date.now() - 24 * 60 * 60 * 1000), // Last 24 hours
          },
        },
      });

      return {
        summary: {
          total_detections: stats.reduce((sum, stat) => sum + stat._count.id, 0),
          threat_breakdown: stats.reduce((acc, stat) => {
            acc[stat.threatLevel] = stat._count.id;
            return acc;
          }, {}),
        },
      };
    } catch (error) {
      console.error('Error getting cached intelligence:', error);
      return { summary: { total_detections: 0, threat_breakdown: {} } };
    }
  }

  /**
   * Hash URL for consistent storage
   */
  hashUrl(url) {
    const crypto = require('crypto');
    const normalized = url.toLowerCase().trim();
    return crypto.createHash('sha256').update(normalized).digest('hex');
  }

  /**
   * Health check for AI service
   */
  async healthCheck() {
    try {
      const response = await this.axiosInstance.get('/health');
      return {
        status: 'healthy',
        response: response.data,
      };
    } catch (error) {
      return {
        status: 'unhealthy',
        error: error.message,
      };
    }
  }
}

export default new AIService(); 
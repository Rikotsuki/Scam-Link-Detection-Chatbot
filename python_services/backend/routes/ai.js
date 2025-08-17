import { Router } from 'express';
import { body, validationResult } from 'express-validator';
import aiService from '../services/aiService.js';
import { authenticateToken } from '../middlewares/auth.js';
import { v4 as uuidv4 } from 'uuid';

const router = Router();

// Validation middleware
const validateUrl = [
  body('url')
    .trim()
    .isURL()
    .withMessage('Please provide a valid URL'),
  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ 
        success: false, 
        error: 'Validation failed', 
        details: errors.array() 
      });
    }
    next();
  },
];

const validateChatMessage = [
  body('message')
    .trim()
    .isLength({ min: 1, max: 1000 })
    .withMessage('Message must be between 1 and 1000 characters'),
  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ 
        success: false, 
        error: 'Validation failed', 
        details: errors.array() 
      });
    }
    next();
  },
];

const validateReport = [
  body('url')
    .trim()
    .isURL()
    .withMessage('Please provide a valid URL'),
  body('description')
    .trim()
    .isLength({ min: 10, max: 1000 })
    .withMessage('Description must be between 10 and 1000 characters'),
  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ 
        success: false, 
        error: 'Validation failed', 
        details: errors.array() 
      });
    }
    next();
  },
];

/**
 * @route POST /api/ai/analyze
 * @desc Analyze URL for phishing threats
 * @access Public (with optional user authentication)
 */
router.post('/analyze', validateUrl, async (req, res) => {
  try {
    const { url } = req.body;
    const userId = req.user?.id || null;

    const result = await aiService.analyzeUrl(url, userId);

    if (result.success) {
      res.json({
        success: true,
        data: result.data,
        responseTime: result.responseTime,
        message: 'URL analysis completed successfully',
      });
    } else {
      res.status(503).json({
        success: false,
        error: result.error,
        fallback: result.fallback,
        message: 'AI service unavailable, using fallback analysis',
      });
    }
  } catch (error) {
    console.error('Analyze URL error:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error',
      message: 'Failed to analyze URL',
    });
  }
});

/**
 * @route POST /api/ai/chat
 * @desc Chat with AI chatbot
 * @access Public (with optional user authentication)
 */
router.post('/chat', validateChatMessage, async (req, res) => {
  try {
    const { message, sessionId } = req.body;
    const userId = req.user?.id || null;

    // Generate session ID if not provided
    const chatSessionId = sessionId || uuidv4();

    const result = await aiService.chatWithBot(message, chatSessionId, userId);

    if (result.success) {
      res.json({
        success: true,
        data: result.data,
        sessionId: chatSessionId,
        responseTime: result.responseTime,
        message: 'Chat response generated successfully',
      });
    } else {
      res.status(503).json({
        success: false,
        error: result.error,
        fallback: result.fallback,
        sessionId: chatSessionId,
        message: 'AI service unavailable, using fallback response',
      });
    }
  } catch (error) {
    console.error('Chat error:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error',
      message: 'Failed to process chat message',
    });
  }
});

/**
 * @route POST /api/ai/report
 * @desc Report a scam URL
 * @access Public (with optional user authentication)
 */
router.post('/report', validateReport, async (req, res) => {
  try {
    const { url, description } = req.body;
    const userId = req.user?.id || null;

    const result = await aiService.reportScam(url, description, userId);

    if (result.success) {
      res.status(201).json({
        success: true,
        data: result.data,
        message: 'Scam report submitted successfully',
      });
    } else {
      res.status(503).json({
        success: false,
        error: result.error,
        message: 'Report service unavailable, but report saved locally',
      });
    }
  } catch (error) {
    console.error('Report error:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error',
      message: 'Failed to submit report',
    });
  }
});

/**
 * @route GET /api/ai/tips
 * @desc Get safety tips
 * @access Public
 */
router.get('/tips', async (req, res) => {
  try {
    const { category } = req.query;
    const result = await aiService.getSafetyTips(category);

    if (result.success) {
      res.json({
        success: true,
        data: result.data,
        message: 'Safety tips retrieved successfully',
      });
    } else {
      res.status(503).json({
        success: false,
        error: result.error,
        fallback: result.fallback,
        message: 'Tips service unavailable, using cached tips',
      });
    }
  } catch (error) {
    console.error('Tips error:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error',
      message: 'Failed to retrieve safety tips',
    });
  }
});

/**
 * @route GET /api/ai/intelligence
 * @desc Get threat intelligence summary
 * @access Public
 */
router.get('/intelligence', async (req, res) => {
  try {
    const result = await aiService.getThreatIntelligence();

    if (result.success) {
      res.json({
        success: true,
        data: result.data,
        message: 'Threat intelligence retrieved successfully',
      });
    } else {
      res.status(503).json({
        success: false,
        error: result.error,
        fallback: result.fallback,
        message: 'Intelligence service unavailable, using cached data',
      });
    }
  } catch (error) {
    console.error('Intelligence error:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error',
      message: 'Failed to retrieve threat intelligence',
    });
  }
});

/**
 * @route GET /api/ai/health
 * @desc Check AI service health
 * @access Public
 */
router.get('/health', async (req, res) => {
  try {
    const health = await aiService.healthCheck();
    
    if (health.status === 'healthy') {
      res.json({
        success: true,
        status: 'healthy',
        data: health.response,
        message: 'AI service is operational',
      });
    } else {
      res.status(503).json({
        success: false,
        status: 'unhealthy',
        error: health.error,
        message: 'AI service is experiencing issues',
      });
    }
  } catch (error) {
    console.error('Health check error:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error',
      message: 'Failed to check AI service health',
    });
  }
});

/**
 * @route GET /api/ai/stats
 * @desc Get AI service statistics (requires authentication)
 * @access Private
 */
router.get('/stats', authenticateToken, async (req, res) => {
  try {
    // This would typically require admin privileges
    if (req.user.role !== 'ADMIN') {
      return res.status(403).json({
        success: false,
        error: 'Access denied',
        message: 'Admin privileges required',
      });
    }

    // Get statistics from PostgreSQL
    const { PrismaClient } = await import('@prisma/client');
    const prisma = new PrismaClient();

    const [
      totalDetections,
      totalReports,
      totalChatMessages,
      recentDetections,
    ] = await Promise.all([
      prisma.detectionHistory.count(),
      prisma.userReport.count(),
      prisma.chatMessage.count(),
      prisma.detectionHistory.count({
        where: {
          timestamp: {
            gte: new Date(Date.now() - 24 * 60 * 60 * 1000), // Last 24 hours
          },
        },
      }),
    ]);

    res.json({
      success: true,
      data: {
        totalDetections,
        totalReports,
        totalChatMessages,
        recentDetections24h: recentDetections,
        aiServiceStatus: await aiService.healthCheck(),
      },
      message: 'Statistics retrieved successfully',
    });
  } catch (error) {
    console.error('Stats error:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error',
      message: 'Failed to retrieve statistics',
    });
  }
});

export default router; 
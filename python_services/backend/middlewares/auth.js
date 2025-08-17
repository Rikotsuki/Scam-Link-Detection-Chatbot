import jwt from 'jsonwebtoken';
import user from '../models/user.js';

/**
 * Middleware to authenticate JWT token
 */
export const authenticateToken = async (req, res, next) => {
  try {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN

    if (!token) {
      return res.status(401).json({
        success: false,
        error: 'Access token required',
        message: 'Please provide a valid authentication token',
      });
    }

    // Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    
    // Get user from database
    const userData = await user.findById(decoded.id).select('-password');
    
    if (!userData) {
      return res.status(401).json({
        success: false,
        error: 'Invalid token',
        message: 'User not found',
      });
    }

    // Add user to request object
    req.user = userData;
    next();
  } catch (error) {
    console.error('Authentication error:', error);
    
    if (error.name === 'JsonWebTokenError') {
      return res.status(401).json({
        success: false,
        error: 'Invalid token',
        message: 'Token is not valid',
      });
    }
    
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({
        success: false,
        error: 'Token expired',
        message: 'Authentication token has expired',
      });
    }

    return res.status(500).json({
      success: false,
      error: 'Authentication failed',
      message: 'Internal server error during authentication',
    });
  }
};

/**
 * Optional authentication middleware (doesn't fail if no token)
 */
export const optionalAuth = async (req, res, next) => {
  try {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    if (!token) {
      req.user = null;
      return next();
    }

    // Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    
    // Get user from database
    const userData = await user.findById(decoded.id).select('-password');
    
    if (userData) {
      req.user = userData;
    } else {
      req.user = null;
    }
    
    next();
  } catch (error) {
    // If token is invalid, just continue without user
    req.user = null;
    next();
  }
};

/**
 * Role-based authorization middleware
 */
export const authorizeRole = (roles) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({
        success: false,
        error: 'Authentication required',
        message: 'Please log in to access this resource',
      });
    }

    const userRole = req.user.role || 'USER';
    
    if (!roles.includes(userRole)) {
      return res.status(403).json({
        success: false,
        error: 'Access denied',
        message: 'You do not have permission to access this resource',
      });
    }

    next();
  };
};

/**
 * Admin-only middleware
 */
export const requireAdmin = authorizeRole(['ADMIN']);

/**
 * Moderator or Admin middleware
 */
export const requireModerator = authorizeRole(['MODERATOR', 'ADMIN']);

/**
 * Rate limiting middleware for AI endpoints
 */
export const rateLimit = (windowMs = 15 * 60 * 1000, max = 100) => {
  const requests = new Map();

  return (req, res, next) => {
    const ip = req.ip || req.connection.remoteAddress;
    const now = Date.now();
    const windowStart = now - windowMs;

    // Clean old entries
    if (requests.has(ip)) {
      const userRequests = requests.get(ip).filter(time => time > windowStart);
      requests.set(ip, userRequests);
    } else {
      requests.set(ip, []);
    }

    const userRequests = requests.get(ip);

    if (userRequests.length >= max) {
      return res.status(429).json({
        success: false,
        error: 'Rate limit exceeded',
        message: 'Too many requests, please try again later',
        retryAfter: Math.ceil(windowMs / 1000),
      });
    }

    userRequests.push(now);
    next();
  };
};

/**
 * API key validation middleware for AI service communication
 */
export const validateApiKey = (req, res, next) => {
  const apiKey = req.headers['x-api-key'] || req.headers['authorization']?.split(' ')[1];
  
  if (!apiKey || apiKey !== process.env.AI_SERVICE_API_KEY) {
    return res.status(401).json({
      success: false,
      error: 'Invalid API key',
      message: 'API key is required and must be valid',
    });
  }

  next();
}; 
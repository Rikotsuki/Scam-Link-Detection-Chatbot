#!/usr/bin/env node
/**
 * Enhanced Anime AI Backend Server
 * Connects frontend to Python AI services
 */

require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const path = require('path');

// Import routes
const animeRoutes = require('./routes/anime');

const app = express();
const PORT = process.env.PORT || 3001;

// Security middleware
app.use(helmet());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.'
});
app.use('/api/', limiter);

// CORS configuration
app.use(cors({
  origin: process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000',
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Body parsing middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'anime-ai-backend',
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  });
});

// API routes
app.use('/api/anime', animeRoutes);

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    message: '🎌 Enhanced Anime AI Backend Server',
    version: '1.0.0',
    endpoints: {
      health: '/health',
      anime: '/api/anime',
      docs: 'https://github.com/your-repo/docs'
    },
    timestamp: new Date().toISOString()
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Backend Error:', err);
  res.status(500).json({
    error: 'Internal Server Error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong'
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Not Found',
    message: `Route ${req.originalUrl} not found`
  });
});

// Start server
app.listen(PORT, () => {
  console.log('🎌 Enhanced Anime AI Backend Server');
  console.log('=' .repeat(50));
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`🔗 Health check: http://localhost:${PORT}/health`);
  console.log(`🎯 API base: http://localhost:${PORT}/api`);
  console.log(`📚 Anime routes: http://localhost:${PORT}/api/anime`);
  console.log('=' .repeat(50));
  console.log('✅ Backend ready to connect with frontend and Python AI services!');
});

module.exports = app; 
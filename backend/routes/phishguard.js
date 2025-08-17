import { Router } from "express";
import axios from "axios";
import { verifyToken, optionalAuth } from "../middlewares/auth.js";

const phishguardRoutes = Router();

// Python service base URL
const PYTHON_SERVICE_URL = process.env.PYTHON_SERVICE_URL || "http://localhost:8000";

// Analyze URL endpoint
phishguardRoutes.post('/analyze', verifyToken, async (req, res) => {
  try {
    const { url, user_id } = req.body;
    
    if (!url) {
      return res.status(400).json({ error: "URL is required" });
    }

    // Forward request to Python service
    const response = await axios.post(`${PYTHON_SERVICE_URL}/analyze`, {
      url,
      user_id: user_id || req.user?.id // Use authenticated user ID if available
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': req.headers.authorization
      },
      timeout: 30000 // 30 second timeout
    });

    res.json(response.data);
  } catch (error) {
    console.error('Error analyzing URL:', error.message);
    
    if (error.response) {
      // Python service returned an error
      res.status(error.response.status).json(error.response.data);
    } else if (error.code === 'ECONNREFUSED') {
      res.status(503).json({ error: "PhishGuard service is unavailable" });
    } else {
      res.status(500).json({ error: "Failed to analyze URL" });
    }
  }
});

// Report scam endpoint
phishguardRoutes.post('/report', verifyToken, async (req, res) => {
  try {
    const { url, description, user_id } = req.body;
    
    if (!url || !description) {
      return res.status(400).json({ error: "URL and description are required" });
    }

    // Forward request to Python service
    const response = await axios.post(`${PYTHON_SERVICE_URL}/report`, {
      url,
      description,
      user_id: user_id || req.user?.id
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': req.headers.authorization
      },
      timeout: 30000
    });

    res.json(response.data);
  } catch (error) {
    console.error('Error reporting scam:', error.message);
    
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else if (error.code === 'ECONNREFUSED') {
      res.status(503).json({ error: "PhishGuard service is unavailable" });
    } else {
      res.status(500).json({ error: "Failed to report scam" });
    }
  }
});

// Get safety tips endpoint
phishguardRoutes.get('/tips', optionalAuth, async (req, res) => {
  try {
    // Forward request to Python service
    const response = await axios.get(`${PYTHON_SERVICE_URL}/tips`, {
      timeout: 10000
    });

    res.json(response.data);
  } catch (error) {
    console.error('Error getting safety tips:', error.message);
    
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else if (error.code === 'ECONNREFUSED') {
      res.status(503).json({ error: "PhishGuard service is unavailable" });
    } else {
      res.status(500).json({ error: "Failed to get safety tips" });
    }
  }
});

// Chat with bot endpoint
phishguardRoutes.post('/chat', verifyToken, async (req, res) => {
  try {
    const { message, user_id, session_id } = req.body;
    
    if (!message) {
      return res.status(400).json({ error: "Message is required" });
    }

    // Forward request to Python service
    const response = await axios.post(`${PYTHON_SERVICE_URL}/chat`, {
      message,
      user_id: user_id || req.user?.id,
      session_id
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': req.headers.authorization
      },
      timeout: 30000
    });

    res.json(response.data);
  } catch (error) {
    console.error('Error in chat:', error.message);
    
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else if (error.code === 'ECONNREFUSED') {
      res.status(503).json({ error: "PhishGuard service is unavailable" });
    } else {
      res.status(500).json({ error: "Failed to process chat message" });
    }
  }
});

// Health check endpoint
phishguardRoutes.get('/health', async (req, res) => {
  try {
    const response = await axios.get(`${PYTHON_SERVICE_URL}/`, {
      timeout: 5000
    });
    
    res.json({
      status: 'healthy',
      python_service: 'connected',
      message: response.data.message
    });
  } catch (error) {
    res.status(503).json({
      status: 'unhealthy',
      python_service: 'disconnected',
      error: error.message
    });
  }
});

export default phishguardRoutes; 
import { Router } from "express";
import axios from "axios";
import multer from "multer";
import path from "path";
import fs from "fs";
import { verifyToken, optionalAuth } from "../middlewares/auth.js";
import { config } from "../config.js";

const animeRoutes = Router();

// Python service base URL
const PYTHON_SERVICE_URL = config.PYTHON_SERVICE_URL;

// Configure multer for image uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = path.join(process.cwd(), 'uploads', 'images');
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, `anime-analysis-${uniqueSuffix}${path.extname(file.originalname)}`);
  }
});

const upload = multer({ 
  storage: storage,
  limits: {
    fileSize: 10 * 1024 * 1024, // 10MB limit
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = /jpeg|jpg|png|gif|webp|svg/;
    const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
    const mimetype = allowedTypes.test(file.mimetype);
    
    if (mimetype && extname) {
      return cb(null, true);
    } else {
      cb(new Error('Only image files are allowed (JPEG, PNG, GIF, WEBP, SVG)'));
    }
  }
});

// AI-chan greeting endpoint
animeRoutes.get('/ai-chan/greeting', optionalAuth, async (req, res) => {
  try {
    const response = await axios.get(`${PYTHON_SERVICE_URL}/anime/ai-chan/greeting`, {
      timeout: 10000
    });

    res.json({
      ...response.data,
      character: "AI-chan",
      personality: "cheerful anime girl phishing detector"
    });
  } catch (error) {
    console.error('Error getting AI-chan greeting:', error.message);
    
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else if (error.code === 'ECONNREFUSED') {
      res.status(503).json({ error: "Anime AI service is unavailable" });
    } else {
      res.status(500).json({ error: "Failed to get AI-chan greeting" });
    }
  }
});

// Haru greeting endpoint  
animeRoutes.get('/haru/greeting', optionalAuth, async (req, res) => {
  try {
    const response = await axios.get(`${PYTHON_SERVICE_URL}/anime/haru/greeting`, {
      timeout: 10000
    });

    res.json({
      ...response.data,
      character: "Haru",
      personality: "lazy but caring anime boy recovery assistant"
    });
  } catch (error) {
    console.error('Error getting Haru greeting:', error.message);
    
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else if (error.code === 'ECONNREFUSED') {
      res.status(503).json({ error: "Anime AI service is unavailable" });
    } else {
      res.status(500).json({ error: "Failed to get Haru greeting" });
    }
  }
});

// AI-chan phishing detection with voice warning
animeRoutes.post('/ai-chan/analyze', verifyToken, upload.single('image'), async (req, res) => {
  try {
    const { url, user_id } = req.body;
    const image = req.file;
    
    if (!url && !image) {
      return res.status(400).json({ error: "URL or image is required" });
    }

    const formData = new FormData();
    if (url) formData.append('url', url);
    if (user_id || req.user?.id) formData.append('user_id', user_id || req.user.id);
    
    // If image is provided, send it as binary data
    if (image) {
      const imageBuffer = fs.readFileSync(image.path);
      formData.append('image', new Blob([imageBuffer]), image.filename);
    }

    const response = await axios.post(`${PYTHON_SERVICE_URL}/anime/ai-chan/analyze`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': req.headers.authorization
      },
      timeout: 60000 // Longer timeout for vision processing
    });

    // Clean up uploaded file
    if (image && fs.existsSync(image.path)) {
      fs.unlinkSync(image.path);
    }

    res.json({
      ...response.data,
      character: "AI-chan",
      analysis_type: "vision_enhanced_phishing_detection"
    });
  } catch (error) {
    console.error('Error in AI-chan analysis:', error.message);
    
    // Clean up uploaded file on error
    if (req.file && fs.existsSync(req.file.path)) {
      fs.unlinkSync(req.file.path);
    }
    
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else if (error.code === 'ECONNREFUSED') {
      res.status(503).json({ error: "Anime AI service is unavailable" });
    } else {
      res.status(500).json({ error: "Failed to analyze with AI-chan" });
    }
  }
});

// Haru recovery assistance with lazy responses
animeRoutes.post('/haru/help', verifyToken, upload.single('screenshot'), async (req, res) => {
  try {
    const { situation, user_id } = req.body;
    const screenshot = req.file;
    
    if (!situation) {
      return res.status(400).json({ error: "Situation description is required" });
    }

    const formData = new FormData();
    formData.append('situation', situation);
    if (user_id || req.user?.id) formData.append('user_id', user_id || req.user.id);
    
    // If screenshot is provided, send it as binary data
    if (screenshot) {
      const imageBuffer = fs.readFileSync(screenshot.path);
      formData.append('screenshot', new Blob([imageBuffer]), screenshot.filename);
    }

    const response = await axios.post(`${PYTHON_SERVICE_URL}/anime/haru/help`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': req.headers.authorization
      },
      timeout: 60000
    });

    // Clean up uploaded file
    if (screenshot && fs.existsSync(screenshot.path)) {
      fs.unlinkSync(screenshot.path);
    }

    res.json({
      ...response.data,
      character: "Haru",
      help_type: "recovery_assistance_with_lazy_attitude"
    });
  } catch (error) {
    console.error('Error in Haru help:', error.message);
    
    // Clean up uploaded file on error
    if (req.file && fs.existsSync(req.file.path)) {
      fs.unlinkSync(req.file.path);
    }
    
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else if (error.code === 'ECONNREFUSED') {
      res.status(503).json({ error: "Anime AI service is unavailable" });
    } else {
      res.status(500).json({ error: "Failed to get help from Haru" });
    }
  }
});

// Combined analysis endpoint (AI-chan detects, Haru helps if needed)
animeRoutes.post('/analyze-and-help', verifyToken, upload.single('image'), async (req, res) => {
  try {
    const { url, situation, user_id } = req.body;
    const image = req.file;
    
    if (!url && !image) {
      return res.status(400).json({ error: "URL or image is required" });
    }

    const formData = new FormData();
    if (url) formData.append('url', url);
    if (situation) formData.append('situation', situation);
    if (user_id || req.user?.id) formData.append('user_id', user_id || req.user.id);
    
    if (image) {
      const imageBuffer = fs.readFileSync(image.path);
      formData.append('image', new Blob([imageBuffer]), image.filename);
    }

    const response = await axios.post(`${PYTHON_SERVICE_URL}/anime/combined-analysis`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': req.headers.authorization
      },
      timeout: 90000 // Extra long timeout for combined analysis
    });

    // Clean up uploaded file
    if (image && fs.existsSync(image.path)) {
      fs.unlinkSync(image.path);
    }

    res.json({
      ...response.data,
      analysis_type: "combined_ai_chan_and_haru_analysis"
    });
  } catch (error) {
    console.error('Error in combined analysis:', error.message);
    
    // Clean up uploaded file on error
    if (req.file && fs.existsSync(req.file.path)) {
      fs.unlinkSync(req.file.path);
    }
    
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else if (error.code === 'ECONNREFUSED') {
      res.status(503).json({ error: "Anime AI service is unavailable" });
    } else {
      res.status(500).json({ error: "Failed to perform combined analysis" });
    }
  }
});

// Download voice file endpoint
animeRoutes.get('/voice/:filename', async (req, res) => {
  try {
    const { filename } = req.params;
    
    // Security check: only allow .wav files and prevent directory traversal
    if (!filename.endsWith('.wav') || filename.includes('..') || filename.includes('/')) {
      return res.status(400).json({ error: "Invalid filename" });
    }

    const response = await axios.get(`${PYTHON_SERVICE_URL}/anime/voice/${filename}`, {
      responseType: 'stream',
      timeout: 10000
    });

    res.setHeader('Content-Type', 'audio/wav');
    res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
    
    response.data.pipe(res);
  } catch (error) {
    console.error('Error downloading voice file:', error.message);
    
    if (error.response?.status === 404) {
      res.status(404).json({ error: "Voice file not found" });
    } else if (error.code === 'ECONNREFUSED') {
      res.status(503).json({ error: "Anime AI service is unavailable" });
    } else {
      res.status(500).json({ error: "Failed to download voice file" });
    }
  }
});

// Anime system health check
animeRoutes.get('/health', async (req, res) => {
  try {
    const response = await axios.get(`${PYTHON_SERVICE_URL}/anime/health`, {
      timeout: 5000
    });
    
    res.json({
      status: 'healthy',
      anime_ai_service: 'connected',
      characters: {
        "ai_chan": "ready for phishing detection",
        "haru": "ready for recovery assistance"
      },
      features: {
        "vision_analysis": "llama3.2-vision:11b",
        "japanese_tts": "parler-tts-mini",
        "rag_system": "chromadb"
      },
      message: response.data.message
    });
  } catch (error) {
    console.error('Error checking anime system health:', error.message);
    
    res.status(503).json({
      status: 'unhealthy',
      anime_ai_service: 'disconnected',
      error: error.message,
      note: "Make sure the Python anime AI service is running"
    });
  }
});

// Generate custom voice endpoint
animeRoutes.post('/voice/generate', verifyToken, async (req, res) => {
  try {
    const { text, character, user_id } = req.body;
    
    if (!text || !character) {
      return res.status(400).json({ error: "Text and character are required" });
    }

    if (!['ai-chan', 'haru'].includes(character.toLowerCase())) {
      return res.status(400).json({ error: "Character must be 'ai-chan' or 'haru'" });
    }

    const response = await axios.post(`${PYTHON_SERVICE_URL}/anime/voice/generate`, {
      text,
      character: character.toLowerCase(),
      user_id: user_id || req.user?.id
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': req.headers.authorization
      },
      timeout: 30000
    });

    res.json({
      ...response.data,
      character: character,
      generated_text: text
    });
  } catch (error) {
    console.error('Error generating voice:', error.message);
    
    if (error.response) {
      res.status(error.response.status).json(error.response.data);
    } else if (error.code === 'ECONNREFUSED') {
      res.status(503).json({ error: "Anime AI service is unavailable" });
    } else {
      res.status(500).json({ error: "Failed to generate voice" });
    }
  }
});

export default animeRoutes; 
# 🎌 Anime PhishGuard AI Integration Guide

## 🚀 Complete System Integration

This guide shows how to integrate the anime AI system with your existing **Node.js backend** and **Next.js frontend**.

## 📁 System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Next.js       │    │   Node.js       │    │   Python        │
│   Frontend      │◄──►│   Backend       │◄──►│   Anime AI API  │
│   (Port 3001)   │    │   (Port 3000)   │    │   (Port 8000)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   MongoDB       │    │   Ollama        │
                       │   Database      │    │   llama3.2-     │
                       │                 │    │   vision:11b    │
                       └─────────────────┘    └─────────────────┘
```

## 🛠️ Prerequisites

### 1. Ollama Setup
```bash
# Install Ollama from https://ollama.ai
# Pull the vision model (this is large - 11B parameters!)
ollama pull llama3.2-vision:11b

# Verify installation
ollama list
```

### 2. Node.js Backend Dependencies
```bash
cd backend
npm install multer cors  # Additional dependencies for anime routes
```

### 3. Python Dependencies
```bash
cd ai_training
pip install -r requirements_anime.txt

# Install Japanese TTS dependencies
pip install git+https://github.com/huggingface/parler-tts.git
pip install git+https://github.com/getuka/RubyInserter.git
```

## 🚀 Quick Start (Automated)

### Option 1: One-Click Setup
```bash
cd ai_training
python start_integrated_system.py
```

This will:
- ✅ Check Ollama and model availability
- ✅ Install all dependencies automatically
- ✅ Start Python API server (port 8000)
- ✅ Start Node.js backend (port 3000)
- ✅ Test integration between components
- ✅ Display available API endpoints

### Option 2: Manual Setup

#### Step 1: Start Python Anime AI API
```bash
cd ai_training
python anime_api_server.py
```

#### Step 2: Start Node.js Backend
```bash
cd backend
npm start
```

#### Step 3: Verify Integration
```bash
# Test anime API health
curl http://localhost:8000/anime/health

# Test backend integration
curl http://localhost:3000/api/anime/health

# Test AI-chan greeting
curl http://localhost:3000/api/anime/ai-chan/greeting
```

## 🌸 AI-chan API Endpoints

### Character Greeting
```http
GET /api/anime/ai-chan/greeting
```

**Response:**
```json
{
  "character": "AI-chan",
  "greeting": "こんにちは！AI-chanです♪",
  "voice_file": "ai_greeting_1234567890.wav",
  "personality": "cheerful anime girl phishing detector",
  "message": "AI-chan is ready to help detect phishing! ♪"
}
```

### Phishing Analysis with Voice Warning
```http
POST /api/anime/ai-chan/analyze
Content-Type: multipart/form-data
Authorization: Bearer <token>

{
  "url": "https://suspicious-site.com",
  "image": <file>,
  "user_id": "user123"
}
```

**Response:**
```json
{
  "character": "AI-chan",
  "analysis_type": "vision_enhanced_phishing_detection",
  "url_analysis": {
    "analysis": "This URL appears suspicious...",
    "character": "AI-chan"
  },
  "image_analysis": {
    "analysis": "The image shows a fake login form...",
    "voice_file": "danger_warning_1234567890.wav"
  },
  "danger_detected": true,
  "voice_warning": "danger_warning_1234567890.wav",
  "message": "AI-chan has completed the analysis! ♪"
}
```

## 😴 Haru API Endpoints

### Character Greeting
```http
GET /api/anime/haru/greeting
```

**Response:**
```json
{
  "character": "Haru",
  "greeting": "はぁ...Haruだよ。何か用？",
  "voice_file": "haru_greeting_1234567890.wav",
  "personality": "lazy but caring anime boy recovery assistant",
  "message": "Haru is here to help... *sigh*"
}
```

### Recovery Assistance
```http
POST /api/anime/haru/help
Content-Type: multipart/form-data
Authorization: Bearer <token>

{
  "situation": "I clicked on a suspicious link",
  "screenshot": <file>,
  "user_id": "user123"
}
```

**Response:**
```json
{
  "character": "Haru",
  "situation": "I clicked on a suspicious link",
  "help_response": {
    "response": "はぁ...まあ、まず落ち着いて...",
    "character": "Haru"
  },
  "lazy_response": "lazy_response_1234567890.wav",
  "message": "Haru is getting a bit tired of all the questions...",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## 🎭 Combined Analysis

### Analyze and Get Help
```http
POST /api/anime/analyze-and-help
Content-Type: multipart/form-data
Authorization: Bearer <token>

{
  "url": "https://suspicious-site.com",
  "situation": "I'm worried about this link",
  "image": <file>,
  "user_id": "user123"
}
```

**Response:**
```json
{
  "analysis_type": "combined_ai_chan_and_haru_analysis",
  "ai_chan_analysis": {
    "danger_detected": true,
    "voice_warning": "danger_warning_1234567890.wav"
  },
  "haru_assistance": {
    "help_response": "Recovery steps...",
    "lazy_response": "lazy_response_1234567890.wav"
  },
  "danger_level": "high",
  "message": "Combined analysis completed by both AI-chan and Haru!"
}
```

## 🔊 Voice File Management

### Download Voice Files
```http
GET /api/anime/voice/{filename}
```

**Example:**
```bash
# Download AI-chan's danger warning
curl -O http://localhost:3000/api/anime/voice/danger_warning_1234567890.wav

# Download Haru's lazy response
curl -O http://localhost:3000/api/anime/voice/lazy_response_1234567890.wav
```

### Generate Custom Voice
```http
POST /api/anime/voice/generate
Content-Type: application/json
Authorization: Bearer <token>

{
  "text": "こんにちは、元気ですか？",
  "character": "ai-chan",
  "user_id": "user123"
}
```

## 🎨 Frontend Integration Examples

### React/Next.js Components

#### AI-chan Greeting Component
```tsx
import { useState, useEffect } from 'react';

const AIChanGreeting: React.FC = () => {
  const [greeting, setGreeting] = useState(null);
  const [audio, setAudio] = useState<HTMLAudioElement | null>(null);

  useEffect(() => {
    fetch('/api/anime/ai-chan/greeting')
      .then(res => res.json())
      .then(data => {
        setGreeting(data);
        if (data.voice_file) {
          setAudio(new Audio(`/api/anime/voice/${data.voice_file}`));
        }
      });
  }, []);

  const playVoice = () => {
    if (audio) {
      audio.play();
    }
  };

  return (
    <div className="ai-chan-greeting">
      <div className="character-avatar">🌸</div>
      <h3>AI-chan</h3>
      {greeting && (
        <>
          <p>{greeting.greeting}</p>
          <p className="personality">{greeting.personality}</p>
          {greeting.voice_file && (
            <button onClick={playVoice} className="voice-button">
              🔊 Hear AI-chan's Voice
            </button>
          )}
        </>
      )}
    </div>
  );
};
```

#### Phishing Analysis Component
```tsx
import { useState } from 'react';

const PhishingAnalyzer: React.FC = () => {
  const [url, setUrl] = useState('');
  const [image, setImage] = useState<File | null>(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeContent = async () => {
    setLoading(true);
    
    const formData = new FormData();
    if (url) formData.append('url', url);
    if (image) formData.append('image', image);
    
    try {
      const response = await fetch('/api/anime/ai-chan/analyze', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${userToken}`
        },
        body: formData
      });
      
      const data = await response.json();
      setResult(data);
      
      // Play danger warning if detected
      if (data.danger_detected && data.voice_warning) {
        const audio = new Audio(`/api/anime/voice/${data.voice_warning}`);
        audio.play();
      }
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="phishing-analyzer">
      <h3>🌸 AI-chan's Phishing Detector</h3>
      
      <input
        type="url"
        placeholder="Enter suspicious URL..."
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setImage(e.target.files?.[0] || null)}
      />
      
      <button onClick={analyzeContent} disabled={loading || (!url && !image)}>
        {loading ? 'Analyzing...' : 'Analyze with AI-chan ♪'}
      </button>
      
      {result && (
        <div className="analysis-result">
          {result.danger_detected && (
            <div className="danger-alert">
              🚨 AI-chan detected danger!
              {result.voice_warning && (
                <audio controls>
                  <source src={`/api/anime/voice/${result.voice_warning}`} type="audio/wav" />
                </audio>
              )}
            </div>
          )}
          
          {result.url_analysis && (
            <div className="url-analysis">
              <h4>URL Analysis:</h4>
              <p>{result.url_analysis.analysis}</p>
            </div>
          )}
          
          {result.image_analysis && (
            <div className="image-analysis">
              <h4>Image Analysis:</h4>
              <p>{result.image_analysis.analysis}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
```

#### Haru Help Component
```tsx
import { useState } from 'react';

const HaruHelp: React.FC = () => {
  const [situation, setSituation] = useState('');
  const [screenshot, setScreenshot] = useState<File | null>(null);
  const [help, setHelp] = useState(null);
  const [questionCount, setQuestionCount] = useState(0);

  const getHelp = async () => {
    const formData = new FormData();
    formData.append('situation', situation);
    if (screenshot) formData.append('screenshot', screenshot);
    
    try {
      const response = await fetch('/api/anime/haru/help', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${userToken}`
        },
        body: formData
      });
      
      const data = await response.json();
      setHelp(data);
      setQuestionCount(prev => prev + 1);
      
      // Play lazy response if Haru is getting tired
      if (data.lazy_response) {
        const audio = new Audio(`/api/anime/voice/${data.lazy_response}`);
        audio.play();
      }
    } catch (error) {
      console.error('Help request failed:', error);
    }
  };

  return (
    <div className="haru-help">
      <h3>😴 Haru's Recovery Assistant</h3>
      
      <textarea
        placeholder="Describe your situation..."
        value={situation}
        onChange={(e) => setSituation(e.target.value)}
      />
      
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setScreenshot(e.target.files?.[0] || null)}
      />
      
      <button onClick={getHelp} disabled={!situation}>
        Get Help from Haru
      </button>
      
      {questionCount >= 3 && (
        <p className="lazy-warning">
          💤 Haru is getting a bit tired of questions...
        </p>
      )}
      
      {help && (
        <div className="help-response">
          <div className="character-response">
            <strong>😴 Haru:</strong>
            <p>{help.help_response?.response}</p>
          </div>
          
          {help.lazy_response && (
            <div className="lazy-response">
              🔊 Haru's tired response:
              <audio controls>
                <source src={`/api/anime/voice/${help.lazy_response}`} type="audio/wav" />
              </audio>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
```

## 🎨 Frontend Styling

### CSS for Anime Components
```css
.ai-chan-greeting {
  background: linear-gradient(135deg, #FFB6C1, #FF69B4);
  border-radius: 15px;
  padding: 20px;
  text-align: center;
  color: white;
  box-shadow: 0 4px 15px rgba(255, 105, 180, 0.3);
}

.character-avatar {
  font-size: 2rem;
  margin-bottom: 10px;
}

.haru-help {
  background: linear-gradient(135deg, #B0C4DE, #778899);
  border-radius: 15px;
  padding: 20px;
  color: white;
  box-shadow: 0 4px 15px rgba(119, 136, 153, 0.3);
}

.danger-alert {
  background: #FF4444;
  color: white;
  padding: 15px;
  border-radius: 10px;
  margin: 10px 0;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

.voice-button {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 25px;
  cursor: pointer;
  transition: background 0.3s;
}

.voice-button:hover {
  background: #45a049;
}

.lazy-warning {
  background: #FFA500;
  color: white;
  padding: 10px;
  border-radius: 5px;
  margin: 10px 0;
}
```

## 🔧 Environment Configuration

### Backend Environment (.env)
```env
# Database
DB_URL=mongodb://localhost:27017/phishguard
JWT_SECRET=your_jwt_secret_here

# Python Service
PYTHON_SERVICE_URL=http://localhost:8000
PYTHON_SERVICE_PORT=8000

# Server
PORT=3000

# Frontend
FRONTEND_URL=http://localhost:3001
```

### Python Environment
```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2-vision:11b

# TTS Configuration
TTS_MODEL=2121-8/japanese-parler-tts-mini

# RAG Configuration
RAG_DATABASE_PATH=./rag_database
```

## 🚀 Deployment

### Docker Compose Setup
```yaml
version: '3.8'
services:
  anime-ai:
    build: ./ai_training
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      - ollama
    volumes:
      - ./voice_files:/app/voice_files

  backend:
    build: ./backend
    ports:
      - "3000:3000"
    environment:
      - PYTHON_SERVICE_URL=http://anime-ai:8000
      - DB_URL=mongodb://mongo:27017/phishguard
    depends_on:
      - anime-ai
      - mongo

  frontend:
    build: ./frontend
    ports:
      - "3001:3001"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:3000
    depends_on:
      - backend

  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  ollama_data:
  mongo_data:
```

## 🧪 Testing the Integration

### Health Check Script
```bash
#!/bin/bash
echo "🔍 Testing Anime PhishGuard AI Integration"

# Test Python API
echo "Testing Python API..."
curl -s http://localhost:8000/anime/health | jq '.'

# Test Backend Integration
echo "Testing Backend Integration..."
curl -s http://localhost:3000/api/anime/health | jq '.'

# Test AI-chan
echo "Testing AI-chan..."
curl -s http://localhost:3000/api/anime/ai-chan/greeting | jq '.greeting'

# Test Haru
echo "Testing Haru..."
curl -s http://localhost:3000/api/anime/haru/greeting | jq '.greeting'

echo "✅ Integration tests completed!"
```

## 🐛 Troubleshooting

### Common Issues

1. **Ollama Model Not Found**
   ```bash
   ollama pull llama3.2-vision:11b
   ollama list  # Verify model is installed
   ```

2. **Japanese TTS Installation Failed**
   ```bash
   pip uninstall parler-tts
   pip install git+https://github.com/huggingface/parler-tts.git
   ```

3. **Backend Can't Connect to Python API**
   - Check Python API is running on port 8000
   - Verify PYTHON_SERVICE_URL in backend config
   - Check firewall/network settings

4. **Voice Files Not Playing**
   - Ensure voice files are generated in correct directory
   - Check file permissions
   - Verify audio codec support in browser

5. **Memory Issues with Vision Model**
   - llama3.2-vision:11b requires 16GB+ RAM
   - Consider using a smaller model if needed
   - Close other applications to free memory

## 📚 API Reference

### Complete API Documentation
Visit `http://localhost:8000/docs` when the Python API is running for interactive API documentation with Swagger UI.

### Character Information Endpoint
```http
GET /anime/characters
```

Returns detailed information about AI-chan and Haru, including personalities, voice characteristics, and trigger conditions.

---

**🎌 Your integrated anime AI system is now ready!**

Start with `python start_integrated_system.py` to launch everything automatically, or follow the manual setup for more control.

*AI-chan*: "みんなで一緒にフィッシングと戦いましょう！♪" (Let's fight phishing together, everyone! ♪)

*Haru*: "はぁ...でもちゃんと手伝うからね..." (Sigh... but I'll help properly...) 
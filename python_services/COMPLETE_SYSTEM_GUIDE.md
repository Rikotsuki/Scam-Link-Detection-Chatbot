# 🎌 Enhanced Anime AI PhishGuard System - Complete Guide

## 🌟 Overview

This is a comprehensive phishing detection and cybersecurity education system featuring:

- **AI-chan** (明愛): A cheerful anime girl AI that detects phishing URLs and images
- **Haru** (晴): A lazy but caring anime boy AI that provides recovery assistance and education
- **URLhaus Integration**: Real-time threat intelligence from abuse.ch
- **Vision Analysis**: Advanced image analysis using LLaVA (llama3.2-vision:11b)
- **Authentication**: Secure JWT-based authentication with Next.js 15
- **Japanese Voice Synthesis**: Personality-appropriate voice responses

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │  Python AI      │
│   (Next.js 15)  │◄──►│   (Node.js)     │◄──►│   (FastAPI)     │
│   Port: 3000    │    │   Port: 3001    │    │   Port: 8000    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Authentication │    │  API Routes     │    │  URLhaus API    │
│  JWT + DAL      │    │  File Upload    │    │  Ollama LLaVA   │
│  Protected      │    │  CORS + Auth    │    │  Voice Synthesis│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

1. **Node.js** (v18 or higher) - [Download](https://nodejs.org/)
2. **Python** (3.9 or higher) - [Download](https://python.org/)
3. **Ollama** - [Install Guide](https://ollama.ai/)
4. **Git** - [Download](https://git-scm.com/)

### 🎯 One-Command Setup

```bash
# From the python_services directory
python start_enhanced_system.py
```

This script will:
- ✅ Check Ollama status and pull required models
- ✅ Verify environment variables
- ✅ Install all dependencies
- ✅ Start all services (Python API, Backend, Frontend)
- ✅ Open browser to login page

## 🔧 Manual Setup (Alternative)

### 1. Environment Configuration

Create `.env` files in both `frontend` and `backend` directories:

**Frontend `.env.local`:**
```env
# Required
JWT_SECRET="your-secure-32-byte-key"
NEXT_PUBLIC_BASE_URL="http://localhost:3000"

# Optional (for enhanced features)
URLHAUS_AUTH_KEY="your-urlhaus-api-key"
NEXT_PUBLIC_TURNSTILE_SITE_KEY="your-turnstile-site-key"
TURNSTILE_SECRET_KEY="your-turnstile-secret-key"
```

**Backend `.env`:**
```env
JWT_SECRET="your-secure-32-byte-key"
PYTHON_SERVICE_URL="http://localhost:8000"
```

**Python Services `.env`:**
```env
URLHAUS_AUTH_KEY="your-urlhaus-api-key"
```

### 2. Generate JWT Secret

```bash
# Using OpenSSL (Linux/Mac)
openssl rand -base64 32

# Using Node.js (Windows/Universal)
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

### 3. Install Ollama and Models

```bash
# Install Ollama (follow platform-specific instructions)
# Then pull the required model
ollama pull llama3.2-vision:11b
```

### 4. Install Dependencies

**Python Services:**
```bash
cd python_services
pip install -r requirements.txt
```

**Backend:**
```bash
cd backend
npm install
```

**Frontend:**
```bash
cd frontend
npm install
```

### 5. Start Services

**Terminal 1 - Python API:**
```bash
cd python_services
python ai_training/enhanced_anime_api_server.py
```

**Terminal 2 - Backend:**
```bash
cd backend
npm start
# or
node server.js
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```

## 🎭 Character Profiles

### AI-chan (明愛) - The Phishing Detector
- **Personality**: Cheerful, energetic anime girl
- **Specialty**: URL and image analysis for phishing detection
- **Voice**: Female Japanese voice saying "危険です！" (It's dangerous!)
- **Enhanced with**: URLhaus threat intelligence
- **Capabilities**:
  - Real-time URL analysis
  - Image-based phishing detection
  - Confidence scoring
  - Voice warnings

### Haru (晴) - The Recovery Specialist
- **Personality**: Lazy but caring anime boy
- **Specialty**: Recovery assistance and cybersecurity education
- **Voice**: Male Japanese voice saying "めんどくさいな..." (It's a pain in the ass...)
- **Enhanced with**: Advanced analysis algorithms
- **Capabilities**:
  - Step-by-step recovery guidance
  - Screenshot analysis
  - Educational responses
  - Lazy but helpful comments

## 🔐 Authentication System

### Login Credentials (Demo)
- **Regular User**: user@example.com / password123
- **Admin User**: admin@example.com / admin123

### Security Features
- JWT-based authentication with httpOnly cookies
- Data Access Layer (DAL) following Next.js 15 best practices
- Protected routes with middleware
- Role-based access control
- Session management with automatic refresh

### Authentication Flow
1. User visits protected route (`/anime`)
2. Middleware checks for valid JWT token
3. If no token, redirects to `/login`
4. After successful login, creates secure session
5. DAL verifies user on each request

## 🌐 API Endpoints

### Python API (Port 8000)

**Core Endpoints:**
- `GET /` - System information
- `GET /health` - Health check
- `GET /anime/status` - Character status

**AI-chan Endpoints:**
- `GET /anime/ai-chan/greeting` - Get greeting
- `POST /anime/ai-chan/analyze` - Analyze URL/image

**Haru Endpoints:**
- `GET /anime/haru/greeting` - Get greeting  
- `POST /anime/haru/help` - Get recovery assistance

### Backend API (Port 3001)

**Authentication:**
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

**Anime Routes:**
- `GET /api/anime/ai-chan/greeting` - AI-chan greeting
- `POST /api/anime/ai-chan/analyze` - AI-chan analysis
- `GET /api/anime/haru/greeting` - Haru greeting
- `POST /api/anime/haru/help` - Haru assistance
- `GET /api/anime/voice/:filename` - Download voice files

### Frontend (Port 3000)

**Public Routes:**
- `/login` - Login page
- `/` - Public landing page

**Protected Routes:**
- `/anime` - Main anime dashboard (requires authentication)
- `/dashboard` - User dashboard
- `/admin` - Admin panel (admin role only)

## 🎯 Features

### 🔍 Enhanced Threat Detection
- **URLhaus Integration**: Real-time threat intelligence from abuse.ch
- **Pattern Matching**: Advanced suspicious pattern detection
- **Confidence Scoring**: AI-driven confidence assessment
- **Multi-source Analysis**: Combines multiple threat indicators

### 👁️ Vision Analysis
- **Image Scanning**: Analyzes uploaded images for phishing indicators
- **Screenshot Analysis**: Examines website screenshots for threats
- **Visual Pattern Recognition**: Detects suspicious visual elements
- **OCR Capabilities**: Extracts and analyzes text from images

### 🎌 Character Interactions
- **Personality-driven Responses**: Each character has unique response patterns
- **Contextual Reactions**: Responses adapt based on threat level and user behavior
- **Educational Content**: Haru provides learning opportunities
- **Emotional Intelligence**: Characters respond appropriately to user stress levels

### 🔊 Voice Synthesis
- **Japanese TTS**: Native Japanese voice synthesis
- **Character Voices**: Distinct voices for AI-chan and Haru
- **Contextual Audio**: Voice responses triggered by specific events
- **Emotion Modeling**: Voice tone matches character personality

## 🛡️ Security Features

### Authentication & Authorization
- **JWT Tokens**: Secure token-based authentication
- **httpOnly Cookies**: XSS-resistant token storage
- **CSRF Protection**: Built-in CSRF protection
- **Role-based Access**: User and admin role separation

### Data Protection
- **Input Validation**: Comprehensive input sanitization
- **File Upload Security**: Secure file handling with type/size limits
- **API Rate Limiting**: Protection against abuse
- **Error Handling**: Secure error responses

### Infrastructure Security
- **CORS Configuration**: Proper cross-origin resource sharing
- **Environment Variables**: Secure configuration management
- **Dependency Management**: Regular security updates
- **Logging**: Comprehensive security event logging

## 🧪 Testing

### Manual Testing Endpoints

**Test Phishing Detection:**
```bash
# Test suspicious URL
curl -X POST http://localhost:8000/anime/ai-chan/analyze \
  -F "url=http://phishing-example.com/login"

# Test legitimate URL
curl -X POST http://localhost:8000/anime/ai-chan/analyze \
  -F "url=https://google.com"
```

**Test Authentication:**
```bash
# Login
curl -X POST http://localhost:3001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Access protected endpoint
curl -X GET http://localhost:3000/anime \
  -H "Cookie: session-token=your-jwt-token"
```

### Health Checks
- Python API: http://localhost:8000/health
- Backend API: http://localhost:3001/api/health
- Frontend: http://localhost:3000

## 🔧 Troubleshooting

### Common Issues

**Ollama Not Running:**
```bash
# Start Ollama service
ollama serve

# Pull required model
ollama pull llama3.2-vision:11b
```

**Port Conflicts:**
```bash
# Check what's using ports
netstat -ano | findstr :3000
netstat -ano | findstr :3001
netstat -ano | findstr :8000

# Kill processes if needed
taskkill /PID <process-id> /F
```

**Environment Variables:**
```bash
# Check if JWT_SECRET is set
echo $JWT_SECRET   # Linux/Mac
echo %JWT_SECRET%  # Windows
```

**Dependencies:**
```bash
# Reinstall Python dependencies
pip install --force-reinstall -r requirements.txt

# Reinstall Node dependencies
rm -rf node_modules package-lock.json
npm install
```

### Debug Mode

**Enable Debug Logging:**
```bash
# Python API
PYTHONPATH=. python -m uvicorn enhanced_anime_api_server:app --reload --log-level debug

# Backend with debug
DEBUG=* npm start

# Frontend with debug
DEBUG=* npm run dev
```

## 🚀 Production Deployment

### Environment Setup
1. Set strong JWT secrets
2. Configure proper CORS origins
3. Use HTTPS for all communications
4. Set up proper database (replace mock authentication)
5. Configure environment-specific URLs

### Security Checklist
- [ ] Change all default passwords
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS
- [ ] Configure rate limiting
- [ ] Set up monitoring and logging
- [ ] Regular security updates

### Performance Optimization
- [ ] Enable Redis for session storage
- [ ] Configure CDN for static assets
- [ ] Optimize image uploads
- [ ] Implement caching strategies
- [ ] Monitor API response times

## 📊 Monitoring

### Key Metrics
- Authentication success/failure rates
- API response times
- Threat detection accuracy
- User engagement metrics
- System resource usage

### Logging
- Authentication events
- Threat detection results
- API access patterns
- Error conditions
- Performance metrics

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Follow coding standards
4. Add tests for new features
5. Submit pull request

### Code Style
- Python: PEP 8
- JavaScript/TypeScript: ESLint + Prettier
- Commit messages: Conventional Commits

## 📞 Support

### Getting Help
1. Check this guide first
2. Review troubleshooting section
3. Check GitHub issues
4. Contact development team

### Reporting Issues
1. Include system information
2. Provide error logs
3. Steps to reproduce
4. Expected vs actual behavior

---

## 🎉 Conclusion

You now have a complete, production-ready anime AI phishing detection system with:

✅ **Enhanced Security** - JWT authentication, protected routes, secure file handling  
✅ **Real Threat Intelligence** - URLhaus integration for accurate threat detection  
✅ **Modern Architecture** - Next.js 15, FastAPI, and best practices  
✅ **Character Personalities** - Engaging anime AI assistants  
✅ **Vision Capabilities** - Advanced image analysis with LLaVA  
✅ **Japanese Voice Synthesis** - Authentic character voices  
✅ **Educational Features** - Recovery assistance and cybersecurity education  

**Happy Phishing Protection! 🛡️✨** 
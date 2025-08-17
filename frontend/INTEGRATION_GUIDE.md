# PhishGuard Integration Guide

This guide explains how the complete PhishGuard system works with Python microservices, Express.js backend, and Next.js frontend.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Next.js       │    │   Express.js    │    │   Python        │
│   Frontend      │───▶│   Backend       │───▶│   Microservices │
│   (Port 3001)   │    │   (Port 3000)   │    │   (Port 8000)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### 1. Start Python Microservices
```bash
cd python_services
python start_service.py
```
- Service runs on: http://localhost:8000
- API docs: http://localhost:8000/docs

### 2. Start Express.js Backend
```bash
cd backend
npm install
npm run dev
```
- Service runs on: http://localhost:3000
- Health check: http://localhost:3000/api/phishguard/health

### 3. Start Next.js Frontend
```bash
cd frontend
npm run dev
```
- App runs on: http://localhost:3001

## 🔧 Configuration

### Backend Environment (.env in backend/)
```env
# Database
DB_URL=mongodb://localhost:27017/phishguard

# JWT Configuration
JWT_SECRET=your_super_secret_jwt_key_here
JWT_EXPIRES_IN=1d

# Python Service Configuration
PYTHON_SERVICE_URL=http://localhost:8000
PYTHON_SERVICE_PORT=8000

# Server Configuration
PORT=3000
```

### Frontend Environment (.env.local in frontend/)
```env
NEXT_PUBLIC_API_URL=http://localhost:3000
```

## 📱 User Interface Features

### 1. Landing Page Scanner Preview
- **Location**: Main page (`/`)
- **Features**:
  - Real-time URL analysis
  - AI chat assistant
  - Message analysis
  - Screenshot upload (UI ready)
- **Integration**: Connects directly to backend API

### 2. Authentication System
- **Login Page** (`/login`): Integrated with backend auth
- **Register Page** (`/register`): Multi-step form with validation
- **Features**:
  - JWT token management
  - Form validation
  - Error handling
  - Auto-redirect to dashboard

### 3. Dashboard (`/dashboard`)
- **URL Scanner**: Real-time phishing detection
- **AI Assistant**: Chat with bot for help
- **Safety Tips**: Dynamic tips from Python service
- **Quick Stats**: User activity tracking
- **Quick Actions**: History, analytics, reporting

## 🔌 API Integration

### Frontend → Backend Communication
The frontend uses the `src/lib/api.ts` utility for all API calls:

```typescript
// Authentication
const loginResult = await authApi.login({ email, password });
const registerResult = await authApi.register(userData);

// PhishGuard Features
const analysisResult = await phishguardApi.analyzeUrl(url);
const chatResult = await phishguardApi.chatWithBot(message);
const tipsResult = await phishguardApi.getSafetyTips();
```

### Backend → Python Communication
The Express.js backend acts as a proxy to Python services:

```javascript
// Example: URL Analysis
const response = await axios.post(`${PYTHON_SERVICE_URL}/analyze`, {
  url,
  user_id: req.user?.id
});
```

## 🎨 Design System

### Color Scheme
- **Primary**: Blue (`rgb(142, 197, 255)`)
- **Secondary**: Pink (`rgb(232, 118, 152)`)
- **Gradients**: Primary to Secondary transitions
- **Dark Mode**: Automatic theme detection

### Components
- **Cards**: Shadow-2xl with border-0
- **Buttons**: Gradient backgrounds for primary actions
- **Badges**: Color-coded threat levels
- **Animations**: Framer Motion with staggered delays

### Typography
- **Font**: Quicksand
- **Headings**: Bold with gradient underlines
- **Body**: Clean, readable text

## 🔍 Testing the System

### 1. Test URL Analysis
1. Go to http://localhost:3001
2. Scroll to "Interactive Scanner Preview"
3. Enter a suspicious URL (e.g., `http://suspicious-site.com`)
4. Click "Analyze"
5. View real-time results from Python service

### 2. Test AI Chat
1. In the scanner preview, switch to "Chat (AI)" tab
2. Ask questions like:
   - "How can I check if a link is safe?"
   - "What should I do if I clicked a suspicious link?"
   - "Tell me about phishing scams"

### 3. Test Authentication
1. Go to http://localhost:3001/register
2. Create a new account
3. Verify email validation and password strength
4. Complete registration
5. Login at http://localhost:3001/login
6. Access dashboard

### 4. Test Dashboard Features
1. Login to dashboard
2. Try URL analysis with real results
3. Chat with AI assistant
4. View safety tips
5. Test logout functionality

## 🛠️ Development Workflow

### Making Changes
1. **Frontend**: Edit files in `src/`
2. **Backend**: Edit files in `backend/`
3. **Python**: Edit files in `python_services/`

### Auto-reload
- **Frontend**: Next.js hot reload
- **Backend**: Nodemon auto-restart
- **Python**: Uvicorn reload enabled

### Testing API Endpoints
```bash
# Test backend health
curl http://localhost:3000/api/phishguard/health

# Test Python service
curl http://localhost:8000/

# Test URL analysis (requires auth)
curl -X POST http://localhost:3000/api/phishguard/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"url": "https://example.com"}'
```

## 🔒 Security Features

### Authentication
- JWT tokens with expiration
- Secure password hashing (bcrypt)
- Form validation and sanitization
- Protected API endpoints

### API Security
- CORS configuration
- Request validation
- Error handling
- Rate limiting (can be added)

### Frontend Security
- Token storage in localStorage
- Automatic token validation
- Protected routes
- Input sanitization

## 📊 Monitoring & Debugging

### Backend Logs
```bash
cd backend
npm run dev
# Watch for connection logs and API calls
```

### Python Service Logs
```bash
cd python_services
python start_service.py
# Watch for analysis logs and errors
```

### Frontend Debugging
- Open browser DevTools
- Check Network tab for API calls
- Check Console for errors
- Use React DevTools for component debugging

### Health Checks
```bash
# Backend health
curl http://localhost:3000/api/phishguard/health

# Python service health
curl http://localhost:8000/
```

## 🚀 Production Deployment

### Environment Setup
1. Set production environment variables
2. Configure database connections
3. Set up SSL certificates
4. Configure reverse proxy (Nginx)

### Services
1. **Python**: Use Gunicorn with multiple workers
2. **Backend**: Use PM2 for process management
3. **Frontend**: Build and serve static files

### Monitoring
1. Set up logging (Winston, etc.)
2. Configure error tracking (Sentry)
3. Set up health checks
4. Monitor API performance

## 🐛 Troubleshooting

### Common Issues

1. **Python Service Not Responding**
   - Check if service is running on port 8000
   - Verify dependencies are installed
   - Check Python logs for errors

2. **Backend Connection Issues**
   - Verify MongoDB is running
   - Check environment variables
   - Ensure Python service is accessible

3. **Frontend API Errors**
   - Check `NEXT_PUBLIC_API_URL` environment variable
   - Verify backend is running
   - Check browser console for CORS errors

4. **Authentication Issues**
   - Verify JWT_SECRET is set
   - Check token expiration
   - Ensure database is connected

### Debug Commands
```bash
# Test all services
cd backend
npm run test:connection

# Check service status
netstat -ano | findstr :3000  # Backend
netstat -ano | findstr :8000  # Python
netstat -ano | findstr :3001  # Frontend
```

## 📈 Future Enhancements

### Planned Features
1. **Real-time Notifications**: WebSocket integration
2. **Advanced Analytics**: User behavior tracking
3. **Mobile App**: React Native version
4. **Browser Extension**: Chrome/Firefox extension
5. **API Rate Limiting**: Protect against abuse
6. **Multi-language Support**: Internationalization

### Performance Optimizations
1. **Caching**: Redis for API responses
2. **CDN**: Static asset delivery
3. **Database Indexing**: Optimize queries
4. **Image Optimization**: Next.js image optimization

This integration provides a complete, production-ready phishing detection system with a beautiful, responsive UI that seamlessly connects to powerful Python microservices through a robust Express.js backend. 
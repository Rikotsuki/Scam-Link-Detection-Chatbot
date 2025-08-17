# PhishGuard Backend API

This is the Express.js backend that serves as a bridge between the Next.js frontend and Python microservices for the PhishGuard phishing detection system.

## Architecture

```
Frontend (Next.js) → Express.js Backend → Python Microservices (FastAPI)
```

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file with the following variables:
```env
# Database
DB_URL=mongodb://localhost:27017/phishguard

# JWT Configuration
JWT_SECRET=your_jwt_secret_here
JWT_EXPIRES_IN=1d

# Python Service Configuration
PYTHON_SERVICE_URL=http://localhost:8000
PYTHON_SERVICE_PORT=8000

# Server Configuration
PORT=3000
```

3. Start the backend:
```bash
# Development mode with auto-reload
npm run dev

# Production mode
npm start
```

## API Endpoints

### Authentication Endpoints

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login user

### PhishGuard API Endpoints

All PhishGuard endpoints are prefixed with `/api/phishguard/`

#### 1. Analyze URL
```http
POST /api/phishguard/analyze
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "url": "https://example.com/suspicious-link",
  "user_id": "optional_user_id"
}
```

**Response:**
```json
{
  "url": "https://example.com/suspicious-link",
  "is_suspicious": true,
  "threat_level": "high",
  "message": "This URL appears to be a phishing attempt",
  "confidence": 0.95,
  "detection_methods": ["urlhaus", "ai_analysis"],
  "warnings": ["Suspicious domain", "Phishing indicators detected"],
  "analysis_time": 1.2
}
```

#### 2. Report Scam
```http
POST /api/phishguard/report
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "url": "https://example.com/scam-site",
  "description": "This site is trying to steal my credit card information",
  "user_id": "optional_user_id"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Scam reported successfully",
  "report_id": "report_12345"
}
```

#### 3. Get Safety Tips
```http
GET /api/phishguard/tips
```

**Response:**
```json
{
  "tips": [
    "Never click on suspicious links in emails",
    "Check the URL carefully before entering credentials",
    "Use two-factor authentication when possible"
  ],
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 4. Chat with Bot
```http
POST /api/phishguard/chat
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "message": "How can I check if a link is safe?",
  "user_id": "optional_user_id",
  "session_id": "optional_session_id"
}
```

**Response:**
```json
{
  "response": "I can help you check if a link is safe! Please paste the URL you'd like me to analyze.",
  "confidence": 0.8,
  "suggestions": ["Paste the suspicious URL here"],
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 5. Health Check
```http
GET /api/phishguard/health
```

**Response:**
```json
{
  "status": "healthy",
  "python_service": "connected",
  "message": "PhishGuard API - Protecting Myanmar from phishing scams"
}
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `400` - Bad Request (missing required fields)
- `401` - Unauthorized (invalid or missing token)
- `500` - Internal Server Error
- `503` - Service Unavailable (Python service not responding)

## Python Service Integration

The backend acts as a proxy to the Python FastAPI service. It:

1. Validates JWT tokens
2. Forwards requests to the Python service
3. Handles errors and timeouts
4. Provides a unified API interface

### Environment Variables for Python Service

- `PYTHON_SERVICE_URL` - Base URL of the Python service (default: http://localhost:8000)
- `PYTHON_SERVICE_PORT` - Port of the Python service (default: 8000)

## Development

### Running Both Services

1. Start the Python service:
```bash
cd ../python_services
python start_service.py
```

2. Start the Express.js backend:
```bash
cd ../backend
npm run dev
```

3. Start the Next.js frontend:
```bash
cd ../frontend
npm run dev
```

### Testing the Connection

You can test if the services are connected by calling the health check endpoint:

```bash
curl http://localhost:3000/api/phishguard/health
```

## Security

- All sensitive endpoints require JWT authentication
- Tokens are validated on each request
- User IDs are automatically extracted from tokens
- CORS is configured for frontend communication

## Troubleshooting

### Python Service Not Responding

1. Check if the Python service is running on the correct port
2. Verify the `PYTHON_SERVICE_URL` environment variable
3. Check Python service logs for errors

### Authentication Issues

1. Ensure JWT_SECRET is set correctly
2. Check token expiration
3. Verify token format in Authorization header

### Database Connection Issues

1. Ensure MongoDB is running
2. Check the `DB_URL` environment variable
3. Verify network connectivity 
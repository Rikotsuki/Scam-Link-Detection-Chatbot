# PhishGuard Startup Guide

This guide will help you start all three services for the PhishGuard phishing detection system.

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Next.js       │    │   Express.js    │    │   Python        │
│   Frontend      │───▶│   Backend       │───▶│   Microservices │
│   (Port 3001)   │    │   (Port 3000)   │    │   (Port 8000)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Prerequisites

1. **Node.js** (v16 or higher)
2. **Python** (v3.8 or higher)
3. **MongoDB** (running locally or cloud instance)
4. **Git** (to clone the repository)

## Step 1: Setup Environment Variables

### Backend (.env file in `backend/` directory)
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

### Frontend (.env.local file in `frontend/` directory)
```env
NEXT_PUBLIC_API_URL=http://localhost:3000
```

### Python Services (.env file in `python_services/` directory)
```env
# Copy from env.example and configure as needed
URLHAUS_AUTH_KEY=your_urlhaus_key_here
```

## Step 2: Install Dependencies

### Backend
```bash
cd backend
npm install
```

### Frontend
```bash
cd frontend
npm install
```

### Python Services
```bash
cd python_services
pip install -r requirements.txt
```

## Step 3: Start Services

### 1. Start Python Microservices
```bash
cd python_services
python start_service.py
```

**Expected output:**
```
Starting PhishGuard Python API service on 0.0.0.0:8000
API Documentation available at:
  - Swagger UI: http://0.0.0.0:8000/docs
  - ReDoc: http://0.0.0.0:8000/redoc
```

**Verify:** Visit http://localhost:8000/docs to see the API documentation.

### 2. Start Express.js Backend
```bash
cd backend
npm run dev
```

**Expected output:**
```
DB connected
server running at localhost:3000
```

**Verify:** Visit http://localhost:3000/api/phishguard/health to check the health status.

### 3. Start Next.js Frontend
```bash
cd frontend
npm run dev
```

**Expected output:**
```
- ready started server on 0.0.0.0:3001
```

**Verify:** Visit http://localhost:3001 to see the frontend.

## Step 4: Test the Connection

### Option 1: Use the Test Script
```bash
cd backend
npm run test:connection
```

### Option 2: Manual Testing

1. **Test Python Service Directly:**
   ```bash
   curl http://localhost:8000/
   ```

2. **Test Express.js Backend:**
   ```bash
   curl http://localhost:3000/api/phishguard/health
   ```

3. **Test Frontend API Integration:**
   - Visit http://localhost:3001
   - Navigate to the API example page (if you add the component)
   - Try the health check button

## Step 5: API Endpoints

### Authentication (Express.js Backend)
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login user

### PhishGuard API (Express.js → Python)
- `POST /api/phishguard/analyze` - Analyze URL for phishing
- `POST /api/phishguard/report` - Report a scam
- `GET /api/phishguard/tips` - Get safety tips
- `POST /api/phishguard/chat` - Chat with bot
- `GET /api/phishguard/health` - Health check

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find process using port
   netstat -ano | findstr :3000
   # Kill process (replace PID with actual process ID)
   taskkill /PID <PID> /F
   ```

2. **MongoDB Not Running**
   ```bash
   # Start MongoDB (Windows)
   net start MongoDB
   
   # Or use MongoDB Atlas (cloud)
   # Update DB_URL in .env file
   ```

3. **Python Dependencies Missing**
   ```bash
   cd python_services
   pip install -r requirements.txt
   ```

4. **CORS Issues**
   - Check that the frontend is making requests to the correct backend URL
   - Verify the `NEXT_PUBLIC_API_URL` environment variable

5. **JWT Token Issues**
   - Ensure `JWT_SECRET` is set in the backend `.env` file
   - Check that tokens are being stored and sent correctly from frontend

### Service Status Check

```bash
# Check if all services are running
curl http://localhost:8000/     # Python service
curl http://localhost:3000/api/phishguard/health  # Express.js backend
curl http://localhost:3001/     # Next.js frontend
```

## Development Workflow

1. **Start all services** (as described above)
2. **Make changes** to any service
3. **Services auto-reload** (Python and Express.js with nodemon)
4. **Test changes** using the API endpoints or frontend
5. **Check logs** in each terminal for errors

## Production Deployment

For production, you'll want to:

1. **Use PM2** for Node.js services
2. **Use Gunicorn** for Python services
3. **Set up reverse proxy** (Nginx/Apache)
4. **Use environment-specific** configuration files
5. **Set up monitoring** and logging
6. **Configure SSL certificates**

## Support

If you encounter issues:

1. Check the logs in each terminal
2. Verify all environment variables are set
3. Ensure all dependencies are installed
4. Test each service individually
5. Check the API documentation at http://localhost:8000/docs 
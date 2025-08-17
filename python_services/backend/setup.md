# PhishGuard Express.js Backend Setup Guide

## 🏗️ Architecture Overview

This setup uses a **dual-database architecture**:

- **MongoDB**: User management, authentication, and application data
- **PostgreSQL + pgvector**: AI/ML data, embeddings, training data, and analytics

## 📋 Prerequisites

1. **Node.js** (v18 or higher)
2. **MongoDB** (v5 or higher)
3. **PostgreSQL** (v14 or higher) with pgvector extension
4. **Python** (v3.8+) for AI microservice

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
cd backend
npm install
```

### 2. Database Setup

#### MongoDB Setup
```bash
# Install MongoDB (Ubuntu/Debian)
sudo apt update
sudo apt install mongodb

# Start MongoDB
sudo systemctl start mongodb
sudo systemctl enable mongodb

# Create database
mongosh
use phishguard_users
```

#### PostgreSQL Setup
```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql postgresql-contrib

# Install pgvector extension
sudo apt install postgresql-14-pgvector  # Adjust version as needed

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql

CREATE DATABASE phishguard_ai;
CREATE USER phishguard_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE phishguard_ai TO phishguard_user;
\c phishguard_ai
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgvector";
\q
```

### 3. Environment Configuration

Create `.env` file in the backend directory:

```env
# Server Configuration
PORT=3000
NODE_ENV=development

# MongoDB (User Management & Application Data)
DB_URL=mongodb://localhost:27017/phishguard_users

# PostgreSQL (AI/ML Data)
DATABASE_URL=postgresql://phishguard_user:your_secure_password@localhost:5432/phishguard_ai

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
JWT_EXPIRES_IN=1d

# AI Service Configuration
AI_SERVICE_URL=http://localhost:8000
AI_SERVICE_API_KEY=your-ai-service-api-key

# OpenAI Configuration (for embeddings)
OPENAI_API_KEY=your-openai-api-key

# Redis (for caching and job queues)
REDIS_URL=redis://localhost:6379

# Security
CORS_ORIGIN=http://localhost:3001

# Rate Limiting
RATE_LIMIT_WINDOW=15
RATE_LIMIT_MAX=100
```

### 4. Database Schema Setup

#### PostgreSQL Schema
```bash
# Run the database schema
psql -U phishguard_user -d phishguard_ai -f ../database-setup.sql
```

#### Prisma Setup
```bash
# Generate Prisma client
npm run db:generate

# Push schema to database
npm run db:push

# (Optional) Open Prisma Studio
npm run db:studio
```

### 5. Start the Server

```bash
# Development mode
npm run dev

# Production mode
npm run build
npm start
```

## 🔧 Configuration Details

### Database Connections

#### MongoDB (User Management)
- **Purpose**: User accounts, authentication, sessions
- **Connection**: `mongodb://localhost:27017/phishguard_users`
- **Collections**: `users`, `sessions`, `user_preferences`

#### PostgreSQL (AI/ML Data)
- **Purpose**: AI training data, embeddings, analytics
- **Connection**: `postgresql://user:password@localhost:5432/phishguard_ai`
- **Extensions**: `pgvector` for vector similarity search
- **Tables**: `scam_urls`, `detection_history`, `knowledge_base`, `chat_messages`

### API Endpoints

#### Authentication Routes (`/auth`)
- `POST /auth/register` - User registration
- `POST /auth/login` - User login

#### AI Routes (`/api/ai`)
- `POST /api/ai/analyze` - Analyze URL for threats
- `POST /api/ai/chat` - Chat with AI chatbot
- `POST /api/ai/report` - Report scam URL
- `GET /api/ai/tips` - Get safety tips
- `GET /api/ai/intelligence` - Get threat intelligence
- `GET /api/ai/health` - AI service health check
- `GET /api/ai/stats` - AI service statistics (admin only)

#### Private Routes (`/private`)
- Protected routes requiring authentication

### Security Features

1. **JWT Authentication**: Secure token-based authentication
2. **Rate Limiting**: Prevents abuse of AI endpoints
3. **CORS Protection**: Configurable cross-origin requests
4. **Helmet.js**: Security headers
5. **Input Validation**: Request validation using express-validator
6. **API Key Protection**: For AI service communication

## 🔄 AI Service Integration

The Express.js backend communicates with your Python AI microservice:

### Communication Flow
1. **Frontend** → **Express.js** → **Python AI Service**
2. **Express.js** stores results in **PostgreSQL**
3. **Fallback mechanisms** when AI service is unavailable

### API Key Authentication
- AI service requests include `Authorization: Bearer <api-key>`
- Configured via `AI_SERVICE_API_KEY` environment variable

## 📊 Monitoring & Analytics

### Health Checks
- `GET /health` - Backend health
- `GET /api/ai/health` - AI service health

### Statistics
- `GET /api/ai/stats` - AI service statistics (admin only)
- Includes detection counts, response times, error rates

### Logging
- Request logging with Morgan
- Error logging with Winston
- Database query logging in development

## 🚀 Deployment

### Development
```bash
npm run dev
```

### Production
```bash
npm run build
npm start
```

### Docker (Optional)
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 🔍 Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check MongoDB/PostgreSQL services are running
   - Verify connection strings in `.env`
   - Ensure database permissions are correct

2. **AI Service Connection Errors**
   - Verify Python AI service is running on port 8000
   - Check `AI_SERVICE_API_KEY` is correct
   - Review AI service logs for errors

3. **Prisma Errors**
   - Run `npm run db:generate` to regenerate client
   - Check PostgreSQL connection and permissions
   - Verify pgvector extension is installed

4. **CORS Errors**
   - Update `CORS_ORIGIN` in `.env` to match frontend URL
   - Check frontend is making requests to correct backend URL

### Logs
- Check console output for detailed error messages
- Review MongoDB and PostgreSQL logs
- Monitor AI service logs separately

## 📚 Next Steps

1. **Start Python AI Service**: Ensure your Python FastAPI service is running
2. **Test API Endpoints**: Use tools like Postman or curl to test endpoints
3. **Connect Frontend**: Update your Next.js frontend to use these endpoints
4. **Monitor Performance**: Set up monitoring for both databases and services
5. **Scale Up**: Consider Redis for caching and Bull for job queues

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review logs for specific error messages
3. Verify all services are running and accessible
4. Test database connections individually 
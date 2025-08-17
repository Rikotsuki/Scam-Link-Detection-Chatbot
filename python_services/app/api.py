from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict
import uvicorn
import logging
from datetime import datetime
import json

from .phish_core import PhishGuardCore
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="PhishGuard API",
    description="AI-powered phishing detection chatbot for Myanmar",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize PhishGuard core with URLhaus auth key if available
urlhaus_auth_key = os.getenv('URLHAUS_AUTH_KEY')
phish_guard = PhishGuardCore(urlhaus_auth_key=urlhaus_auth_key)

# Security
security = HTTPBearer()

# Pydantic models
class URLAnalysisRequest(BaseModel):
    url: str
    user_id: Optional[str] = None

class URLAnalysisResponse(BaseModel):
    url: str
    is_suspicious: bool
    threat_level: str
    message: str
    confidence: float
    detection_methods: List[str]
    warnings: List[str]
    analysis_time: float

class ScamReportRequest(BaseModel):
    url: str
    description: str
    user_id: Optional[str] = None

class ScamReportResponse(BaseModel):
    success: bool
    message: str
    report_id: Optional[str] = None

class SafetyTipsResponse(BaseModel):
    tips: List[str]
    timestamp: datetime

class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    confidence: float
    suggestions: List[str]
    timestamp: datetime

# In-memory storage (replace with proper database in production)
reported_scams = []
chat_sessions = {}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "PhishGuard API - Protecting Myanmar from phishing scams",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "analyze_url": "/analyze",
            "report_scam": "/report",
            "safety_tips": "/tips",
            "chat": "/chat"
        }
    }

@app.post("/analyze", response_model=URLAnalysisResponse)
async def analyze_url(request: URLAnalysisRequest):
    """
    Analyze a URL for phishing threats
    """
    try:
        logger.info(f"Analyzing URL: {request.url}")
        
        # Perform URL analysis
        result = phish_guard.analyze_url(request.url)
        
        # Log the analysis
        logger.info(f"Analysis result: {result['threat_level']} - {result['message']}")
        
        return URLAnalysisResponse(
            url=result['url'],
            is_suspicious=result['is_suspicious'],
            threat_level=result['threat_level'],
            message=result['message'],
            confidence=result['confidence'],
            detection_methods=result.get('detection_methods', []),
            warnings=result.get('warnings', []),
            analysis_time=result.get('analysis_time', 0)
        )
        
    except Exception as e:
        logger.error(f"Error analyzing URL: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/report", response_model=ScamReportResponse)
async def report_scam(request: ScamReportRequest, background_tasks: BackgroundTasks):
    """
    Report a scam URL for community protection
    """
    try:
        logger.info(f"Reporting scam: {request.url}")
        
        # Report the scam
        result = phish_guard.report_scam(
            url=request.url,
            description=request.description,
            user_id=request.user_id
        )
        
        # Store in memory (replace with database in production)
        if result['success']:
            reported_scams.append({
                'url': request.url,
                'description': request.description,
                'user_id': request.user_id,
                'timestamp': datetime.now().isoformat(),
                'report_id': result.get('report_id')
            })
        
        return ScamReportResponse(
            success=result['success'],
            message=result['message'],
            report_id=result.get('report_id')
        )
        
    except Exception as e:
        logger.error(f"Error reporting scam: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Report failed: {str(e)}")

@app.get("/tips", response_model=SafetyTipsResponse)
async def get_safety_tips():
    """
    Get digital safety tips for users
    """
    try:
        tips = phish_guard.get_safety_tips()
        return SafetyTipsResponse(
            tips=tips,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error getting safety tips: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get tips: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat_with_bot(request: ChatMessage):
    """
    Chat with the PhishGuard bot for guidance and help
    """
    try:
        message = request.message.lower().strip()
        response = ""
        confidence = 0.0
        suggestions = []
        
        # Simple intent recognition
        if any(word in message for word in ['link', 'url', 'check', 'scan']):
            response = "I can help you check if a link is safe! Please paste the URL you'd like me to analyze."
            confidence = 0.8
            suggestions = ["Paste the suspicious URL here"]
            
        elif any(word in message for word in ['scam', 'report', 'phishing']):
            response = "I can help you report a scam! Please provide the URL and describe what happened."
            confidence = 0.9
            suggestions = ["Report a scam URL", "Get safety tips"]
            
        elif any(word in message for word in ['help', 'tips', 'safe', 'protect']):
            response = "Here are some key safety tips:\n" + "\n".join(phish_guard.get_safety_tips()[:3])
            confidence = 0.9
            suggestions = ["Get all safety tips", "Check a URL", "Report a scam"]
            
        elif any(word in message for word in ['hacked', 'compromised', 'clicked']):
            response = "If you've clicked a suspicious link:\n1. Don't enter any information\n2. Change your passwords immediately\n3. Enable two-factor authentication\n4. Contact your bank if financial info was involved"
            confidence = 0.95
            suggestions = ["Report the scam", "Get recovery steps", "Check other URLs"]
            
        else:
            response = "Hello! I'm PhishGuard, your digital safety assistant. I can help you:\n• Check if links are safe\n• Report scams\n• Get safety tips\n• Help if you've been compromised\n\nWhat would you like to do?"
            confidence = 0.7
            suggestions = ["Check a URL", "Report a scam", "Get safety tips", "Emergency help"]
        
        return ChatResponse(
            response=response,
            confidence=confidence,
            suggestions=suggestions,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@app.get("/stats")
async def get_stats():
    """
    Get system statistics
    """
    try:
        return {
            "total_reports": len(reported_scams),
            "recent_reports": len([r for r in reported_scams if r['timestamp'] > (datetime.now().isoformat()[:-7])]),
            "active_sessions": len(chat_sessions),
            "system_status": "healthy",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Stats failed: {str(e)}")

@app.get("/reports")
async def get_recent_reports(limit: int = 10):
    """
    Get recent scam reports (for admin/monitoring)
    """
    try:
        # Return recent reports (limit for privacy)
        recent_reports = reported_scams[-limit:] if reported_scams else []
        
        # Anonymize user IDs for privacy
        for report in recent_reports:
            if report.get('user_id'):
                report['user_id'] = report['user_id'][:8] + "..."
        
        return {
            "reports": recent_reports,
            "total": len(reported_scams),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting reports: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Reports failed: {str(e)}")

# URLhaus intelligence endpoints
@app.get("/intelligence/recent-urls")
async def get_recent_malware_urls(limit: int = 10):
    """Get recent malware URLs from URLhaus"""
    try:
        if limit > 100:
            limit = 100  # Limit for API performance
            
        result = phish_guard.get_recent_urlhaus_urls(limit=limit)
        
        if not result.get('success'):
            raise HTTPException(status_code=503, detail=result.get('error', 'URLhaus API unavailable'))
        
        return {
            "recent_urls": result.get('urls', []),
            "count": result.get('count', 0),
            "timestamp": result.get('timestamp'),
            "limit": limit
        }
        
    except Exception as e:
        logger.error(f"Error getting recent URLs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get recent URLs: {str(e)}")

@app.get("/intelligence/recent-payloads")
async def get_recent_malware_payloads(limit: int = 10):
    """Get recent malware payloads from URLhaus"""
    try:
        if limit > 50:
            limit = 50  # Limit for API performance
            
        result = phish_guard.get_recent_urlhaus_payloads(limit=limit)
        
        if not result.get('success'):
            raise HTTPException(status_code=503, detail=result.get('error', 'URLhaus API unavailable'))
        
        return {
            "recent_payloads": result.get('payloads', []),
            "count": result.get('count', 0),
            "timestamp": result.get('timestamp'),
            "limit": limit
        }
        
    except Exception as e:
        logger.error(f"Error getting recent payloads: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get recent payloads: {str(e)}")

@app.get("/intelligence/summary")
async def get_intelligence_summary():
    """Get threat intelligence summary from URLhaus"""
    try:
        result = phish_guard.get_urlhaus_intelligence_summary()
        
        if not result.get('success'):
            raise HTTPException(status_code=503, detail=result.get('error', 'URLhaus API unavailable'))
        
        return result
        
    except Exception as e:
        logger.error(f"Error getting intelligence summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get intelligence summary: {str(e)}")

@app.post("/intelligence/search-tag")
async def search_by_tag(tag: str):
    """Search URLs by malware tag"""
    try:
        if not tag or len(tag.strip()) < 2:
            raise HTTPException(status_code=400, detail="Tag must be at least 2 characters")
        
        result = phish_guard.search_urlhaus_tag(tag.strip())
        
        if not result.get('success'):
            raise HTTPException(status_code=503, detail=result.get('error', 'URLhaus API unavailable'))
        
        return {
            "tag": tag,
            "url_count": result.get('url_count', 0),
            "urls": result.get('urls', [])[:20],  # Limit results
            "firstseen": result.get('firstseen'),
            "lastseen": result.get('lastseen')
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching by tag: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to search by tag: {str(e)}")

@app.post("/intelligence/check-host")
async def check_host_intelligence(host: str):
    """Check host information in URLhaus"""
    try:
        if not host or len(host.strip()) < 3:
            raise HTTPException(status_code=400, detail="Host must be at least 3 characters")
        
        result = phish_guard.check_urlhaus_host(host.strip())
        
        if not result.get('success'):
            raise HTTPException(status_code=503, detail=result.get('error', 'URLhaus API unavailable'))
        
        return {
            "host": host,
            "is_malicious": result.get('is_malicious', False),
            "url_count": result.get('url_count', 0),
            "blacklists": result.get('blacklists', {}),
            "firstseen": result.get('firstseen'),
            "threat_level": "critical" if result.get('is_malicious') else "safe"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking host: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to check host: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/detection-status")
async def get_detection_status():
    """Get status of all detection methods"""
    return {
        "detection_methods": phish_guard.get_detection_status(),
        "timestamp": datetime.now().isoformat(),
        "message": "URLhaus is PRIMARY method, others are FALLBACK"
    }

@app.get("/database/stats")
async def get_database_stats():
    """Get database statistics"""
    return {
        "database_stats": phish_guard.get_database_stats(),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/database/search")
async def search_database(domain: str):
    """Search database by domain"""
    results = phish_guard.db.search_scams_by_domain(domain)
    return {
        "domain": domain,
        "results": results,
        "count": len(results),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

"""
AI Service Integration for PhishGuard
Integrates trained AI models with existing backend services
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime
import requests
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import uvicorn

from ollama_integration import PhishGuardOllamaManager, PhishGuardAI, Haru

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for API requests/responses
class URLAnalysisRequest(BaseModel):
    url: HttpUrl
    user_id: Optional[str] = None
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    chatbot_type: str = "ai"  # "ai" or "haru"
    timestamp: Optional[str] = None

class ReportRequest(BaseModel):
    url: HttpUrl
    description: str
    user_id: Optional[str] = None
    timestamp: Optional[str] = None

class TipsRequest(BaseModel):
    category: Optional[str] = None
    context: Optional[str] = None

class URLAnalysisResponse(BaseModel):
    url: str
    threat_level: str
    confidence: float
    is_suspicious: bool
    detection_methods: List[str]
    warnings: List[str]
    ai_analysis: Optional[str] = None
    message: str
    timestamp: str

class ChatResponse(BaseModel):
    response: str
    session_id: str
    chatbot_type: str
    confidence: float
    timestamp: str

class ReportResponse(BaseModel):
    success: bool
    message: str
    report_id: Optional[str] = None
    timestamp: str

class TipsResponse(BaseModel):
    tips: List[str]
    category: Optional[str] = None
    source: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    ai_model_status: str
    haru_model_status: str
    ollama_status: str
    timestamp: str

class AIServiceIntegration:
    """Integration service for AI models with existing backend"""
    
    def __init__(self):
        self.app = FastAPI(
            title="PhishGuard AI Service",
            description="AI-powered phishing detection and recovery assistance",
            version="2.0.0"
        )
        
        # Setup CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Initialize Ollama manager
        self.ollama_manager = PhishGuardOllamaManager()
        self.ai_chatbot = self.ollama_manager.ai_chatbot
        self.haru_chatbot = self.ollama_manager.haru_chatbot
        
        # Setup routes
        self._setup_routes()
        
        # Health status
        self.health_status = {
            'ai_model': 'unknown',
            'haru_model': 'unknown',
            'ollama': 'unknown'
        }
    
    def _setup_routes(self):
        """Setup API routes"""
        
        @self.app.get("/", response_model=Dict)
        async def root():
            """Root endpoint with service information"""
            return {
                "service": "PhishGuard AI Service v2.0",
                "description": "AI-powered phishing detection and recovery assistance",
                "models": {
                    "ai": "PhishGuard AI - Phishing Detection",
                    "haru": "Haru - Recovery & Education"
                },
                "endpoints": {
                    "analyze": "/analyze",
                    "chat": "/chat",
                    "report": "/report",
                    "tips": "/tips",
                    "health": "/health"
                }
            }
        
        @self.app.post("/analyze", response_model=URLAnalysisResponse)
        async def analyze_url(request: URLAnalysisRequest):
            """Analyze URL for phishing threats using AI"""
            try:
                # Get AI analysis
                ai_result = self.ai_chatbot.analyze_url(str(request.url))
                
                # Determine threat level based on AI analysis
                threat_level = self._determine_threat_level(ai_result['analysis'])
                confidence = self._extract_confidence(ai_result['analysis'])
                is_suspicious = threat_level in ['high', 'critical']
                
                # Create response
                response = URLAnalysisResponse(
                    url=str(request.url),
                    threat_level=threat_level,
                    confidence=confidence,
                    is_suspicious=is_suspicious,
                    detection_methods=['ai_analysis'],
                    warnings=[ai_result['analysis']] if is_suspicious else [],
                    ai_analysis=ai_result['analysis'],
                    message=self._generate_response_message(threat_level, ai_result['analysis']),
                    timestamp=datetime.now().isoformat()
                )
                
                return response
                
            except Exception as e:
                logger.error(f"Error analyzing URL: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/chat", response_model=ChatResponse)
        async def chat_with_bot(request: ChatRequest):
            """Chat with either AI or Haru chatbot"""
            try:
                if request.chatbot_type.lower() == "haru":
                    # Use Haru for recovery and education
                    result = self.haru_chatbot.help_victim(request.message)
                    response_text = result['guidance']
                    confidence = 0.8
                else:
                    # Use AI for phishing detection and analysis
                    result = self.ai_chatbot.provide_safety_tips(request.message)
                    response_text = result['safety_tips']
                    confidence = 0.7
                
                response = ChatResponse(
                    response=response_text,
                    session_id=request.session_id or "default",
                    chatbot_type=request.chatbot_type,
                    confidence=confidence,
                    timestamp=datetime.now().isoformat()
                )
                
                return response
                
            except Exception as e:
                logger.error(f"Error in chat: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/report", response_model=ReportResponse)
        async def report_scam(request: ReportRequest):
            """Report a scam URL"""
            try:
                # Get AI analysis for additional context
                ai_result = self.ai_chatbot.analyze_url(str(request.url))
                
                # Generate report ID
                report_id = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                response = ReportResponse(
                    success=True,
                    message=f"Scam reported successfully. AI analysis: {ai_result['analysis'][:100]}...",
                    report_id=report_id,
                    timestamp=datetime.now().isoformat()
                )
                
                return response
                
            except Exception as e:
                logger.error(f"Error reporting scam: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/tips", response_model=TipsResponse)
        async def get_safety_tips(category: Optional[str] = None, context: Optional[str] = None):
            """Get safety tips from AI"""
            try:
                if context:
                    result = self.ai_chatbot.provide_safety_tips(context)
                    tips = [result['safety_tips']]
                else:
                    result = self.ai_chatbot.provide_safety_tips()
                    tips = [result['safety_tips']]
                
                response = TipsResponse(
                    tips=tips,
                    category=category,
                    source="ai_analysis",
                    timestamp=datetime.now().isoformat()
                )
                
                return response
                
            except Exception as e:
                logger.error(f"Error getting tips: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/health", response_model=HealthResponse)
        async def health_check():
            """Health check for all services"""
            try:
                # Test Ollama connection
                models = self.ollama_manager.client.list_models()
                ollama_status = "healthy" if models else "unhealthy"
                
                # Test AI model
                try:
                    ai_test = self.ai_chatbot.analyze_url("https://example.com")
                    ai_status = "healthy" if ai_test else "unhealthy"
                except:
                    ai_status = "unhealthy"
                
                # Test Haru model
                try:
                    haru_test = self.haru_chatbot.help_victim("test")
                    haru_status = "healthy" if haru_test else "unhealthy"
                except:
                    haru_status = "unhealthy"
                
                overall_status = "healthy" if all([
                    ollama_status == "healthy",
                    ai_status == "healthy",
                    haru_status == "healthy"
                ]) else "unhealthy"
                
                response = HealthResponse(
                    status=overall_status,
                    ai_model_status=ai_status,
                    haru_model_status=haru_status,
                    ollama_status=ollama_status,
                    timestamp=datetime.now().isoformat()
                )
                
                return response
                
            except Exception as e:
                logger.error(f"Health check error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/ai/analyze")
        async def ai_analyze_url(request: URLAnalysisRequest):
            """Direct AI analysis endpoint"""
            try:
                result = self.ai_chatbot.analyze_url(str(request.url))
                return result
            except Exception as e:
                logger.error(f"AI analysis error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/haru/help")
        async def haru_help_victim(request: ChatRequest):
            """Direct Haru help endpoint"""
            try:
                result = self.haru_chatbot.help_victim(request.message)
                return result
            except Exception as e:
                logger.error(f"Haru help error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/haru/educate")
        async def haru_educate(request: ChatRequest):
            """Haru education endpoint"""
            try:
                result = self.haru_chatbot.educate_user(request.message)
                return result
            except Exception as e:
                logger.error(f"Haru education error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/haru/recovery")
        async def haru_recovery_plan(request: ChatRequest):
            """Haru recovery plan endpoint"""
            try:
                result = self.haru_chatbot.recovery_plan(request.message)
                return result
            except Exception as e:
                logger.error(f"Haru recovery error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
    
    def _determine_threat_level(self, analysis: str) -> str:
        """Determine threat level from AI analysis"""
        analysis_lower = analysis.lower()
        
        if any(word in analysis_lower for word in ['critical', 'malware', 'confirmed', 'dangerous']):
            return 'critical'
        elif any(word in analysis_lower for word in ['high risk', 'suspicious', 'phishing', 'scam']):
            return 'high'
        elif any(word in analysis_lower for word in ['medium', 'concerning', 'caution']):
            return 'medium'
        elif any(word in analysis_lower for word in ['safe', 'clean', 'legitimate']):
            return 'safe'
        else:
            return 'unknown'
    
    def _extract_confidence(self, analysis: str) -> float:
        """Extract confidence score from AI analysis"""
        # Simple heuristic - can be improved with more sophisticated parsing
        analysis_lower = analysis.lower()
        
        if any(word in analysis_lower for word in ['confirmed', 'definitely', 'certainly']):
            return 0.95
        elif any(word in analysis_lower for word in ['likely', 'probably', 'strong']):
            return 0.8
        elif any(word in analysis_lower for word in ['possibly', 'might', 'could']):
            return 0.6
        elif any(word in analysis_lower for word in ['uncertain', 'unclear', 'unknown']):
            return 0.3
        else:
            return 0.5
    
    def _generate_response_message(self, threat_level: str, analysis: str) -> str:
        """Generate user-friendly response message"""
        if threat_level == 'critical':
            return f"🚨 CRITICAL WARNING: {analysis}"
        elif threat_level == 'high':
            return f"⚠️ HIGH RISK: {analysis}"
        elif threat_level == 'medium':
            return f"⚠️ SUSPICIOUS: {analysis}"
        elif threat_level == 'safe':
            return f"✅ SAFE: {analysis}"
        else:
            return f"❓ UNKNOWN: {analysis}"

def create_ai_service() -> FastAPI:
    """Create and return the AI service FastAPI app"""
    service = AIServiceIntegration()
    return service.app

def main():
    """Run the AI service"""
    app = create_ai_service()
    
    # Run the service
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,  # Different port from main backend
        log_level="info"
    )

if __name__ == "__main__":
    main() 
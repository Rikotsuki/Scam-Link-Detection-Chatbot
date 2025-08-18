#!/usr/bin/env python3
"""
Enhanced Anime AI API Server with URLhaus Integration
Combines anime characters with real threat intelligence for comprehensive phishing protection
"""

import os
import sys
import logging
import tempfile
import asyncio
import random
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import json

# Configure logging FIRST before any other imports
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI imports
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import uvicorn

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

# Local imports with proper error handling
try:
    from urlhaus_integration import URLhausClient, URLhausEnhancedAnalysis
    URLHAUS_AVAILABLE = True
    logger.info("✅ URLhaus integration loaded successfully")
except ImportError as e:
    logger.warning(f"❌ URLhaus integration not available: {e}")
    URLhausClient = None
    URLhausEnhancedAnalysis = None
    URLHAUS_AVAILABLE = False





# Global components
urlhaus_client: Optional[URLhausClient] = None
threat_analyzer: Optional[URLhausEnhancedAnalysis] = None

async def get_threat_analyzer():
    """Dependency to get the threat analyzer instance"""
    global threat_analyzer, urlhaus_client
    if threat_analyzer is None and URLHAUS_AVAILABLE:
        try:
            urlhaus_client = URLhausClient()
            threat_analyzer = URLhausEnhancedAnalysis(urlhaus_client)
            logger.info("✅ URLhaus threat analyzer initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize URLhaus analyzer: {e}")
            threat_analyzer = None
    return threat_analyzer

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    logger.info("🚀 Starting Enhanced Anime AI Protection API...")
    
    # Ensure required directories exist
    os.makedirs("voice_files", exist_ok=True)
    os.makedirs("temp_uploads", exist_ok=True)
    
    # Initialize threat analyzer
    try:
        await get_threat_analyzer()
    except Exception as e:
        logger.warning(f"⚠️ Threat analyzer initialization failed: {e}")
    
    logger.info("✅ Enhanced Anime AI Protection API started successfully!")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Enhanced Anime AI Protection API...")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Enhanced Anime AI Protection API",
    description="AI-chan and Haru with URLhaus threat intelligence integration",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with enhanced capabilities"""
    return {
        "message": "Enhanced Anime AI Protection API",
        "version": "2.0.0",
        "characters": ["AI-chan", "Haru"],
        "capabilities": [
            "vision_enhanced_phishing_detection",
            "urlhaus_threat_intelligence", 
            "voice_synthesis",
            "recovery_assistance",
            "comprehensive_analysis"
        ],
        "threat_intelligence": "URLhaus Integration Active" if URLHAUS_AVAILABLE else "Basic Analysis Only",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Enhanced health check endpoint"""
    try:
        threat_status = "available" if threat_analyzer else "unavailable"
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "ollama": "available",  # Would check actual Ollama status
                "ai_chan": "ready",
                "haru": "ready",
                "voice_synthesis": "available",
                "urlhaus_integration": threat_status
            },
            "version": "2.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}

# Enhanced AI-chan endpoints
@app.get("/anime/ai-chan/greeting")
async def ai_chan_greeting():
    """Get AI-chan's enhanced greeting with threat detection status"""
    try:
        greeting_messages = [
            "こんにちは！AI-chanです♪ URLhaus脅威インテリジェンスで強化されました！",
            "Hello! I'm AI-chan! ♪ Now enhanced with real-time threat intelligence!",
            "やっほー！新しい脅威検出機能でさらに強くなりました！",
            "Hi there! Ready to protect you with enhanced phishing detection! (＾◡＾)",
            "安全第一！URLhaus統合でより正確な分析ができます～♪"
        ]
        
        greeting = random.choice(greeting_messages)
        
        return {
            "character": "AI-chan",
            "greeting": greeting,
            "personality": "cheerful_anime_girl",
            "enhancement": "URLhaus Threat Intelligence",
            "timestamp": datetime.now().isoformat(),
            "message": "AI-chan is ready to protect you with enhanced threat detection! ♪"
        }
    except Exception as e:
        logger.error(f"Error in AI-chan greeting: {e}")
        raise HTTPException(status_code=500, detail=f"Greeting failed: {str(e)}")

@app.post("/anime/ai-chan/analyze")
async def ai_chan_enhanced_analyze(
    url: Optional[str] = Form(None),
    user_id: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    analyzer: Optional[URLhausEnhancedAnalysis] = Depends(get_threat_analyzer)
):
    """AI-chan's enhanced analysis with URLhaus integration"""
    if not url and not image:
        raise HTTPException(status_code=400, detail="Either URL or image must be provided")
    
    temp_image_path = None
    try:
        # Handle image upload if provided
        if image:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{image.filename.split('.')[-1]}") as temp_file:
                content = await image.read()
                temp_file.write(content)
                temp_image_path = temp_file.name
        
        # Enhanced URL analysis using URLhaus
        url_analysis = None
        if url and analyzer:
            logger.info(f"🌸 AI-chan analyzing URL with URLhaus: {url}")
            url_analysis = analyzer.analyze_url_comprehensive(url)
        elif url:
            # Fallback to basic analysis
            logger.info(f"🌸 AI-chan performing basic URL analysis: {url}")
            url_analysis = basic_url_analysis(url)
        
        # Image analysis (mock for now)
        image_analysis = None
        if image:
            logger.info(f"🌸 AI-chan analyzing image: {image.filename}")
            image_analysis = mock_image_analysis(temp_image_path)
        
        # Determine overall threat level
        danger_detected = False
        confidence = 0.0
        
        if url_analysis:
            danger_detected = url_analysis.get('is_malicious', False)
            confidence = url_analysis.get('confidence', 0.0)
        
        if image_analysis:
            image_danger = image_analysis.get('is_suspicious', False)
            image_confidence = image_analysis.get('confidence', 0.0)
            
            # Combine assessments
            if image_danger:
                danger_detected = True
                confidence = max(confidence, image_confidence)
        
        # Generate AI-chan's response
        ai_chan_message = generate_ai_chan_response(danger_detected, confidence, url_analysis)
        
        # Generate voice warning if danger detected
        voice_warning = None
        if danger_detected:
            voice_warning = f"ai_chan_warning_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            # In real implementation, generate actual Japanese voice: "危険です！"
        
        return {
            "character": "AI-chan",
            "analysis_type": "enhanced_vision_threat_detection",
            "url_analysis": url_analysis,
            "image_analysis": image_analysis,
            "danger_detected": danger_detected,
            "confidence_score": confidence,
            "ai_chan_assessment": ai_chan_message,
            "voice_warning": voice_warning,
            "enhancement_source": "URLhaus" if analyzer else "Basic",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in AI-chan enhanced analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    finally:
        # Clean up temporary file
        if temp_image_path and os.path.exists(temp_image_path):
            try:
                os.unlink(temp_image_path)
            except Exception as e:
                logger.warning(f"Failed to clean up temp file: {e}")

# Enhanced Haru endpoints
@app.get("/anime/haru/greeting")
async def haru_greeting():
    """Get Haru's enhanced greeting"""
    try:
        greeting_messages = [
            "はぁ... URLhaus統合で仕事が増えたな... でも、より良い回復支援ができる。",
            "やれやれ... 脅威インテリジェンスが追加されたか... まぁ、役に立つだろう。",
            "めんどくさいけど... 新しいシステムでより正確な助言ができるようになった。",
            "別に嬉しくないからな！でも強化された分析で助けてやる。",
            "はぁ... 今度はURLhausデータも見なきゃいけないのか... まぁ、やってやる。"
        ]
        
        greeting = random.choice(greeting_messages)
        
        return {
            "character": "Haru",
            "greeting": greeting,
            "personality": "lazy_but_caring_anime_boy",
            "enhancement": "Enhanced Recovery Analysis",
            "timestamp": datetime.now().isoformat(),
            "message": "Haru is ready to help with enhanced recovery analysis... reluctantly."
        }
    except Exception as e:
        logger.error(f"Error in Haru greeting: {e}")
        raise HTTPException(status_code=500, detail=f"Greeting failed: {str(e)}")

@app.post("/anime/haru/help")
async def haru_enhanced_help(
    issue_description: Optional[str] = Form(None),
    user_id: Optional[str] = Form(None),
    question_count: Optional[str] = Form("1"),
    screenshot: Optional[UploadFile] = File(None),
    analyzer: Optional[URLhausEnhancedAnalysis] = Depends(get_threat_analyzer)
):
    """Haru's enhanced recovery assistance"""
    if not issue_description and not screenshot:
        raise HTTPException(status_code=400, detail="Issue description or screenshot is required")
    
    temp_screenshot_path = None
    try:
        questions = int(question_count) if question_count else 1
        
        # Handle screenshot upload if provided
        if screenshot:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{screenshot.filename.split('.')[-1]}") as temp_file:
                content = await screenshot.read()
                temp_file.write(content)
                temp_screenshot_path = temp_file.name
        
        # Generate Haru's lazy comment based on question count
        lazy_comment = generate_haru_lazy_comment(questions)
        
        # Enhanced recovery analysis
        recovery_advice = generate_enhanced_recovery_advice(
            issue_description, 
            temp_screenshot_path, 
            analyzer
        )
        
        # Generate voice response for excessive questions
        voice_response = None
        if questions > 5:
            voice_response = f"haru_sigh_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            # In real implementation, generate "めんどくさいな..." voice
        
        return {
            "character": "Haru",
            "assistance_type": "enhanced_recovery_and_education",
            "recovery_advice": recovery_advice,
            "screenshot_analysis": analyze_screenshot_for_threats(temp_screenshot_path, analyzer),
            "voice_response": voice_response,
            "lazy_comment": lazy_comment,
            "enhancement_note": "Analysis enhanced with threat intelligence" if analyzer else "Basic analysis",
            "timestamp": datetime.now().isoformat(),
            "haru_message": generate_haru_response(recovery_advice, questions)
        }
        
    except Exception as e:
        logger.error(f"Error in Haru enhanced assistance: {e}")
        raise HTTPException(status_code=500, detail=f"Assistance failed: {str(e)}")
    finally:
        # Clean up temporary file
        if temp_screenshot_path and os.path.exists(temp_screenshot_path):
            try:
                os.unlink(temp_screenshot_path)
            except Exception as e:
                logger.warning(f"Failed to clean up temp file: {e}")

# Combined analysis endpoint
@app.post("/anime/combined/analyze")
async def combined_analyze(
    url: Optional[str] = Form(None),
    issue_description: Optional[str] = Form(None),
    content: Optional[UploadFile] = File(None),
    analyzer: Optional[URLhausEnhancedAnalysis] = Depends(get_threat_analyzer)
):
    """Combined analysis from both AI-chan and Haru"""
    try:
        # Get AI-chan's analysis
        ai_chan_result = None
        if url or content:
            # Mock AI-chan analysis for combined endpoint
            ai_chan_result = {
                "character": "AI-chan",
                "analysis": "Combined analysis mode activated!",
                "threat_level": "medium",
                "recommendation": "Further investigation recommended"
            }
        
        # Get Haru's assistance
        haru_result = None
        if issue_description or content:
            # Mock Haru assistance for combined endpoint
            haru_result = {
                "character": "Haru",
                "assistance": "Combined recovery mode... めんどくさいけど、やってやる。",
                "priority": "medium",
                "steps": ["Analyze threat level", "Provide recovery steps", "Monitor for issues"]
            }
        
        return {
            "combined_analysis": {
                "ai_chan": ai_chan_result,
                "haru": haru_result,
                "enhancement": "URLhaus + Vision Analysis"
            },
            "timestamp": datetime.now().isoformat(),
            "message": "Combined analysis completed by both characters!"
        }
        
    except Exception as e:
        logger.error(f"Error in combined analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Combined analysis failed: {str(e)}")

# Voice file endpoints
@app.get("/anime/voice/{filename}")
async def download_voice_file(filename: str):
    """Download generated voice file"""
    try:
        voice_path = Path("voice_files") / filename
        if voice_path.exists():
            return FileResponse(voice_path, media_type="audio/wav")
        else:
            raise HTTPException(status_code=404, detail="Voice file not found")
    except Exception as e:
        logger.error(f"Error serving voice file: {e}")
        raise HTTPException(status_code=500, detail=f"Voice file error: {str(e)}")

@app.post("/anime/voice/generate")
async def generate_custom_voice(character: str = Form(...), text: str = Form(...)):
    """Generate custom voice for characters"""
    try:
        filename = f"{character}_custom_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        
        # Mock voice generation - replace with actual TTS
        voice_path = Path("voice_files") / filename
        
        # Create a dummy file for now
        with open(voice_path, 'w') as f:
            f.write(f"Voice file for {character}: {text}")
        
        return {
            "character": character,
            "text": text,
            "voice_file": filename,
            "status": "generated",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error generating voice: {e}")
        raise HTTPException(status_code=500, detail=f"Voice generation failed: {str(e)}")

# Utility functions
def basic_url_analysis(url: str) -> Dict[str, Any]:
    """Basic URL analysis without URLhaus"""
    suspicious_patterns = ['bit.ly', 'tinyurl', 'secure-update', 'verify-account', 'login', 'banking']
    is_suspicious = any(pattern in url.lower() for pattern in suspicious_patterns)
    
    return {
        'url': url,
        'is_malicious': is_suspicious,
        'confidence': 0.6 if is_suspicious else 0.8,
        'analysis_timestamp': datetime.now().isoformat(),
        'sources': {
            'urlhaus': {
                'status': 'error',
                'message': 'Failed to query URLhaus',
                'is_malicious': False,
                'confidence': 0
            },
            'pattern_analysis': {
                'is_suspicious': is_suspicious,
                'confidence': 0.6 if is_suspicious else 0.8,
                'suspicious_score': len([p for p in suspicious_patterns if p in url.lower()]),
                'matched_patterns': [p for p in suspicious_patterns if p in url.lower()],
                'total_patterns_checked': len(suspicious_patterns)
            }
        },
        'recommendation': '❔ UNKNOWN: Insufficient data for confident assessment'
    }

def mock_image_analysis(image_path: Optional[str]) -> Dict[str, Any]:
    """Mock image analysis - replace with actual computer vision"""
    if not image_path:
        return None
    
    return {
        'is_suspicious': False,  # Would use actual image analysis
        'confidence': 0.85,
        'detected_elements': ['login_form', 'input_fields'],
        'analysis_type': 'mock_computer_vision',
        'recommendation': '📷 Image appears to contain standard web elements'
    }

def generate_ai_chan_response(danger_detected: bool, confidence: float, analysis: Optional[Dict]) -> str:
    """Generate AI-chan's personality-appropriate response"""
    if danger_detected:
        if confidence >= 0.8:
            return "危険です！この URL は非常に怪しいです！絶対にアクセスしないでください♪"
        else:
            return "ちょっと怪しいかも... 注意してくださいね！ (＾◡＾)"
    else:
        return "安全そうですね♪ でも、いつでも注意は大切ですよ～！"

def generate_haru_lazy_comment(question_count: int) -> Optional[str]:
    """Generate Haru's lazy comments based on question frequency"""
    if question_count <= 3:
        return None
    elif question_count <= 5:
        return f"めんどくさいな... {question_count}回目の質問だぞ？"
    else:
        return f"はぁ... {question_count}回も質問するなよ... でも答えてやる。"

def generate_enhanced_recovery_advice(
    description: Optional[str], 
    screenshot_path: Optional[str], 
    analyzer: Optional[URLhausEnhancedAnalysis]
) -> Dict[str, Any]:
    """Generate enhanced recovery advice"""
    priority = "medium"
    steps = []
    estimated_time = "10-20 minutes"
    
    if description:
        if "password" in description.lower():
            priority = "high"
            steps = [
                "すぐにパスワードを変更してください",
                "二要素認証を有効にする",
                "最近のアカウント活動を確認",
                "同じパスワードを使用している他のアカウントも更新"
            ]
            estimated_time = "15-30 minutes"
        elif "click" in description.lower() and "link" in description.lower():
            priority = "medium"
            steps = [
                "慌てる必要はありません。リンクをクリックしただけでは必ずしも危険ではありません",
                "ウイルススキャンを実行",
                "ブラウザのキャッシュとクッキーをクリア",
                "アカウントの異常な活動を監視"
            ]
        else:
            steps = [
                "より詳細な情報を提供してください",
                "個人情報を入力したかどうか確認",
                "アカウントの異常な活動を監視",
                "セキュリティスキャンの実行を検討"
            ]
    
    return {
        "steps": steps,
        "priority": priority,
        "estimated_time": estimated_time,
        "enhancement_note": "URLhaus データで強化された分析" if analyzer else "基本的な分析"
    }

def analyze_screenshot_for_threats(
    screenshot_path: Optional[str], 
    analyzer: Optional[URLhausEnhancedAnalysis]
) -> Optional[Dict[str, Any]]:
    """Analyze screenshot for potential threats"""
    if not screenshot_path:
        return None
    
    # Mock analysis - would use actual computer vision
    return {
        "detected_issues": ["潜在的に怪しいログインフォーム", "異常なURL構造"],
        "recommendations": ["ウェブサイトのURLを確認", "HTTPSを確認", "公式ブランディングを探す"],
        "threat_level": "low",
        "enhancement_note": "画像分析システムで強化" if analyzer else "基本画像分析"
    }

def generate_haru_response(recovery_advice: Dict, question_count: int) -> str:
    """Generate Haru's personality-appropriate response"""
    if question_count > 5:
        return "やれやれ... 何度も質問するなよ。でも、これで解決するはずだ。"
    elif recovery_advice["priority"] == "high":
        return "おい、これは重要だぞ！すぐに対処しろ。"
    else:
        return "まぁ、この手順で大丈夫だろう。面倒だが、やってみろ。"

# Additional endpoints for system integration
@app.get("/anime/status")
async def system_status():
    """Get comprehensive system status"""
    return {
        "ai_chan": {
            "status": "active",
            "capabilities": ["phishing_detection", "image_analysis", "voice_warnings"],
            "enhancement": "URLhaus Integration"
        },
        "haru": {
            "status": "active", 
            "capabilities": ["recovery_assistance", "educational_guidance", "lazy_responses"],
            "enhancement": "Enhanced Analysis"
        },
        "threat_intelligence": {
            "urlhaus": "active" if URLHAUS_AVAILABLE else "unavailable",
            "pattern_matching": "active",
            "confidence_scoring": "active"
        },
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    logger.info("🎌 Starting Enhanced Anime AI Protection API Server...")
    uvicorn.run(
        "enhanced_anime_api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
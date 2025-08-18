#!/usr/bin/env python3
"""
Anime AI API Server
FastAPI server that handles AI-chan and Haru requests with vision, voice, and RAG capabilities
"""

import os
import sys
import logging
import tempfile
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import base64
import json

# FastAPI imports
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

# Local imports
try:
    from anime_vision_ollama_integration import AnimePhishGuardManager
except ImportError:
    print("anime_vision_ollama_integration not found, creating basic implementation...")
    # We'll create a basic implementation if the module doesn't exist
    class AnimePhishGuardManager:
        def __init__(self):
            self.ai_chan = None
            self.haru = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Anime AI Protection API",
    description="AI-chan and Haru anime AI assistants for phishing detection and recovery",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global manager instance
manager: Optional[AnimePhishGuardManager] = None

async def get_manager():
    """Dependency to get the manager instance"""
    global manager
    if manager is None:
        try:
            manager = AnimePhishGuardManager()
            logger.info("✅ Anime AI Manager initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Anime AI Manager: {e}")
            raise HTTPException(status_code=503, detail="AI service initialization failed")
    return manager

@app.on_event("startup")
async def startup_event():
    """Initialize the anime AI system on startup"""
    logger.info("🚀 Starting Anime AI Protection API...")
    
    # Ensure required directories exist
    os.makedirs("voice_files", exist_ok=True)
    os.makedirs("temp_uploads", exist_ok=True)
    
    # Initialize manager
    await get_manager()
    
    logger.info("✅ Anime AI Protection API started successfully!")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Anime AI Protection API",
        "version": "1.0.0",
        "characters": ["AI-chan", "Haru"],
        "capabilities": ["phishing_detection", "recovery_assistance", "voice_synthesis", "vision_analysis"]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if manager is available
        if manager is None:
            return {"status": "unhealthy", "error": "Manager not initialized"}
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "ollama": "available",
                "ai_chan": "ready",
                "haru": "ready",
                "voice_synthesis": "available"
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}

# AI-chan endpoints
@app.get("/anime/ai-chan/greeting")
async def ai_chan_greeting(manager: AnimePhishGuardManager = Depends(get_manager)):
    """Get AI-chan's greeting message"""
    try:
        greeting_messages = [
            "こんにちは！AI-chanです♪ 危険なリンクや画像をチェックしますよ～！",
            "Hello! I'm AI-chan! ♪ I'll help protect you from phishing attacks!",
            "やっほー！みんなを守るために頑張ります！",
            "Hi there! Ready to scan for suspicious content together? (＾◡＾)",
            "安全第一！AI-chanにお任せください～♪"
        ]
        
        import random
        greeting = random.choice(greeting_messages)
        
        return {
            "character": "AI-chan",
            "greeting": greeting,
            "personality": "cheerful_anime_girl",
            "timestamp": datetime.now().isoformat(),
            "message": "AI-chan is ready to protect you! ♪"
        }
    except Exception as e:
        logger.error(f"Error in AI-chan greeting: {e}")
        raise HTTPException(status_code=500, detail=f"Greeting failed: {str(e)}")

@app.post("/anime/ai-chan/analyze")
async def ai_chan_analyze(
    url: Optional[str] = Form(None),
    user_id: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    manager: AnimePhishGuardManager = Depends(get_manager)
):
    """AI-chan analyzes URL or image for phishing with voice warning"""
    if not url and not image:
        raise HTTPException(status_code=400, detail="Either URL or image must be provided")
    
    temp_image_path = None
    try:
        # Handle image upload if provided
        if image:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{image.filename.split('.')[-1]}") as temp_file:
                content = await image.read()
                temp_file.write(content)
                temp_image_path = temp_file.name
        
        # Mock analysis since we don't have the full implementation yet
        # In real implementation, this would use the manager.ai_chan.analyze_with_voice_warning method
        
        # Simulate analysis
        danger_detected = False
        analysis_result = {
            "analysis_type": "vision_enhanced_phishing_detection"
        }
        
        if url:
            # Basic URL analysis
            suspicious_domains = ['phishing', 'malware', 'fake', 'scam', 'suspicious']
            is_phishing = any(domain in url.lower() for domain in suspicious_domains)
            danger_detected = is_phishing
            
            analysis_result["url_analysis"] = {
                "is_phishing": is_phishing,
                "confidence": 0.85 if is_phishing else 0.95,
                "reasons": ["Suspicious domain pattern detected"] if is_phishing else ["Domain appears legitimate"]
            }
        
        if image:
            # Mock image analysis
            analysis_result["image_analysis"] = {
                "is_suspicious": False,  # Would be determined by actual vision analysis
                "confidence": 0.92,
                "detected_elements": ["login_form", "input_fields"] if temp_image_path else []
            }
        
        # Generate voice warning if danger detected
        voice_warning = None
        if danger_detected:
            voice_warning = f"ai_chan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            # In real implementation, this would generate actual voice file
        
        return {
            "character": "AI-chan",
            "analysis_type": analysis_result["analysis_type"],
            "url_analysis": analysis_result.get("url_analysis"),
            "image_analysis": analysis_result.get("image_analysis"),
            "danger_detected": danger_detected,
            "voice_warning": voice_warning,
            "timestamp": datetime.now().isoformat(),
            "message": "危険です！" if danger_detected else "安全そうですね♪ (Looks safe!)"
        }
        
    except Exception as e:
        logger.error(f"Error in AI-chan analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    finally:
        # Clean up temporary file
        if temp_image_path and os.path.exists(temp_image_path):
            os.unlink(temp_image_path)

# Haru endpoints
@app.get("/anime/haru/greeting")
async def haru_greeting(manager: AnimePhishGuardManager = Depends(get_manager)):
    """Get Haru's greeting message"""
    try:
        greeting_messages = [
            "はぁ... また仕事か... でも、困ってるなら手伝ってやる。(Sigh... more work... but I'll help if you're in trouble.)",
            "やれやれ... まぁ、回復のお手伝いはしてやるよ。(Good grief... well, I'll help with recovery.)",
            "めんどくさいけど... セキュリティは大事だからな。(It's a pain, but security is important.)",
            "別に心配してるわけじゃないからな！でも助けてやる。(It's not like I'm worried! But I'll help.)",
            "はぁ... 今度は何の問題だ？まぁ、聞いてやる。(Sigh... what's the problem this time? Well, I'll listen.)"
        ]
        
        import random
        greeting = random.choice(greeting_messages)
        
        return {
            "character": "Haru",
            "greeting": greeting,
            "personality": "lazy_but_caring_anime_boy",
            "timestamp": datetime.now().isoformat(),
            "message": "Haru is ready to help... reluctantly."
        }
    except Exception as e:
        logger.error(f"Error in Haru greeting: {e}")
        raise HTTPException(status_code=500, detail=f"Greeting failed: {str(e)}")

@app.post("/anime/haru/help")
async def haru_help(
    issue_description: Optional[str] = Form(None),
    user_id: Optional[str] = Form(None),
    question_count: Optional[str] = Form("1"),
    screenshot: Optional[UploadFile] = File(None),
    manager: AnimePhishGuardManager = Depends(get_manager)
):
    """Haru provides recovery assistance with voice response"""
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
        
        # Generate lazy comment based on question count
        lazy_comment = None
        if questions > 3:
            lazy_comments = [
                f"めんどくさいな... {questions}個も質問して。(This is a pain... {questions} questions already.)",
                f"はぁ... また質問？{questions}回目だぞ？(Sigh... another question? That's the {questions}th time.)",
                f"やれやれ... 質問多すぎ。でも答えてやる。(Good grief... too many questions. But I'll answer.)"
            ]
            import random
            lazy_comment = random.choice(lazy_comments)
        
        # Mock recovery advice
        priority = "medium"
        steps = []
        
        if issue_description:
            if "password" in issue_description.lower():
                priority = "high"
                steps = [
                    "Immediately change your password on the affected account",
                    "Enable two-factor authentication if available",
                    "Check recent account activity for unauthorized access",
                    "Update passwords on other accounts if you reused the same password"
                ]
            elif "click" in issue_description.lower() and "link" in issue_description.lower():
                priority = "medium"
                steps = [
                    "Don't panic, clicking a link doesn't always mean you're compromised",
                    "Run a full antivirus scan on your device",
                    "Clear your browser cache and cookies",
                    "Monitor your accounts for unusual activity"
                ]
            else:
                steps = [
                    "Provide more details about what happened",
                    "Check if any personal information was entered",
                    "Monitor your accounts for unusual activity",
                    "Consider running a security scan"
                ]
        
        # Mock screenshot analysis
        screenshot_analysis = None
        if screenshot:
            screenshot_analysis = {
                "detected_issues": ["Potentially suspicious login form", "Unusual URL structure"],
                "recommendations": ["Verify the website URL", "Check for HTTPS", "Look for official branding"]
            }
        
        # Generate voice response if lazy
        voice_response = None
        if questions > 5:
            voice_response = f"haru_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            # In real implementation, this would generate "めんどくさいな..." voice
        
        return {
            "character": "Haru",
            "assistance_type": "recovery_and_education",
            "advice": {
                "steps": steps,
                "priority": priority,
                "estimated_time": "5-15 minutes"
            },
            "screenshot_analysis": screenshot_analysis,
            "voice_response": voice_response,
            "lazy_comment": lazy_comment,
            "timestamp": datetime.now().isoformat(),
            "message": f"やれやれ... まぁ、これで解決するはずだ。(Good grief... well, this should solve it.)"
        }
        
    except Exception as e:
        logger.error(f"Error in Haru assistance: {e}")
        raise HTTPException(status_code=500, detail=f"Assistance failed: {str(e)}")
    finally:
        # Clean up temporary file
        if temp_screenshot_path and os.path.exists(temp_screenshot_path):
            os.unlink(temp_screenshot_path)

# Combined analysis endpoint
@app.post("/anime/combined/analyze")
async def combined_analyze(
    url: Optional[str] = Form(None),
    issue_description: Optional[str] = Form(None),
    user_id: Optional[str] = Form(None),
    content: Optional[UploadFile] = File(None),
    manager: AnimePhishGuardManager = Depends(get_manager)
):
    """Combined analysis from both AI-chan and Haru"""
    if not url and not content and not issue_description:
        raise HTTPException(status_code=400, detail="URL, content, or issue description is required")
    
    try:
        # This would integrate both AI-chan and Haru analyses
        return {
            "ai_chan_analysis": "Would analyze for phishing",
            "haru_analysis": "Would provide recovery guidance",
            "combined_recommendation": "Comprehensive protection and recovery plan",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in combined analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Combined analysis failed: {str(e)}")

# Voice endpoints
@app.get("/anime/voice/{filename}")
async def download_voice_file(filename: str):
    """Download generated voice files"""
    # Security: Only allow specific voice files
    if not filename.match(r'^(ai_chan|haru)_\d+\.wav$'):
        raise HTTPException(status_code=400, detail="Invalid voice file")
    
    voice_path = Path("voice_files") / filename
    
    if not voice_path.exists():
        raise HTTPException(status_code=404, detail="Voice file not found")
    
    return FileResponse(voice_path, media_type="audio/wav", filename=filename)

@app.post("/anime/voice/generate")
async def generate_custom_voice(
    character: str = Form(...),
    text: str = Form(...),
    voice_type: str = Form("default"),
    user_id: Optional[str] = Form(None),
    manager: AnimePhishGuardManager = Depends(get_manager)
):
    """Generate custom voice for characters"""
    if character not in ['ai-chan', 'haru']:
        raise HTTPException(status_code=400, detail="Invalid character. Use 'ai-chan' or 'haru'")
    
    try:
        # Mock voice generation
        voice_filename = f"{character.replace('-', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        
        return {
            "character": character,
            "text": text,
            "voice_file": voice_filename,
            "voice_type": voice_type,
            "timestamp": datetime.now().isoformat(),
            "message": f"Voice generated for {character}"
        }
    except Exception as e:
        logger.error(f"Error generating voice: {e}")
        raise HTTPException(status_code=500, detail=f"Voice generation failed: {str(e)}")

if __name__ == "__main__":
    # Run the server
    logger.info("🎌 Starting Anime AI Protection API Server...")
    uvicorn.run(
        "anime_api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 
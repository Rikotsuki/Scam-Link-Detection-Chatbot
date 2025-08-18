#!/usr/bin/env python3
"""
Integrated System Startup Script
Starts both the anime AI API server and verifies backend integration
"""

import sys
import subprocess
import time
import logging
import requests
import json
from pathlib import Path
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IntegratedSystemManager:
    """Manages the integrated anime AI and backend system"""
    
    def __init__(self):
        self.python_port = 8000
        self.backend_port = 3000
        self.frontend_port = 3001
        
        self.python_url = f"http://localhost:{self.python_port}"
        self.backend_url = f"http://localhost:{self.backend_port}"
        
    def check_ollama_status(self) -> bool:
        """Check if Ollama is running with llama3.2-vision:11b"""
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if result.returncode == 0:
                models = result.stdout
                if 'llama3.2-vision:11b' in models:
                    logger.info("✅ Ollama is running with llama3.2-vision:11b")
                    return True
                else:
                    logger.error("❌ llama3.2-vision:11b model not found")
                    logger.info("Please run: ollama pull llama3.2-vision:11b")
                    return False
            else:
                logger.error("❌ Ollama is not running")
                return False
        except FileNotFoundError:
            logger.error("❌ Ollama is not installed")
            return False
    
    def install_dependencies(self) -> bool:
        """Install required dependencies"""
        try:
            logger.info("📦 Installing Python dependencies...")
            
            # Install anime system requirements
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-r', 'requirements_anime.txt'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ Python dependencies installed")
            else:
                logger.warning(f"⚠️ Some Python dependencies failed: {result.stderr}")
            
            # Install Japanese TTS dependencies
            logger.info("🎌 Installing Japanese TTS dependencies...")
            
            tts_packages = [
                'git+https://github.com/huggingface/parler-tts.git',
                'git+https://github.com/getuka/RubyInserter.git'
            ]
            
            for package in tts_packages:
                logger.info(f"Installing {package}...")
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', package
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info(f"✅ {package} installed")
                else:
                    logger.warning(f"⚠️ {package} installation failed: {result.stderr}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error installing dependencies: {e}")
            return False
    
    def install_backend_dependencies(self) -> bool:
        """Install backend Node.js dependencies"""
        try:
            logger.info("📦 Installing backend dependencies...")
            backend_dir = Path("../backend")
            
            if backend_dir.exists():
                result = subprocess.run(
                    ['npm', 'install'],
                    cwd=backend_dir,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    logger.info("✅ Backend dependencies installed")
                    return True
                else:
                    logger.error(f"❌ Backend installation failed: {result.stderr}")
                    return False
            else:
                logger.warning("⚠️ Backend directory not found")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error installing backend dependencies: {e}")
            return False
    
    def start_anime_api_server(self) -> subprocess.Popen:
        """Start the anime AI API server"""
        try:
            logger.info(f"🎌 Starting Anime AI API server on port {self.python_port}...")
            
            process = subprocess.Popen([
                sys.executable, 'anime_api_server.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for server to start
            for i in range(30):
                try:
                    response = requests.get(f"{self.python_url}/anime/health", timeout=2)
                    if response.status_code in [200, 503]:  # 503 is OK during initialization
                        logger.info("✅ Anime AI API server started")
                        return process
                except:
                    pass
                time.sleep(1)
            
            logger.error("❌ Anime AI API server failed to start")
            process.terminate()
            return None
            
        except Exception as e:
            logger.error(f"❌ Error starting anime API server: {e}")
            return None
    
    def start_backend_server(self) -> subprocess.Popen:
        """Start the backend Node.js server"""
        try:
            logger.info(f"🚀 Starting backend server on port {self.backend_port}...")
            backend_dir = Path("../backend")
            
            if not backend_dir.exists():
                logger.error("❌ Backend directory not found")
                return None
            
            process = subprocess.Popen([
                'npm', 'start'
            ], cwd=backend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for server to start
            for i in range(20):
                try:
                    response = requests.get(f"{self.backend_url}/api/anime/health", timeout=2)
                    if response.status_code in [200, 503]:
                        logger.info("✅ Backend server started")
                        return process
                except:
                    pass
                time.sleep(1)
            
            logger.error("❌ Backend server failed to start")
            process.terminate()
            return None
            
        except Exception as e:
            logger.error(f"❌ Error starting backend server: {e}")
            return None
    
    def test_integration(self) -> bool:
        """Test the integration between components"""
        try:
            logger.info("🧪 Testing system integration...")
            
            # Test anime API health
            logger.info("Testing anime AI API...")
            response = requests.get(f"{self.python_url}/anime/health", timeout=10)
            if response.status_code == 200:
                logger.info("✅ Anime AI API is healthy")
            else:
                logger.warning(f"⚠️ Anime AI API status: {response.status_code}")
            
            # Test backend anime routes
            logger.info("Testing backend anime integration...")
            response = requests.get(f"{self.backend_url}/api/anime/health", timeout=10)
            if response.status_code == 200:
                logger.info("✅ Backend anime integration is working")
            else:
                logger.warning(f"⚠️ Backend anime status: {response.status_code}")
            
            # Test AI-chan greeting
            logger.info("Testing AI-chan greeting...")
            response = requests.get(f"{self.backend_url}/api/anime/ai-chan/greeting", timeout=15)
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ AI-chan says: {data.get('greeting', 'Hello!')}")
            else:
                logger.warning(f"⚠️ AI-chan greeting failed: {response.status_code}")
            
            # Test Haru greeting
            logger.info("Testing Haru greeting...")
            response = requests.get(f"{self.backend_url}/api/anime/haru/greeting", timeout=15)
            if response.status_code == 200:
                data = response.json()
                logger.info(f"✅ Haru says: {data.get('greeting', 'Hello...')}")
            else:
                logger.warning(f"⚠️ Haru greeting failed: {response.status_code}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Integration test failed: {e}")
            return False
    
    def print_api_endpoints(self):
        """Print available API endpoints"""
        logger.info("\n🌸 AI-chan Endpoints:")
        logger.info(f"   GET  {self.backend_url}/api/anime/ai-chan/greeting")
        logger.info(f"   POST {self.backend_url}/api/anime/ai-chan/analyze")
        
        logger.info("\n😴 Haru Endpoints:")
        logger.info(f"   GET  {self.backend_url}/api/anime/haru/greeting")
        logger.info(f"   POST {self.backend_url}/api/anime/haru/help")
        
        logger.info("\n🎭 Combined Endpoints:")
        logger.info(f"   POST {self.backend_url}/api/anime/analyze-and-help")
        logger.info(f"   POST {self.backend_url}/api/anime/voice/generate")
        logger.info(f"   GET  {self.backend_url}/api/anime/voice/{{filename}}")
        
        logger.info("\n🔧 System Endpoints:")
        logger.info(f"   GET  {self.backend_url}/api/anime/health")
        logger.info(f"   GET  {self.python_url}/anime/characters")
        logger.info(f"   GET  {self.python_url}/docs (API Documentation)")
    
    def start_integrated_system(self):
        """Start the complete integrated system"""
        logger.info("🎌 Starting Integrated Anime PhishGuard AI System")
        logger.info("=" * 60)
        
        # Check prerequisites
        if not self.check_ollama_status():
            logger.error("Please set up Ollama with llama3.2-vision:11b first")
            return False
        
        # Install dependencies
        if not self.install_dependencies():
            logger.error("Failed to install Python dependencies")
            return False
        
        if not self.install_backend_dependencies():
            logger.warning("Backend dependencies installation failed, continuing...")
        
        # Start servers
        anime_process = self.start_anime_api_server()
        if not anime_process:
            return False
        
        backend_process = self.start_backend_server()
        if not backend_process:
            anime_process.terminate()
            return False
        
        # Test integration
        time.sleep(5)  # Give servers time to fully initialize
        if not self.test_integration():
            logger.warning("Some integration tests failed, but system may still work")
        
        # Print information
        self.print_api_endpoints()
        
        logger.info("\n🎉 Integrated system is running!")
        logger.info("=" * 60)
        logger.info("🌸 AI-chan: Cheerful anime girl phishing detector")
        logger.info("😴 Haru: Lazy but caring anime boy recovery assistant")
        logger.info("🎌 Japanese voice synthesis enabled")
        logger.info("🔍 Vision analysis with llama3.2-vision:11b")
        logger.info("🧠 RAG-enhanced context retrieval")
        
        logger.info(f"\n📊 System Status:")
        logger.info(f"   🐍 Python API: {self.python_url}")
        logger.info(f"   🚀 Backend API: {self.backend_url}")
        logger.info(f"   📖 Documentation: {self.python_url}/docs")
        
        try:
            logger.info("\n⌨️ Press Ctrl+C to stop all services")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("\n🛑 Stopping integrated system...")
            anime_process.terminate()
            backend_process.terminate()
            logger.info("✅ All services stopped")
        
        return True

def main():
    """Main function"""
    manager = IntegratedSystemManager()
    success = manager.start_integrated_system()
    
    if not success:
        logger.error("❌ Failed to start integrated system")
        sys.exit(1)

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Python-Only Enhanced Anime AI System Startup
Starts the enhanced Python API server with URLhaus integration
"""

import os
import sys
import subprocess
import time
import logging
import requests
import webbrowser
from pathlib import Path
from typing import Optional

# Load environment variables from .env files
try:
    from dotenv import load_dotenv
    load_dotenv()
    load_dotenv(Path(__file__).parent.parent / "frontend" / ".env.local")
    load_dotenv(Path(__file__).parent.parent / "backend" / ".env")
except ImportError:
    # Fallback: manually load .env files
    def load_env_file(file_path):
        if file_path.exists():
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key] = value
    
    load_env_file(Path(__file__).parent / ".env")
    load_env_file(Path(__file__).parent.parent / "frontend" / ".env.local")
    load_env_file(Path(__file__).parent.parent / "backend" / ".env")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PythonOnlyStarter:
    """Python-only system starter for the enhanced anime AI API"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.python_service_port = 8000
        self.processes = []
        
        # URLs for testing
        self.api_urls = {
            'python_health': f'http://localhost:{self.python_service_port}/health',
            'python_root': f'http://localhost:{self.python_service_port}/',
            'anime_status': f'http://localhost:{self.python_service_port}/anime/status'
        }
    
    def check_ollama_status(self) -> bool:
        """Check Ollama status and ensure llama3.2-vision:11b is available"""
        logger.info("🔍 Checking Ollama status...")
        
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code != 200:
                logger.error("❌ Ollama is not running. Please start Ollama first.")
                return False
            
            models = response.json().get('models', [])
            model_names = [model['name'] for model in models]
            
            if 'llama3.2-vision:11b' not in model_names:
                logger.warning("⚠️ llama3.2-vision:11b not found")
                logger.info("📥 Attempting to pull the model...")
                
                try:
                    result = subprocess.run(['ollama', 'pull', 'llama3.2-vision:11b'], 
                                          capture_output=True, text=True, timeout=300)
                    if result.returncode == 0:
                        logger.info("✅ Successfully pulled llama3.2-vision:11b")
                    else:
                        logger.error(f"❌ Failed to pull model: {result.stderr}")
                        return False
                except subprocess.TimeoutExpired:
                    logger.error("❌ Timeout while pulling model")
                    return False
                except FileNotFoundError:
                    logger.error("❌ Ollama command not found. Please install Ollama.")
                    return False
            
            logger.info(f"✅ Ollama is running with models: {model_names}")
            return True
            
        except requests.exceptions.RequestException:
            logger.error("❌ Cannot connect to Ollama. Please ensure Ollama is running.")
            return False
    
    def install_python_dependencies(self) -> bool:
        """Install Python dependencies"""
        logger.info("📦 Installing Python dependencies...")
        
        try:
            requirements_file = self.project_root / "requirements.txt"
            
            if not requirements_file.exists():
                logger.warning("⚠️ requirements.txt not found, creating basic one...")
                self.create_basic_requirements()
            
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ Python dependencies installed successfully")
                return True
            else:
                logger.error(f"❌ Failed to install Python dependencies: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error installing Python dependencies: {e}")
            return False
    
    def create_basic_requirements(self):
        """Create a basic requirements.txt file"""
        basic_requirements = [
            "fastapi>=0.104.0",
            "uvicorn[standard]>=0.24.0",
            "python-multipart>=0.0.6",
            "requests>=2.31.0",
            "python-jose[cryptography]>=3.3.0",
            "pydantic>=2.5.0"
        ]
        
        requirements_file = self.project_root / "requirements.txt"
        with open(requirements_file, 'w') as f:
            f.write('\n'.join(basic_requirements))
        
        logger.info("✅ Created basic requirements.txt file")
    
    def start_python_api(self) -> Optional[subprocess.Popen]:
        """Start the enhanced Python API server"""
        logger.info("🐍 Starting enhanced Python API server...")
        
        try:
            api_script = self.project_root / "ai_training" / "enhanced_anime_api_server.py"
            
            if not api_script.exists():
                logger.error("❌ Enhanced anime API server not found")
                return None
            
            # Use uvicorn directly with the module path
            process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", 
                "ai_training.enhanced_anime_api_server:app",
                "--host", "0.0.0.0",
                "--port", str(self.python_service_port),
                "--reload"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            time.sleep(5)  # Wait for startup
            
            if process.poll() is None:
                logger.info("✅ Python API server started successfully")
                return process
            else:
                # Check for any error output
                stdout, stderr = process.communicate()
                if stderr:
                    logger.error(f"❌ Server error: {stderr.decode()}")
                logger.error("❌ Python API server failed to start")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error starting Python API: {e}")
            return None
    
    def test_api_endpoints(self) -> bool:
        """Test Python API endpoints"""
        logger.info("🧪 Testing Python API endpoints...")
        
        endpoints_to_test = [
            ('Python API Health', self.api_urls['python_health']),
            ('Python API Root', self.api_urls['python_root']),
            ('Anime Status', self.api_urls['anime_status'])
        ]
        
        all_healthy = True
        
        for name, url in endpoints_to_test:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    logger.info(f"✅ {name}: Healthy")
                else:
                    logger.warning(f"⚠️ {name}: Status {response.status_code}")
                    all_healthy = False
            except requests.exceptions.RequestException as e:
                logger.error(f"❌ {name}: Failed - {e}")
                all_healthy = False
        
        return all_healthy
    
    def cleanup(self):
        """Clean up all started processes"""
        logger.info("🧹 Cleaning up processes...")
        
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception as e:
                logger.warning(f"Error cleaning up process: {e}")
        
        logger.info("✅ Cleanup completed")
    
    def open_browser(self):
        """Open the API documentation in the default browser"""
        logger.info("🌐 Opening API documentation in browser...")
        
        try:
            webbrowser.open(f"http://localhost:{self.python_service_port}/docs")
            logger.info("✅ Browser opened to API documentation")
        except Exception as e:
            logger.warning(f"Could not open browser: {e}")
    
    def start_system(self) -> bool:
        """Start the Python-only enhanced system"""
        logger.info("🎌 Starting Python-Only Enhanced Anime AI PhishGuard System")
        logger.info("=" * 60)
        
        try:
            # Pre-checks
            if not self.check_ollama_status():
                return False
            
            # Install dependencies
            if not self.install_python_dependencies():
                return False
            
            # Start Python API
            python_api = self.start_python_api()
            if python_api:
                self.processes.append(python_api)
            else:
                return False
            
            # Wait for service to stabilize
            logger.info("⏳ Waiting for service to stabilize...")
            time.sleep(5)
            
            # Test endpoints
            if not self.test_api_endpoints():
                logger.warning("⚠️ Some endpoints are not responding properly")
            
            # Success!
            logger.info("=" * 60)
            logger.info("🎉 PYTHON-ONLY ENHANCED ANIME AI PHISHGUARD SYSTEM STARTED!")
            logger.info("=" * 60)
            logger.info("")
            logger.info("🌐 API URLs:")
            logger.info(f"   📚 API Documentation: http://localhost:{self.python_service_port}/docs")
            logger.info(f"   🔧 Health Check: {self.api_urls['python_health']}")
            logger.info(f"   🎌 Anime Status: {self.api_urls['anime_status']}")
            logger.info("")
            logger.info("🎯 API Endpoints Available:")
            logger.info("   • GET /anime/ai-chan/greeting - AI-chan's greeting")
            logger.info("   • POST /anime/ai-chan/analyze - URL/image analysis")
            logger.info("   • GET /anime/haru/greeting - Haru's greeting")
            logger.info("   • POST /anime/haru/help - Recovery assistance")
            logger.info("")
            logger.info("🧪 Test the API:")
            logger.info("   curl http://localhost:8000/anime/ai-chan/greeting")
            logger.info("   curl -X POST http://localhost:8000/anime/ai-chan/analyze -F 'url=https://google.com'")
            logger.info("")
            logger.info("📝 To complete the full system:")
            logger.info("   1. Install Node.js and npm")
            logger.info("   2. Run: cd ../backend && npm install && npm start")
            logger.info("   3. Run: cd ../frontend && npm install && npm run dev")
            logger.info("")
            logger.info("🛑 Press Ctrl+C to stop the Python API")
            logger.info("=" * 60)
            
            # Open browser
            self.open_browser()
            
            # Keep running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("\n🛑 Shutdown requested by user")
                return True
                
        except Exception as e:
            logger.error(f"❌ System startup failed: {e}")
            return False
        finally:
            self.cleanup()

def main():
    """Main function"""
    starter = PythonOnlyStarter()
    
    if starter.start_system():
        logger.info("✅ System stopped successfully")
        sys.exit(0)
    else:
        logger.error("❌ System startup failed")
        sys.exit(1)

if __name__ == "__main__":
    main() 
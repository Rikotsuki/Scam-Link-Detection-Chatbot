#!/usr/bin/env python3
"""
Integrated Anime AI System Startup Script
Starts and coordinates the complete PhishGuard system with anime characters
"""

import os
import sys
import subprocess
import time
import logging
import requests
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import threading

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SystemStarter:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.python_service_port = 8000
        self.backend_port = 3000
        self.frontend_port = 3001
        self.processes = []
        
    def check_ollama_status(self):
        """Check if Ollama is running and has the required model"""
        logger.info("🔍 Checking Ollama status...")
        try:
            # Check if Ollama service is running
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [model['name'] for model in models]
                
                # Check for vision model
                vision_models = [name for name in model_names if 'llava' in name.lower() or 'vision' in name.lower()]
                
                if vision_models:
                    logger.info(f"✅ Ollama is running with vision models: {vision_models}")
                    return True
                else:
                    logger.warning("⚠️ Ollama is running but no vision models found")
                    logger.info("💡 Pulling llava model...")
                    try:
                        subprocess.run(['ollama', 'pull', 'llava'], check=True, timeout=300)
                        logger.info("✅ llava model pulled successfully")
                        return True
                    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                        logger.error(f"❌ Failed to pull llava model: {e}")
                        return False
            else:
                logger.error(f"❌ Ollama service responded with status {response.status_code}")
                return False
                
        except requests.exceptions.RequestException:
            logger.error("❌ Ollama service is not running")
            logger.info("💡 Please start Ollama service: ollama serve")
            return False
    
    def install_python_dependencies(self):
        """Install Python dependencies for the AI service"""
        logger.info("📦 Installing Python dependencies...")
        
        requirements = [
            "fastapi",
            "uvicorn[standard]", 
            "python-multipart",
            "requests",
            "pillow",
            "numpy",
            "opencv-python",
            "websockets"
        ]
        
        try:
            for package in requirements:
                logger.info(f"Installing {package}...")
                subprocess.run([sys.executable, "-m", "pip", "install", package], 
                             check=True, capture_output=True)
            
            logger.info("✅ Python dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install Python dependencies: {e}")
            return False
    
    def install_backend_dependencies(self):
        """Install Node.js backend dependencies"""
        logger.info("📦 Installing backend dependencies...")
        backend_dir = self.project_root.parent / "backend"
        
        if not backend_dir.exists():
            logger.error(f"❌ Backend directory not found: {backend_dir}")
            return False
        
        try:
            subprocess.run(["npm", "install"], cwd=backend_dir, check=True, capture_output=True)
            logger.info("✅ Backend dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install backend dependencies: {e}")
            return False
    
    def install_frontend_dependencies(self):
        """Install Next.js frontend dependencies"""
        logger.info("📦 Installing frontend dependencies...")
        frontend_dir = self.project_root.parent / "frontend"
        
        if not frontend_dir.exists():
            logger.error(f"❌ Frontend directory not found: {frontend_dir}")
            return False
        
        try:
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True, capture_output=True)
            logger.info("✅ Frontend dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install frontend dependencies: {e}")
            return False
    
    def start_python_api(self):
        """Start the Python FastAPI server"""
        logger.info("🐍 Starting Python AI API server...")
        
        api_file = self.project_root / "ai_training" / "anime_api_server.py"
        if not api_file.exists():
            logger.error(f"❌ Python API server file not found: {api_file}")
            return None
        
        try:
            # Change to the ai_training directory to ensure proper imports
            process = subprocess.Popen(
                [sys.executable, "anime_api_server.py"],
                cwd=api_file.parent,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait a moment for the server to start
            time.sleep(3)
            
            # Check if the process is still running
            if process.poll() is None:
                logger.info(f"✅ Python AI API server started (PID: {process.pid})")
                return process
            else:
                stdout, stderr = process.communicate()
                logger.error(f"❌ Python API server failed to start: {stderr.decode()}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Failed to start Python API server: {e}")
            return None
    
    def start_backend_server(self):
        """Start the Node.js backend server"""
        logger.info("🚀 Starting Node.js backend server...")
        backend_dir = self.project_root.parent / "backend"
        
        if not backend_dir.exists():
            logger.error(f"❌ Backend directory not found: {backend_dir}")
            return None
        
        try:
            # Check if server.js exists
            server_file = backend_dir / "server.js"
            app_file = backend_dir / "app.js"
            
            server_command = None
            if server_file.exists():
                server_command = ["node", "server.js"]
            elif app_file.exists():
                server_command = ["node", "app.js"]
            else:
                logger.error("❌ No server file (server.js or app.js) found in backend")
                return None
            
            process = subprocess.Popen(
                server_command,
                cwd=backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, 'PORT': str(self.backend_port)}
            )
            
            # Wait for the server to start
            time.sleep(3)
            
            if process.poll() is None:
                logger.info(f"✅ Backend server started (PID: {process.pid})")
                return process
            else:
                stdout, stderr = process.communicate()
                logger.error(f"❌ Backend server failed to start: {stderr.decode()}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Failed to start backend server: {e}")
            return None
    
    def start_frontend_dev(self):
        """Start the Next.js frontend development server"""
        logger.info("🎨 Starting Next.js frontend server...")
        frontend_dir = self.project_root.parent / "frontend"
        
        if not frontend_dir.exists():
            logger.error(f"❌ Frontend directory not found: {frontend_dir}")
            return None
        
        try:
            process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, 'PORT': str(self.frontend_port)}
            )
            
            # Wait for the server to start
            time.sleep(5)
            
            if process.poll() is None:
                logger.info(f"✅ Frontend server started (PID: {process.pid})")
                return process
            else:
                stdout, stderr = process.communicate()
                logger.error(f"❌ Frontend server failed to start: {stderr.decode()}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Failed to start frontend server: {e}")
            return None
    
    def test_api_endpoints(self):
        """Test the API endpoints"""
        logger.info("🧪 Testing API endpoints...")
        
        tests = [
            {
                "name": "Python API Health",
                "url": f"http://localhost:{self.python_service_port}/health",
                "expected_status": 200
            },
            {
                "name": "AI-chan Greeting",
                "url": f"http://localhost:{self.python_service_port}/anime/ai-chan/greeting",
                "expected_status": 200
            },
            {
                "name": "Haru Greeting", 
                "url": f"http://localhost:{self.python_service_port}/anime/haru/greeting",
                "expected_status": 200
            },
            {
                "name": "Backend Health",
                "url": f"http://localhost:{self.backend_port}",
                "expected_status": 200
            }
        ]
        
        all_passed = True
        for test in tests:
            try:
                response = requests.get(test["url"], timeout=10)
                if response.status_code == test["expected_status"]:
                    logger.info(f"✅ {test['name']}: PASSED")
                else:
                    logger.error(f"❌ {test['name']}: FAILED (status: {response.status_code})")
                    all_passed = False
            except requests.exceptions.RequestException as e:
                logger.error(f"❌ {test['name']}: FAILED ({e})")
                all_passed = False
        
        return all_passed
    
    def cleanup(self):
        """Clean up processes"""
        logger.info("🧹 Cleaning up processes...")
        for process in self.processes:
            if process and process.poll() is None:
                process.terminate()
                process.wait()
        logger.info("✅ Cleanup completed")
    
    def start_system(self):
        """Start the complete integrated system"""
        logger.info("🎌 Starting Anime AI PhishGuard Integrated System")
        logger.info("=" * 60)
        
        try:
            # Step 1: Check prerequisites
            if not self.check_ollama_status():
                logger.error("❌ Ollama not available. Please install and start Ollama first.")
                return False
            
            # Step 2: Install dependencies
            if not self.install_python_dependencies():
                return False
            
            if not self.install_backend_dependencies():
                return False
            
            # Step 3: Start services
            python_api = self.start_python_api()
            if python_api:
                self.processes.append(python_api)
            else:
                logger.error("❌ Failed to start Python API. Cannot continue.")
                return False
            
            backend_server = self.start_backend_server()
            if backend_server:
                self.processes.append(backend_server)
            else:
                logger.error("❌ Failed to start backend server. Cannot continue.")
                return False
            
            # Step 4: Test endpoints
            logger.info("⏳ Waiting for services to stabilize...")
            time.sleep(5)
            
            if not self.test_api_endpoints():
                logger.error("❌ API tests failed. Check service logs.")
                return False
            
            # Step 5: Display success information
            logger.info("=" * 60)
            logger.info("🎉 ANIME AI PHISHGUARD SYSTEM STARTED SUCCESSFULLY!")
            logger.info("=" * 60)
            logger.info(f"🐍 Python AI API: http://localhost:{self.python_service_port}")
            logger.info(f"🚀 Backend API: http://localhost:{self.backend_port}")
            logger.info(f"🎨 Frontend (manual): http://localhost:{self.frontend_port}")
            logger.info("")
            logger.info("📋 Available Characters:")
            logger.info("  🌸 AI-chan - Cheerful phishing detector")
            logger.info("  🌙 Haru - Lazy but caring recovery assistant")
            logger.info("")
            logger.info("🔗 Test URLs:")
            logger.info(f"  • Health Check: http://localhost:{self.python_service_port}/health")
            logger.info(f"  • AI-chan: http://localhost:{self.python_service_port}/anime/ai-chan/greeting")
            logger.info(f"  • Haru: http://localhost:{self.python_service_port}/anime/haru/greeting")
            logger.info("")
            logger.info("Press Ctrl+C to stop all services")
            
            # Keep the system running
            try:
                while True:
                    time.sleep(1)
                    # Check if processes are still running
                    for process in self.processes:
                        if process.poll() is not None:
                            logger.warning("⚠️ A service process has stopped")
                            
            except KeyboardInterrupt:
                logger.info("\n🛑 Stopping system...")
                return True
                
        except Exception as e:
            logger.error(f"❌ System startup failed: {e}")
            return False
        finally:
            self.cleanup()

def main():
    """Main function"""
    starter = SystemStarter()
    
    try:
        success = starter.start_system()
        if success:
            logger.info("✅ System shutdown completed successfully")
        else:
            logger.error("❌ System startup failed")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("\n🛑 System interrupted by user")
        starter.cleanup()

if __name__ == "__main__":
    main() 
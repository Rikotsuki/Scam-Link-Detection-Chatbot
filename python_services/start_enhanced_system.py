#!/usr/bin/env python3
"""
Enhanced Anime AI PhishGuard System Startup Script
Starts the complete integrated system with authentication and URLhaus integration
"""

import os
import sys
import subprocess
import time
import logging
import requests
import webbrowser
from pathlib import Path
from typing import Optional, List

# Load environment variables from .env files
try:
    from dotenv import load_dotenv
    # Load .env files from all relevant directories
    load_dotenv()  # Current directory
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
    
    # Load environment files
    load_env_file(Path(__file__).parent / ".env")
    load_env_file(Path(__file__).parent.parent / "frontend" / ".env.local")
    load_env_file(Path(__file__).parent.parent / "backend" / ".env")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EnhancedSystemStarter:
    """Enhanced system starter with full authentication and threat intelligence"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.python_service_port = 8000
        self.backend_port = 3001
        self.frontend_port = 3000
        self.processes = []
        
        # URLs for testing
        self.api_urls = {
            'python_health': f'http://localhost:{self.python_service_port}/health',
            'backend_health': f'http://localhost:{self.backend_port}/api/health',
            'frontend': f'http://localhost:{self.frontend_port}',
            'anime_dashboard': f'http://localhost:{self.frontend_port}/anime',
            'login': f'http://localhost:{self.frontend_port}/login'
        }
    
    def check_ollama_status(self) -> bool:
        """Check Ollama status and ensure llama3.2-vision:11b is available"""
        logger.info("🔍 Checking Ollama status...")
        
        try:
            # Check if Ollama is running
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code != 200:
                logger.error("❌ Ollama is not running. Please start Ollama first.")
                return False
            
            # Check for required models
            models = response.json().get('models', [])
            model_names = [model['name'] for model in models]
            
            required_models = ['llama3.2-vision:11b']
            missing_models = [model for model in required_models if model not in model_names]
            
            if missing_models:
                logger.warning(f"⚠️ Missing models: {missing_models}")
                logger.info("📥 Attempting to pull missing models...")
                
                for model in missing_models:
                    logger.info(f"Pulling {model}...")
                    try:
                        result = subprocess.run(['ollama', 'pull', model], 
                                              capture_output=True, text=True, timeout=300)
                        if result.returncode == 0:
                            logger.info(f"✅ Successfully pulled {model}")
                        else:
                            logger.error(f"❌ Failed to pull {model}: {result.stderr}")
                            return False
                    except subprocess.TimeoutExpired:
                        logger.error(f"❌ Timeout while pulling {model}")
                        return False
                    except FileNotFoundError:
                        logger.error("❌ Ollama command not found. Please install Ollama.")
                        return False
            
            logger.info(f"✅ Ollama is running with models: {model_names}")
            return True
            
        except requests.exceptions.RequestException:
            logger.error("❌ Cannot connect to Ollama. Please ensure Ollama is running.")
            return False
    
    def check_environment_variables(self) -> bool:
        """Check that all required environment variables are set"""
        logger.info("🔍 Checking environment variables...")
        
        required_vars = [
            'JWT_SECRET',
            'NEXT_PUBLIC_BASE_URL'
        ]
        
        optional_vars = [
            'URLHAUS_AUTH_KEY',
            'TURNSTILE_SECRET_KEY',
            'NEXT_PUBLIC_TURNSTILE_SITE_KEY'
        ]
        
        missing_required = []
        missing_optional = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_required.append(var)
        
        for var in optional_vars:
            if not os.getenv(var):
                missing_optional.append(var)
        
        if missing_required:
            logger.error(f"❌ Missing required environment variables: {missing_required}")
            logger.info("Please set these in your .env file")
            return False
        
        if missing_optional:
            logger.warning(f"⚠️ Missing optional environment variables: {missing_optional}")
            logger.info("Some features may be limited without these")
        
        logger.info("✅ Environment variables checked")
        return True
    
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
    
    def install_backend_dependencies(self) -> bool:
        """Install Node.js backend dependencies"""
        logger.info("📦 Installing backend dependencies...")
        
        backend_dir = self.project_root.parent / "backend"
        
        if not backend_dir.exists():
            logger.error("❌ Backend directory not found")
            return False
        
        try:
            result = subprocess.run(['npm', 'install'], 
                                  cwd=backend_dir, 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ Backend dependencies installed successfully")
                return True
            else:
                logger.error(f"❌ Failed to install backend dependencies: {result.stderr}")
                return False
                
        except FileNotFoundError:
            logger.error("❌ npm not found. Please install Node.js and npm.")
            return False
        except Exception as e:
            logger.error(f"❌ Error installing backend dependencies: {e}")
            return False
    
    def install_frontend_dependencies(self) -> bool:
        """Install Next.js frontend dependencies"""
        logger.info("📦 Installing frontend dependencies...")
        
        frontend_dir = self.project_root.parent / "frontend"
        
        if not frontend_dir.exists():
            logger.error("❌ Frontend directory not found")
            return False
        
        try:
            result = subprocess.run(['npm', 'install'], 
                                  cwd=frontend_dir, 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ Frontend dependencies installed successfully")
                return True
            else:
                logger.error(f"❌ Failed to install frontend dependencies: {result.stderr}")
                return False
                
        except FileNotFoundError:
            logger.error("❌ npm not found. Please install Node.js and npm.")
            return False
        except Exception as e:
            logger.error(f"❌ Error installing frontend dependencies: {e}")
            return False
    
    def start_python_api(self) -> Optional[subprocess.Popen]:
        """Start the enhanced Python API server"""
        logger.info("🐍 Starting enhanced Python API server...")
        
        try:
            api_script = self.project_root / "ai_training" / "enhanced_anime_api_server.py"
            
            if not api_script.exists():
                logger.error("❌ Enhanced anime API server not found")
                return None
            
            process = subprocess.Popen([
                sys.executable, str(api_script)
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            time.sleep(3)  # Wait for startup
            
            if process.poll() is None:
                logger.info("✅ Python API server started successfully")
                return process
            else:
                logger.error("❌ Python API server failed to start")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error starting Python API: {e}")
            return None
    
    def start_backend_server(self) -> Optional[subprocess.Popen]:
        """Start the Node.js backend server"""
        logger.info("🟢 Starting Node.js backend server...")
        
        backend_dir = self.project_root.parent / "backend"
        
        try:
            # Try server.js first, then app.js
            server_files = ['server.js', 'app.js', 'index.js']
            server_file = None
            
            for file in server_files:
                if (backend_dir / file).exists():
                    server_file = file
                    break
            
            if not server_file:
                logger.error("❌ No backend server file found")
                return None
            
            env = os.environ.copy()
            env['PORT'] = str(self.backend_port)
            
            process = subprocess.Popen(['node', server_file], 
                                     cwd=backend_dir,
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE,
                                     env=env)
            
            time.sleep(2)  # Wait for startup
            
            if process.poll() is None:
                logger.info("✅ Backend server started successfully")
                return process
            else:
                logger.error("❌ Backend server failed to start")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error starting backend server: {e}")
            return None
    
    def start_frontend_dev(self) -> Optional[subprocess.Popen]:
        """Start the Next.js frontend development server"""
        logger.info("⚛️ Starting Next.js frontend server...")
        
        frontend_dir = self.project_root.parent / "frontend"
        
        try:
            env = os.environ.copy()
            env['PORT'] = str(self.frontend_port)
            
            process = subprocess.Popen(['npm', 'run', 'dev'], 
                                     cwd=frontend_dir,
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE,
                                     env=env)
            
            time.sleep(5)  # Wait for Next.js to start
            
            if process.poll() is None:
                logger.info("✅ Frontend server started successfully")
                return process
            else:
                logger.error("❌ Frontend server failed to start")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error starting frontend server: {e}")
            return None
    
    def test_api_endpoints(self) -> bool:
        """Test all API endpoints"""
        logger.info("🧪 Testing API endpoints...")
        
        endpoints_to_test = [
            ('Python API Health', self.api_urls['python_health']),
            ('Backend Health', self.api_urls['backend_health']),
            ('Frontend', self.api_urls['frontend'])
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
        """Open the application in the default browser"""
        logger.info("🌐 Opening application in browser...")
        
        try:
            webbrowser.open(self.api_urls['login'])
            logger.info("✅ Browser opened to login page")
        except Exception as e:
            logger.warning(f"Could not open browser: {e}")
    
    def start_system(self) -> bool:
        """Start the complete enhanced system"""
        logger.info("🎌 Starting Enhanced Anime AI PhishGuard System")
        logger.info("=" * 60)
        
        try:
            # Pre-checks
            if not self.check_ollama_status():
                return False
            
            if not self.check_environment_variables():
                return False
            
            # Install dependencies
            if not self.install_python_dependencies():
                return False
            
            if not self.install_backend_dependencies():
                return False
            
            if not self.install_frontend_dependencies():
                return False
            
            # Start services
            python_api = self.start_python_api()
            if python_api:
                self.processes.append(python_api)
            else:
                return False
            
            backend_server = self.start_backend_server()
            if backend_server:
                self.processes.append(backend_server)
            else:
                return False
            
            frontend_server = self.start_frontend_dev()
            if frontend_server:
                self.processes.append(frontend_server)
            else:
                return False
            
            # Wait for services to stabilize
            logger.info("⏳ Waiting for services to stabilize...")
            time.sleep(10)
            
            # Test endpoints
            if not self.test_api_endpoints():
                logger.warning("⚠️ Some endpoints are not responding properly")
            
            # Success!
            logger.info("=" * 60)
            logger.info("🎉 ENHANCED ANIME AI PHISHGUARD SYSTEM STARTED SUCCESSFULLY!")
            logger.info("=" * 60)
            logger.info("")
            logger.info("🌐 Application URLs:")
            logger.info(f"   📱 Login Page: {self.api_urls['login']}")
            logger.info(f"   🎌 Anime Dashboard: {self.api_urls['anime_dashboard']}")
            logger.info(f"   🔧 Python API: {self.api_urls['python_health']}")
            logger.info(f"   ⚙️ Backend API: {self.api_urls['backend_health']}")
            logger.info("")
            logger.info("👤 Demo Login Credentials:")
            logger.info("   User: user@example.com / password123")
            logger.info("   Admin: admin@example.com / admin123")
            logger.info("")
            logger.info("🎯 Features Available:")
            logger.info("   • AI-chan Phishing Detection with URLhaus Intelligence")
            logger.info("   • Haru Recovery & Education Assistant")
            logger.info("   • Vision-Enhanced Image Analysis")
            logger.info("   • Japanese Voice Synthesis")
            logger.info("   • Secure Authentication with JWT")
            logger.info("   • Real-time Threat Intelligence")
            logger.info("")
            logger.info("🛑 Press Ctrl+C to stop all services")
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
    starter = EnhancedSystemStarter()
    
    if starter.start_system():
        logger.info("✅ System stopped successfully")
        sys.exit(0)
    else:
        logger.error("❌ System startup failed")
        sys.exit(1)

if __name__ == "__main__":
    main() 
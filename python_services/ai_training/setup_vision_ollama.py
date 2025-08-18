#!/usr/bin/env python3
"""
Vision Ollama Setup Script for PhishGuard AI
Sets up LLaVA vision model and RAG system for enhanced phishing detection
"""

import os
import sys
import subprocess
import logging
import requests
import json
from pathlib import Path
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VisionOllamaSetup:
    """Setup and configure Ollama with LLaVA vision model for PhishGuard AI"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
        self.vision_model = "llava"
        
    def check_ollama_installation(self) -> bool:
        """Check if Ollama is installed and running"""
        try:
            # Check if ollama command exists
            result = subprocess.run(['ollama', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"✅ Ollama installed: {result.stdout.strip()}")
                return True
            else:
                logger.error("❌ Ollama not found in PATH")
                return False
        except FileNotFoundError:
            logger.error("❌ Ollama not installed")
            return False
    
    def start_ollama_service(self) -> bool:
        """Start Ollama service"""
        try:
            logger.info("Starting Ollama service...")
            
            # Check if Ollama is already running
            try:
                response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
                if response.status_code == 200:
                    logger.info("✅ Ollama service is already running")
                    return True
            except:
                pass
            
            # Start Ollama service
            process = subprocess.Popen(['ollama', 'serve'], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE)
            
            # Wait for service to start
            for i in range(30):  # Wait up to 30 seconds
                try:
                    response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
                    if response.status_code == 200:
                        logger.info("✅ Ollama service started successfully")
                        return True
                except:
                    pass
                time.sleep(1)
            
            logger.error("❌ Failed to start Ollama service")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error starting Ollama: {e}")
            return False
    
    def pull_vision_model(self) -> bool:
        """Pull the LLaVA vision model"""
        try:
            logger.info(f"Pulling vision model: {self.vision_model}")
            
            # Check if model already exists
            try:
                response = requests.get(f"{self.ollama_url}/api/tags")
                if response.status_code == 200:
                    models = response.json().get('models', [])
                    if any(self.vision_model in model.get('name', '') for model in models):
                        logger.info(f"✅ Vision model {self.vision_model} already exists")
                        return True
            except:
                pass
            
            # Pull the model
            result = subprocess.run(['ollama', 'pull', self.vision_model], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"✅ Vision model {self.vision_model} pulled successfully")
                return True
            else:
                logger.error(f"❌ Failed to pull vision model: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error pulling vision model: {e}")
            return False
    
    def list_models(self) -> list:
        """List available models"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get('models', [])
                logger.info(f"Available models: {[model['name'] for model in models]}")
                return models
            else:
                logger.error("❌ Failed to list models")
                return []
        except Exception as e:
            logger.error(f"❌ Error listing models: {e}")
            return []
    
    def test_vision_model(self) -> bool:
        """Test LLaVA vision model with a simple text prompt"""
        try:
            logger.info(f"Testing vision model: {self.vision_model}")
            
            payload = {
                "model": self.vision_model,
                "prompt": "Hello, I'm testing the vision model. Can you respond to this text message?",
                "stream": False
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", 
                                   json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('response'):
                    logger.info(f"✅ Vision model {self.vision_model} text generation test passed")
                    return True
                else:
                    logger.error(f"❌ Vision model {self.vision_model} returned empty response")
                    return False
            else:
                logger.error(f"❌ Vision model {self.vision_model} test failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error testing vision model {self.vision_model}: {e}")
            return False
    
    def install_dependencies(self) -> bool:
        """Install required Python dependencies for vision system"""
        try:
            logger.info("Installing vision system dependencies...")
            
            # List of required packages
            packages = [
                "pillow",  # For image processing
                "chromadb",  # For RAG system
                "numpy",  # For numerical operations
                "requests"  # For API calls
            ]
            
            for package in packages:
                logger.info(f"Installing {package}...")
                result = subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info(f"✅ {package} installed successfully")
                else:
                    logger.warning(f"⚠️ Failed to install {package}: {result.stderr}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error installing dependencies: {e}")
            return False
    
    def create_directories(self) -> bool:
        """Create necessary directories for the vision system"""
        try:
            logger.info("Creating vision system directories...")
            
            directories = [
                "rag_database",
                "vision_cache",
                "image_uploads",
                "screenshots"
            ]
            
            for directory in directories:
                dir_path = Path(directory)
                dir_path.mkdir(exist_ok=True)
                logger.info(f"✅ Created directory: {directory}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error creating directories: {e}")
            return False
    
    def setup_environment(self) -> bool:
        """Complete vision environment setup"""
        logger.info("🚀 Setting up Vision-Enabled Ollama Environment for PhishGuard AI")
        logger.info("=" * 60)
        
        # Step 1: Check Ollama installation
        if not self.check_ollama_installation():
            logger.error("Please install Ollama from https://ollama.ai")
            return False
        
        # Step 2: Start Ollama service
        if not self.start_ollama_service():
            return False
        
        # Step 3: Install Python dependencies
        if not self.install_dependencies():
            logger.warning("⚠️ Some dependencies failed to install. Continuing...")
        
        # Step 4: Create directories
        if not self.create_directories():
            return False
        
        # Step 5: Pull vision model
        if not self.pull_vision_model():
            return False
        
        # Step 6: List models
        models = self.list_models()
        
        # Step 7: Test vision model
        if not self.test_vision_model():
            return False
        
        logger.info("=" * 60)
        logger.info("✅ Vision-Enabled Ollama environment setup completed successfully!")
        logger.info("🎯 LLaVA vision model is ready for image and text analysis!")
        logger.info("🧠 RAG system will be initialized when you run the vision system")
        
        return True

def main():
    """Main function"""
    setup = VisionOllamaSetup()
    
    if setup.setup_environment():
        logger.info("🎉 Vision system setup completed!")
        logger.info("📝 Next steps:")
        logger.info("   1. Run: python vision_ollama_integration.py")
        logger.info("   2. Test with your own images and URLs")
        logger.info("   3. The system will automatically initialize RAG capabilities")
        sys.exit(0)
    else:
        logger.error("❌ Vision system setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 
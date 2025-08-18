#!/usr/bin/env python3
"""
Ollama Setup Script for PhishGuard AI
Sets up Ollama and prepares models for training
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

class OllamaSetup:
    """Setup and configure Ollama for PhishGuard AI"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
        self.base_model = "gemma2:4b"
        
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
    
    def pull_base_model(self) -> bool:
        """Pull the base Gemma model"""
        try:
            logger.info(f"Pulling base model: {self.base_model}")
            
            # Check if model already exists
            try:
                response = requests.get(f"{self.ollama_url}/api/tags")
                if response.status_code == 200:
                    models = response.json().get('models', [])
                    if any(self.base_model in model.get('name', '') for model in models):
                        logger.info(f"✅ Base model {self.base_model} already exists")
                        return True
            except:
                pass
            
            # Pull the model
            result = subprocess.run(['ollama', 'pull', self.base_model], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"✅ Base model {self.base_model} pulled successfully")
                return True
            else:
                logger.error(f"❌ Failed to pull base model: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error pulling base model: {e}")
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
    
    def test_model_generation(self, model_name: str) -> bool:
        """Test model generation"""
        try:
            logger.info(f"Testing model generation for {model_name}")
            
            payload = {
                "model": model_name,
                "prompt": "Hello, how are you?",
                "stream": False
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", 
                                   json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('response'):
                    logger.info(f"✅ Model {model_name} generation test passed")
                    return True
                else:
                    logger.error(f"❌ Model {model_name} returned empty response")
                    return False
            else:
                logger.error(f"❌ Model {model_name} generation test failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error testing model {model_name}: {e}")
            return False
    
    def setup_environment(self) -> bool:
        """Complete environment setup"""
        logger.info("🚀 Setting up Ollama environment for PhishGuard AI")
        logger.info("=" * 50)
        
        # Step 1: Check Ollama installation
        if not self.check_ollama_installation():
            logger.error("Please install Ollama from https://ollama.ai")
            return False
        
        # Step 2: Start Ollama service
        if not self.start_ollama_service():
            return False
        
        # Step 3: Pull base model
        if not self.pull_base_model():
            return False
        
        # Step 4: List models
        models = self.list_models()
        
        # Step 5: Test base model
        if not self.test_model_generation(self.base_model):
            return False
        
        logger.info("=" * 50)
        logger.info("✅ Ollama environment setup completed successfully!")
        logger.info("Ready for model training!")
        
        return True

def main():
    """Main function"""
    setup = OllamaSetup()
    
    if setup.setup_environment():
        logger.info("🎉 Setup completed! You can now run the training pipeline.")
        sys.exit(0)
    else:
        logger.error("❌ Setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 
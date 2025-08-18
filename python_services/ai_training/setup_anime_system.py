#!/usr/bin/env python3
"""
Anime PhishGuard AI Setup Script
Sets up llama3.2-vision:11b model and Japanese Parler-TTS for anime characters
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
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AnimeSystemSetup:
    """Setup and configure the anime-enabled PhishGuard AI system"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
        self.vision_model = "llama3.2-vision:11b"
        
    def check_ollama_installation(self) -> bool:
        """Check if Ollama is installed and running"""
        try:
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
            for i in range(30):
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
        """Pull the llama3.2-vision:11b model"""
        try:
            logger.info(f"Pulling vision model: {self.vision_model}")
            logger.info("⚠️ This is a large model (11B parameters) and may take a while...")
            
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
    
    def install_japanese_tts_dependencies(self) -> bool:
        """Install Japanese TTS dependencies"""
        try:
            logger.info("📦 Installing Japanese TTS dependencies...")
            
            # Install Parler-TTS
            logger.info("Installing Parler-TTS...")
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', 
                'git+https://github.com/huggingface/parler-tts.git'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ Parler-TTS installed successfully")
            else:
                logger.warning(f"⚠️ Parler-TTS installation warning: {result.stderr}")
            
            # Install RubyInserter for Japanese text processing
            logger.info("Installing RubyInserter...")
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install',
                'git+https://github.com/getuka/RubyInserter.git'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ RubyInserter installed successfully")
            else:
                logger.warning(f"⚠️ RubyInserter installation warning: {result.stderr}")
            
            # Install additional audio dependencies
            audio_packages = [
                "soundfile",
                "torch",
                "transformers",
                "accelerate"
            ]
            
            for package in audio_packages:
                logger.info(f"Installing {package}...")
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', package
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info(f"✅ {package} installed successfully")
                else:
                    logger.warning(f"⚠️ Failed to install {package}: {result.stderr}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error installing Japanese TTS dependencies: {e}")
            return False
    
    def install_anime_dependencies(self) -> bool:
        """Install all anime system dependencies"""
        try:
            logger.info("🎌 Installing anime system dependencies...")
            
            # Core dependencies for the anime system
            packages = [
                "pillow>=10.0.0",
                "numpy>=1.24.0",
                "chromadb>=0.4.0",
                "requests>=2.31.0",
                "pandas>=2.0.0",
                "colorama>=0.4.6",
                "tqdm>=4.65.0"
            ]
            
            for package in packages:
                logger.info(f"Installing {package}...")
                result = subprocess.run([
                    sys.executable, '-m', 'pip', 'install', package
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info(f"✅ {package} installed successfully")
                else:
                    logger.warning(f"⚠️ Failed to install {package}: {result.stderr}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error installing anime dependencies: {e}")
            return False
    
    def test_japanese_tts(self) -> bool:
        """Test Japanese TTS functionality"""
        try:
            logger.info("🎌 Testing Japanese TTS...")
            
            # Try to import and test TTS
            import torch
            from parler_tts import ParlerTTSForConditionalGeneration
            from transformers import AutoTokenizer
            import soundfile as sf
            from rubyinserter import add_ruby
            
            device = "cuda:0" if torch.cuda.is_available() else "cpu"
            logger.info(f"Using device: {device}")
            
            # Load the Japanese TTS model
            logger.info("Loading Japanese Parler-TTS model...")
            model = ParlerTTSForConditionalGeneration.from_pretrained(
                "2121-8/japanese-parler-tts-mini"
            ).to(device)
            
            prompt_tokenizer = AutoTokenizer.from_pretrained(
                "2121-8/japanese-parler-tts-mini", 
                subfolder="prompt_tokenizer"
            )
            
            description_tokenizer = AutoTokenizer.from_pretrained(
                "2121-8/japanese-parler-tts-mini", 
                subfolder="description_tokenizer"
            )
            
            # Test AI-chan voice
            logger.info("Testing AI-chan voice...")
            prompt = "危険です！"  # "It is dangerous!"
            description = "A cheerful young female speaker with a bright, anime-style voice delivers her words with enthusiasm."
            
            prompt_with_ruby = add_ruby(prompt)
            input_ids = description_tokenizer(description, return_tensors="pt").input_ids.to(device)
            prompt_input_ids = prompt_tokenizer(prompt_with_ruby, return_tensors="pt").input_ids.to(device)
            
            generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
            audio_arr = generation.cpu().numpy().squeeze()
            sf.write("test_ai_voice.wav", audio_arr, model.config.sampling_rate)
            
            # Test Haru voice
            logger.info("Testing Haru voice...")
            prompt = "めんどくさいな..."  # "What a pain in the ass..."
            description = "A lazy young male speaker with a slightly deep voice delivers his words in a relaxed manner."
            
            prompt_with_ruby = add_ruby(prompt)
            input_ids = description_tokenizer(description, return_tensors="pt").input_ids.to(device)
            prompt_input_ids = prompt_tokenizer(prompt_with_ruby, return_tensors="pt").input_ids.to(device)
            
            generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
            audio_arr = generation.cpu().numpy().squeeze()
            sf.write("test_haru_voice.wav", audio_arr, model.config.sampling_rate)
            
            logger.info("✅ Japanese TTS test completed successfully!")
            logger.info("Generated test files: test_ai_voice.wav, test_haru_voice.wav")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Japanese TTS test failed: {e}")
            return False
    
    def test_vision_model(self) -> bool:
        """Test llama3.2-vision:11b model"""
        try:
            logger.info(f"Testing vision model: {self.vision_model}")
            
            payload = {
                "model": self.vision_model,
                "prompt": "Hello! I'm testing the anime vision model. Please respond cheerfully!",
                "stream": False
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", 
                                   json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('response'):
                    logger.info(f"✅ Vision model {self.vision_model} test passed")
                    return True
                else:
                    logger.error(f"❌ Vision model {self.vision_model} returned empty response")
                    return False
            else:
                logger.error(f"❌ Vision model {self.vision_model} test failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error testing vision model: {e}")
            return False
    
    def create_directories(self) -> bool:
        """Create necessary directories for the anime system"""
        try:
            logger.info("📁 Creating anime system directories...")
            
            directories = [
                "rag_database",
                "voice_cache",
                "anime_voices",
                "character_data",
                "demo_images"
            ]
            
            for directory in directories:
                dir_path = Path(directory)
                dir_path.mkdir(exist_ok=True)
                logger.info(f"✅ Created directory: {directory}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error creating directories: {e}")
            return False
    
    def setup_anime_environment(self) -> bool:
        """Complete anime environment setup"""
        logger.info("🎌 Setting up Anime PhishGuard AI Environment")
        logger.info("=" * 60)
        
        # Step 1: Check Ollama installation
        if not self.check_ollama_installation():
            logger.error("Please install Ollama from https://ollama.ai")
            return False
        
        # Step 2: Start Ollama service
        if not self.start_ollama_service():
            return False
        
        # Step 3: Install anime system dependencies
        if not self.install_anime_dependencies():
            logger.warning("⚠️ Some anime dependencies failed to install. Continuing...")
        
        # Step 4: Install Japanese TTS dependencies
        if not self.install_japanese_tts_dependencies():
            logger.warning("⚠️ Japanese TTS installation had issues. Continuing...")
        
        # Step 5: Create directories
        if not self.create_directories():
            return False
        
        # Step 6: Pull vision model (this may take a while)
        if not self.pull_vision_model():
            return False
        
        # Step 7: Test vision model
        if not self.test_vision_model():
            logger.warning("⚠️ Vision model test failed, but continuing...")
        
        # Step 8: Test Japanese TTS
        if not self.test_japanese_tts():
            logger.warning("⚠️ Japanese TTS test failed, but continuing...")
        
        logger.info("=" * 60)
        logger.info("🎉 Anime PhishGuard AI environment setup completed!")
        logger.info("🌸 AI-chan (cheerful anime girl) is ready for phishing detection!")
        logger.info("😴 Haru (lazy but caring anime boy) is ready for recovery assistance!")
        logger.info("🎌 Japanese voice synthesis is enabled!")
        
        return True

def main():
    """Main function"""
    setup = AnimeSystemSetup()
    
    if setup.setup_anime_environment():
        logger.info("🎉 Anime system setup completed!")
        logger.info("📝 Next steps:")
        logger.info("   1. Run: python anime_vision_ollama_integration.py")
        logger.info("   2. Test with: python anime_demo.py")
        logger.info("   3. Try voice generation with the anime characters!")
        logger.info("\n🎌 Enjoy your anime-powered phishing detection system!")
        sys.exit(0)
    else:
        logger.error("❌ Anime system setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 
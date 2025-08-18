#!/usr/bin/env python3
"""
Anime-Enabled Vision PhishGuard AI with Japanese Voice
Integrates llama3.2-vision:11b and Japanese Parler-TTS for anime character personas
"""

import requests
import json
import logging
import base64
import io
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import time
from datetime import datetime
import numpy as np
from PIL import Image
import hashlib
import asyncio

# For Japanese TTS integration
try:
    import torch
    from parler_tts import ParlerTTSForConditionalGeneration
    from transformers import AutoTokenizer
    import soundfile as sf
    from rubyinserter import add_ruby
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    logging.warning("Japanese TTS dependencies not available. Voice features will be disabled.")

# For RAG integration
try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    logging.warning("ChromaDB not available. RAG features will be disabled.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JapaneseTTSEngine:
    """Japanese Text-to-Speech engine using Parler-TTS Mini"""
    
    def __init__(self):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.prompt_tokenizer = None
        self.description_tokenizer = None
        self.tts_enabled = TTS_AVAILABLE
        
        # Voice descriptions for anime characters
        self.ai_voice_description = "A cheerful young female speaker with a bright, anime-style voice delivers her words with enthusiasm and energy at a moderate pace in a clear recording environment."
        self.haru_voice_description = "A lazy young male speaker with a slightly deep voice delivers his words in a relaxed, somewhat monotone manner with occasional sighs in a clear recording environment."
        
        if self.tts_enabled:
            self._initialize_tts()
    
    def _initialize_tts(self):
        """Initialize the Japanese TTS model"""
        try:
            logger.info("Initializing Japanese TTS engine...")
            self.model = ParlerTTSForConditionalGeneration.from_pretrained(
                "2121-8/japanese-parler-tts-mini"
            ).to(self.device)
            
            self.prompt_tokenizer = AutoTokenizer.from_pretrained(
                "2121-8/japanese-parler-tts-mini", 
                subfolder="prompt_tokenizer"
            )
            
            self.description_tokenizer = AutoTokenizer.from_pretrained(
                "2121-8/japanese-parler-tts-mini", 
                subfolder="description_tokenizer"
            )
            
            logger.info("✅ Japanese TTS engine initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Japanese TTS: {e}")
            self.tts_enabled = False
    
    def generate_voice(self, text: str, character: str = "ai", output_path: str = None) -> Optional[str]:
        """Generate Japanese voice for the given text and character"""
        if not self.tts_enabled:
            logger.warning("TTS not available")
            return None
        
        try:
            # Select voice description based on character
            if character.lower() == "ai":
                voice_description = self.ai_voice_description
            elif character.lower() == "haru":
                voice_description = self.haru_voice_description
            else:
                voice_description = self.ai_voice_description
            
            # Add ruby notation for better pronunciation
            text_with_ruby = add_ruby(text)
            
            # Tokenize inputs
            input_ids = self.description_tokenizer(
                voice_description, return_tensors="pt"
            ).input_ids.to(self.device)
            
            prompt_input_ids = self.prompt_tokenizer(
                text_with_ruby, return_tensors="pt"
            ).input_ids.to(self.device)
            
            # Generate audio
            generation = self.model.generate(
                input_ids=input_ids, 
                prompt_input_ids=prompt_input_ids
            )
            
            audio_arr = generation.cpu().numpy().squeeze()
            
            # Save to file
            if output_path is None:
                output_path = f"voice_{character}_{int(time.time())}.wav"
            
            sf.write(output_path, audio_arr, self.model.config.sampling_rate)
            logger.info(f"✅ Generated voice: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"❌ Error generating voice: {e}")
            return None

class AnimeVisionOllamaClient:
    """Enhanced Ollama client with llama3.2-vision:11b and anime personas"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
        self.vision_model = "llama3.2-vision:11b"  # Updated to llama3.2-vision:11b
        self.tts_engine = JapaneseTTSEngine()
        
        # Anime character personalities
        self.ai_persona = {
            "name": "AI-chan",
            "personality": "cheerful anime girl",
            "voice_character": "ai",
            "danger_phrase": "危険です！", # "It is dangerous!" in Japanese
            "excited_phrases": ["がんばって！", "すごいね！", "気をつけて！"],
            "greeting": "こんにちは！AI-chanです♪"
        }
        
        self.haru_persona = {
            "name": "Haru",
            "personality": "lazy but caring anime boy",
            "voice_character": "haru",
            "lazy_phrase": "めんどくさいな...", # "What a pain in the ass..." in Japanese
            "caring_phrases": ["まあ、大丈夫だよ", "心配しないで", "一緒に解決しよう"],
            "greeting": "はぁ...Haruだよ。何か用？"
        }
    
    def list_models(self) -> List[Dict]:
        """List available models in Ollama"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            return response.json().get('models', [])
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
    
    def pull_vision_model(self) -> bool:
        """Pull the llama3.2-vision:11b model"""
        try:
            logger.info(f"Pulling vision model: {self.vision_model}")
            
            # Check if model already exists
            models = self.list_models()
            if any(self.vision_model in model.get('name', '') for model in models):
                logger.info(f"✅ Vision model {self.vision_model} already exists")
                return True
            
            # Pull the model
            response = self.session.post(
                f"{self.base_url}/api/pull",
                json={"name": self.vision_model}
            )
            response.raise_for_status()
            
            logger.info(f"✅ Vision model {self.vision_model} pulled successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error pulling vision model: {e}")
            return False
    
    def encode_image_to_base64(self, image_path: Union[str, Path]) -> str:
        """Encode image to base64 for API transmission"""
        try:
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                return encoded_string
        except Exception as e:
            logger.error(f"Error encoding image {image_path}: {e}")
            return ""
    
    def analyze_image_with_persona(self, image_path: Union[str, Path], prompt: str, character: str = "ai") -> Optional[Dict]:
        """Analyze image with anime persona and voice generation"""
        try:
            # Get persona information
            persona = self.ai_persona if character.lower() == "ai" else self.haru_persona
            
            # Encode image to base64
            image_base64 = self.encode_image_to_base64(image_path)
            if not image_base64:
                return None
            
            # Create persona-enhanced prompt
            if character.lower() == "ai":
                enhanced_prompt = f"""You are {persona['name']}, a {persona['personality']} who specializes in cybersecurity and phishing detection. 
                
Respond in a cheerful, enthusiastic manner typical of an anime girl character. Use expressions like "♪", "！", and show excitement about helping with security.

{prompt}

If you detect something dangerous, be sure to express concern in a cute but serious way."""
            else:  # Haru
                enhanced_prompt = f"""You are {persona['name']}, a {persona['personality']} who helps with cybersecurity recovery and education.

Respond in a slightly lazy, relaxed manner but show that you genuinely care. Use expressions like "...まあ", "はぁ", and occasional sighs, but always provide helpful information.

{prompt}

Even though you might sound lazy, you actually care about helping people stay safe online."""
            
            # Prepare payload for vision analysis
            payload = {
                "model": self.vision_model,
                "prompt": enhanced_prompt,
                "images": [image_base64],
                "stream": False
            }
            
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=90  # Longer timeout for vision processing
            )
            response.raise_for_status()
            
            result = response.json()
            analysis_text = result.get('response', '')
            
            # Generate voice response
            voice_file = None
            if analysis_text:
                # Check if this is a danger detection
                if character.lower() == "ai" and any(word in analysis_text.lower() for word in ['phishing', 'suspicious', 'dangerous', 'scam']):
                    # Generate danger warning voice
                    voice_file = self.tts_engine.generate_voice(
                        persona['danger_phrase'], 
                        character=character,
                        output_path=f"danger_warning_{int(time.time())}.wav"
                    )
                elif character.lower() == "haru" and len(prompt.split()) > 10:  # If user asks too many questions
                    # Generate lazy response
                    voice_file = self.tts_engine.generate_voice(
                        persona['lazy_phrase'], 
                        character=character,
                        output_path=f"lazy_response_{int(time.time())}.wav"
                    )
            
            return {
                'analysis': analysis_text,
                'character': persona['name'],
                'personality': persona['personality'],
                'voice_file': voice_file,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing image with persona: {e}")
            return None
    
    def generate_response_with_persona(self, prompt: str, character: str = "ai", **kwargs) -> Optional[Dict]:
        """Generate text response with anime persona"""
        try:
            # Get persona information
            persona = self.ai_persona if character.lower() == "ai" else self.haru_persona
            
            # Create persona-enhanced prompt
            if character.lower() == "ai":
                enhanced_prompt = f"""You are {persona['name']}, a {persona['personality']} who specializes in cybersecurity and phishing detection.

Respond in a cheerful, enthusiastic manner typical of an anime girl character. Be helpful and energetic!

{prompt}"""
            else:  # Haru
                enhanced_prompt = f"""You are {persona['name']}, a {persona['personality']} who helps with cybersecurity recovery and education.

Respond in a slightly lazy, relaxed manner but show that you genuinely care. Even if you sound lazy, provide helpful information.

{prompt}"""
            
            payload = {
                "model": self.vision_model,
                "prompt": enhanced_prompt,
                "stream": False,
                **kwargs
            }
            
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            response_text = result.get('response', '')
            
            # Generate voice for specific scenarios
            voice_file = None
            if character.lower() == "haru" and "?" in prompt:
                # If user asks questions, Haru might get lazy
                voice_file = self.tts_engine.generate_voice(
                    persona['lazy_phrase'], 
                    character=character,
                    output_path=f"haru_lazy_{int(time.time())}.wav"
                )
            
            return {
                'response': response_text,
                'character': persona['name'],
                'personality': persona['personality'],
                'voice_file': voice_file,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating response with persona: {e}")
            return None

class RAGSystem:
    """Retrieval-Augmented Generation system for enhanced context"""
    
    def __init__(self, db_path: str = "./rag_database"):
        self.db_path = Path(db_path)
        self.db_path.mkdir(exist_ok=True)
        
        if CHROMA_AVAILABLE:
            self.client = chromadb.PersistentClient(
                path=str(self.db_path),
                settings=Settings(anonymized_telemetry=False)
            )
            self.collection = self.client.get_or_create_collection(
                name="phishing_knowledge",
                metadata={"description": "Phishing detection knowledge base"}
            )
            self.rag_enabled = True
        else:
            self.rag_enabled = False
            logger.warning("RAG system disabled - ChromaDB not available")
    
    def add_knowledge(self, text: str, metadata: Dict = None) -> bool:
        """Add knowledge to the RAG database"""
        if not self.rag_enabled:
            return False
        
        try:
            doc_id = hashlib.md5(text.encode()).hexdigest()
            self.collection.add(
                documents=[text],
                metadatas=[metadata or {}],
                ids=[doc_id]
            )
            return True
        except Exception as e:
            logger.error(f"Error adding knowledge to RAG: {e}")
            return False
    
    def retrieve_relevant_context(self, query: str, n_results: int = 3) -> List[str]:
        """Retrieve relevant context for a query"""
        if not self.rag_enabled:
            return []
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            if results and results['documents']:
                return results['documents'][0]
            return []
            
        except Exception as e:
            logger.error(f"Error retrieving context from RAG: {e}")
            return []

class AnimeAI:
    """AI-chan - Cheerful anime girl phishing detector with voice"""
    
    def __init__(self, vision_client: AnimeVisionOllamaClient, rag_system: RAGSystem):
        self.client = vision_client
        self.rag = rag_system
        self.character = "ai"
        self.persona = vision_client.ai_persona
        
        # Initialize with Japanese phrases
        self.danger_phrases = [
            "危険です！",  # It is dangerous!
            "気をつけて！",  # Be careful!
            "これは怪しいですね...",  # This is suspicious...
        ]
    
    def analyze_with_voice_warning(self, image_path: Union[str, Path] = None, url: str = None) -> Dict[str, Any]:
        """Analyze content and provide voice warning if dangerous"""
        results = {
            'character': self.persona['name'],
            'analysis_type': 'phishing_detection',
            'timestamp': datetime.now().isoformat()
        }
        
        if image_path:
            prompt = """Analyze this image for potential phishing or scam content. Look for:
            
1. Suspicious logos or branding
2. Fake login forms
3. Urgent or threatening messages
4. Suspicious QR codes or links
5. Poor quality graphics indicating scams

Be enthusiastic and thorough in your analysis! ♪"""
            
            analysis = self.client.analyze_image_with_persona(image_path, prompt, self.character)
            if analysis:
                results['image_analysis'] = analysis
                
                # Check if danger detected and voice warning generated
                if analysis.get('voice_file'):
                    results['danger_detected'] = True
                    results['voice_warning'] = analysis['voice_file']
        
        if url:
            # Get context from RAG
            context = self.rag.retrieve_relevant_context(f"URL analysis {url}")
            context_text = "\n".join(context) if context else ""
            
            prompt = f"""Analyze this URL for phishing threats: {url}

Relevant context:
{context_text}

Provide a detailed analysis with enthusiasm! Be sure to warn about any dangers you find! ♪"""
            
            response = self.client.generate_response_with_persona(prompt, self.character)
            if response:
                results['url_analysis'] = response
        
        return results
    
    def get_cheerful_greeting(self) -> Dict[str, Any]:
        """Get AI-chan's cheerful greeting with voice"""
        greeting_text = self.persona['greeting']
        voice_file = self.client.tts_engine.generate_voice(
            greeting_text, 
            character=self.character,
            output_path=f"ai_greeting_{int(time.time())}.wav"
        )
        
        return {
            'character': self.persona['name'],
            'greeting': greeting_text,
            'voice_file': voice_file,
            'personality': self.persona['personality']
        }

class AnimeHaru:
    """Haru - Lazy but caring anime boy for recovery and education"""
    
    def __init__(self, vision_client: AnimeVisionOllamaClient, rag_system: RAGSystem):
        self.client = vision_client
        self.rag = rag_system
        self.character = "haru"
        self.persona = vision_client.haru_persona
        
        # Track question count to trigger lazy responses
        self.question_count = 0
    
    def help_with_lazy_attitude(self, situation: str, image_path: Union[str, Path] = None) -> Dict[str, Any]:
        """Help user with Haru's characteristic lazy but caring attitude"""
        self.question_count += 1
        
        results = {
            'character': self.persona['name'],
            'situation': situation,
            'help_type': 'recovery_assistance',
            'timestamp': datetime.now().isoformat()
        }
        
        # Get recovery guidance from RAG
        recovery_context = self.rag.retrieve_relevant_context("recovery steps after phishing")
        
        if image_path:
            prompt = f"""The user is dealing with this situation: {situation}

Look at this image and help them understand what's happening. Even though you might sound lazy, you genuinely care about helping them.

Be relaxed in your response but provide helpful information."""
            
            analysis = self.client.analyze_image_with_persona(image_path, prompt, self.character)
            if analysis:
                results['image_analysis'] = analysis
        
        # Generate text response
        context_text = "\n".join(recovery_context) if recovery_context else ""
        prompt = f"""Someone needs help with: {situation}

Recovery context:
{context_text}

Help them out, but respond in your characteristic lazy but caring way. Show that you care even if you sound tired."""
        
        response = self.client.generate_response_with_persona(prompt, self.character)
        if response:
            results['help_response'] = response
        
        # Generate lazy response if too many questions
        if self.question_count > 3:
            lazy_voice = self.client.tts_engine.generate_voice(
                self.persona['lazy_phrase'],
                character=self.character,
                output_path=f"haru_lazy_response_{int(time.time())}.wav"
            )
            results['lazy_response'] = lazy_voice
            results['message'] = "Haru is getting a bit tired of all the questions..."
            self.question_count = 0  # Reset counter
        
        return results
    
    def get_lazy_greeting(self) -> Dict[str, Any]:
        """Get Haru's lazy greeting with voice"""
        greeting_text = self.persona['greeting']
        voice_file = self.client.tts_engine.generate_voice(
            greeting_text,
            character=self.character,
            output_path=f"haru_greeting_{int(time.time())}.wav"
        )
        
        return {
            'character': self.persona['name'],
            'greeting': greeting_text,
            'voice_file': voice_file,
            'personality': self.persona['personality']
        }

class AnimePhishGuardManager:
    """Manager for anime-enabled PhishGuard system"""
    
    def __init__(self):
        self.vision_client = AnimeVisionOllamaClient()
        self.rag_system = RAGSystem()
        self.ai_chan = AnimeAI(self.vision_client, self.rag_system)
        self.haru = AnimeHaru(self.vision_client, self.rag_system)
        
        # Initialize anime knowledge
        self._initialize_anime_knowledge()
    
    def _initialize_anime_knowledge(self):
        """Initialize RAG with anime character knowledge"""
        anime_knowledge = [
            "AI-chan is a cheerful anime girl who loves helping with cybersecurity",
            "Haru is a lazy but caring anime boy who specializes in recovery assistance",
            "AI-chan says '危険です！' (It is dangerous!) when detecting phishing",
            "Haru says 'めんどくさいな...' (What a pain in the ass...) when asked too many questions",
            "Both characters use Japanese voice synthesis for responses"
        ]
        
        for knowledge in anime_knowledge:
            self.rag_system.add_knowledge(
                knowledge,
                {"type": "anime_character", "source": "system"}
            )
    
    def setup_anime_system(self) -> bool:
        """Setup the anime-enabled system"""
        logger.info("🚀 Setting up Anime PhishGuard AI System")
        logger.info("=" * 50)
        
        # Pull llama3.2-vision:11b model
        if not self.vision_client.pull_vision_model():
            logger.error("Failed to pull llama3.2-vision:11b model")
            return False
        
        # Test Japanese TTS
        if self.vision_client.tts_engine.tts_enabled:
            logger.info("Testing Japanese TTS...")
            test_voice = self.vision_client.tts_engine.generate_voice(
                "こんにちは、テストです。",
                character="ai",
                output_path="tts_test.wav"
            )
            if test_voice:
                logger.info("✅ Japanese TTS working correctly")
            else:
                logger.warning("⚠️ Japanese TTS test failed")
        
        logger.info("✅ Anime system setup completed!")
        return True
    
    def demo_anime_interaction(self):
        """Demo the anime character interactions"""
        logger.info("🎌 Starting Anime Character Demo")
        
        # AI-chan greeting
        ai_greeting = self.ai_chan.get_cheerful_greeting()
        logger.info(f"🌸 {ai_greeting['character']}: {ai_greeting['greeting']}")
        
        # Haru greeting
        haru_greeting = self.haru.get_lazy_greeting()
        logger.info(f"😴 {haru_greeting['character']}: {haru_greeting['greeting']}")
        
        return {
            'ai_greeting': ai_greeting,
            'haru_greeting': haru_greeting
        }

def main():
    """Main function to setup and test anime system"""
    manager = AnimePhishGuardManager()
    
    # Setup anime system
    if manager.setup_anime_system():
        logger.info("✅ Anime system setup completed")
        
        # Run demo
        demo_results = manager.demo_anime_interaction()
        logger.info("🎉 Anime demo completed!")
        
    else:
        logger.error("❌ Failed to setup anime system")

if __name__ == "__main__":
    main() 
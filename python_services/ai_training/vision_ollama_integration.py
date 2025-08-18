#!/usr/bin/env python3
"""
Vision-Enabled Ollama Integration for PhishGuard AI
Supports LLaVA model for text and image analysis with RAG integration
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

class VisionOllamaClient:
    """Enhanced Ollama client with vision capabilities using LLaVA"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
        self.vision_model = "llava"
        
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
        """Pull the LLaVA vision model"""
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
    
    def encode_pil_image_to_base64(self, image: Image.Image) -> str:
        """Encode PIL Image to base64"""
        try:
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
            return img_str
        except Exception as e:
            logger.error(f"Error encoding PIL image: {e}")
            return ""
    
    def analyze_image(self, image_path: Union[str, Path], prompt: str = "Analyze this image for any suspicious or phishing-related content") -> Optional[str]:
        """Analyze an image using LLaVA vision model"""
        try:
            # Encode image to base64
            image_base64 = self.encode_image_to_base64(image_path)
            if not image_base64:
                return None
            
            # Prepare payload for vision analysis
            payload = {
                "model": self.vision_model,
                "prompt": prompt,
                "images": [image_base64],
                "stream": False
            }
            
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60  # Longer timeout for vision processing
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get('response', '')
            
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            return None
    
    def analyze_pil_image(self, image: Image.Image, prompt: str = "Analyze this image for any suspicious or phishing-related content") -> Optional[str]:
        """Analyze a PIL Image using LLaVA vision model"""
        try:
            # Encode PIL image to base64
            image_base64 = self.encode_pil_image_to_base64(image)
            if not image_base64:
                return None
            
            # Prepare payload for vision analysis
            payload = {
                "model": self.vision_model,
                "prompt": prompt,
                "images": [image_base64],
                "stream": False
            }
            
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get('response', '')
            
        except Exception as e:
            logger.error(f"Error analyzing PIL image: {e}")
            return None
    
    def generate_response(self, model_name: str, prompt: str, **kwargs) -> Optional[str]:
        """Generate text response from a model"""
        try:
            payload = {
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                **kwargs
            }
            
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get('response', '')
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
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
            # Generate a simple hash as ID
            doc_id = hashlib.md5(text.encode()).hexdigest()
            
            # Add to collection
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
    
    def initialize_phishing_knowledge(self):
        """Initialize the RAG system with phishing detection knowledge"""
        if not self.rag_enabled:
            return
        
        # Add common phishing indicators
        phishing_indicators = [
            "Suspicious URLs with misspelled domain names",
            "Requests for personal information like passwords or credit card details",
            "Urgent or threatening language to create panic",
            "Generic greetings instead of personalized messages",
            "Poor grammar and spelling errors",
            "Suspicious attachments or links",
            "Requests to verify account information",
            "Offers that seem too good to be true",
            "Requests for immediate action or payment",
            "Suspicious sender email addresses"
        ]
        
        for indicator in phishing_indicators:
            self.add_knowledge(
                indicator,
                {"type": "phishing_indicator", "category": "general"}
            )
        
        # Add recovery guidance
        recovery_guidance = [
            "If you clicked a suspicious link, immediately change your passwords",
            "Contact your bank if financial information was compromised",
            "Enable two-factor authentication on all accounts",
            "Report phishing attempts to relevant authorities",
            "Scan your device for malware if suspicious activity occurred",
            "Monitor your accounts for unauthorized transactions",
            "Consider freezing your credit if personal information was exposed"
        ]
        
        for guidance in recovery_guidance:
            self.add_knowledge(
                guidance,
                {"type": "recovery_guidance", "category": "recovery"}
            )

class VisionPhishGuardAI:
    """Vision-enabled PhishGuard AI with RAG integration"""
    
    def __init__(self, vision_client: VisionOllamaClient, rag_system: RAGSystem):
        self.client = vision_client
        self.rag = rag_system
        self.model_name = "llava"
        
        # Initialize RAG with knowledge
        self.rag.initialize_phishing_knowledge()
    
    def analyze_url_with_context(self, url: str) -> Dict[str, Any]:
        """Analyze URL with RAG-enhanced context"""
        # Retrieve relevant context
        context = self.rag.retrieve_relevant_context(f"phishing URL analysis {url}")
        
        # Build enhanced prompt
        context_text = "\n".join(context) if context else ""
        enhanced_prompt = f"""You are PhishGuard AI, an expert cybersecurity assistant specializing in phishing detection.

Relevant context for analysis:
{context_text}

Analyze this URL for phishing threats: {url}

Provide a detailed analysis including:
1. Risk assessment (High/Medium/Low)
2. Specific indicators of suspicion
3. Recommendations for the user
4. Safety tips"""
        
        response = self.client.generate_response(
            self.model_name,
            enhanced_prompt,
            temperature=0.3,
            max_tokens=800
        )
        
        return {
            'url': url,
            'analysis': response,
            'context_used': context,
            'timestamp': datetime.now().isoformat(),
            'model': self.model_name
        }
    
    def analyze_image_for_phishing(self, image_path: Union[str, Path]) -> Dict[str, Any]:
        """Analyze image for phishing-related content"""
        prompt = """Analyze this image for potential phishing or scam content. Look for:

1. Suspicious logos or branding that might be fake
2. Urgent or threatening messages
3. Requests for personal information
4. Suspicious QR codes or links
5. Poor quality graphics that might indicate scams
6. Fake security warnings or alerts
7. Suspicious payment requests or offers

Provide a detailed analysis with risk assessment and recommendations."""

        analysis = self.client.analyze_image(image_path, prompt)
        
        if analysis:
            # Get additional context from RAG
            context = self.rag.retrieve_relevant_context("visual phishing indicators")
            
            return {
                'image_path': str(image_path),
                'analysis': analysis,
                'context_used': context,
                'timestamp': datetime.now().isoformat(),
                'model': self.model_name,
                'analysis_type': 'visual_phishing_detection'
            }
        else:
            return {
                'image_path': str(image_path),
                'error': 'Failed to analyze image',
                'timestamp': datetime.now().isoformat()
            }
    
    def analyze_screenshot(self, screenshot_path: Union[str, Path]) -> Dict[str, Any]:
        """Analyze screenshot for phishing indicators"""
        prompt = """This is a screenshot that might contain phishing content. Analyze it thoroughly for:

1. Suspicious website URLs or domains
2. Fake login forms or data collection
3. Suspicious pop-ups or alerts
4. Fake security warnings
5. Suspicious branding or logos
6. Urgent messages or threats
7. Requests for personal or financial information
8. Suspicious buttons or links

Provide a comprehensive analysis with specific details about what you see and the risk level."""

        analysis = self.client.analyze_image(screenshot_path, prompt)
        
        return {
            'screenshot_path': str(screenshot_path),
            'analysis': analysis,
            'timestamp': datetime.now().isoformat(),
            'model': self.model_name,
            'analysis_type': 'screenshot_analysis'
        }
    
    def combined_analysis(self, url: str = None, image_path: Union[str, Path] = None) -> Dict[str, Any]:
        """Perform combined analysis of URL and image"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'model': self.model_name,
            'analysis_type': 'combined'
        }
        
        if url:
            url_analysis = self.analyze_url_with_context(url)
            results['url_analysis'] = url_analysis
        
        if image_path:
            image_analysis = self.analyze_image_for_phishing(image_path)
            results['image_analysis'] = image_analysis
        
        # Generate combined assessment
        if url and image_path:
            combined_prompt = f"""Based on the following analyses, provide a comprehensive assessment:

URL Analysis: {results.get('url_analysis', {}).get('analysis', 'N/A')}
Image Analysis: {results.get('image_analysis', {}).get('analysis', 'N/A')}

Provide a combined risk assessment and overall recommendation."""

            combined_assessment = self.client.generate_response(
                self.model_name,
                combined_prompt,
                temperature=0.4,
                max_tokens=600
            )
            
            results['combined_assessment'] = combined_assessment
        
        return results

class VisionHaru:
    """Vision-enabled Haru for recovery and education"""
    
    def __init__(self, vision_client: VisionOllamaClient, rag_system: RAGSystem):
        self.client = vision_client
        self.rag = rag_system
        self.model_name = "llava"
    
    def help_with_screenshot(self, screenshot_path: Union[str, Path], situation: str) -> Dict[str, Any]:
        """Help user with a screenshot of a suspicious situation"""
        prompt = f"""You are Haru, a compassionate cybersecurity recovery specialist. 

The user is dealing with this situation: {situation}

Analyze this screenshot and provide:
1. What you see in the image
2. Whether it appears to be a scam or legitimate
3. Immediate steps the user should take
4. Emotional support and reassurance
5. Educational information about this type of threat

Be empathetic and helpful while being informative."""

        analysis = self.client.analyze_image(screenshot_path, prompt)
        
        # Get recovery guidance from RAG
        recovery_context = self.rag.retrieve_relevant_context("recovery steps after phishing")
        
        return {
            'screenshot_path': str(screenshot_path),
            'situation': situation,
            'analysis': analysis,
            'recovery_context': recovery_context,
            'timestamp': datetime.now().isoformat(),
            'model': self.model_name
        }
    
    def educate_with_visuals(self, image_path: Union[str, Path], topic: str) -> Dict[str, Any]:
        """Educate user using visual content"""
        prompt = f"""You are Haru, an educational cybersecurity specialist.

The user wants to learn about: {topic}

Using this image, explain:
1. What the image shows
2. How it relates to cybersecurity
3. What users should be aware of
4. Best practices to stay safe
5. Common mistakes to avoid

Make the explanation clear, engaging, and educational."""

        education = self.client.analyze_image(image_path, prompt)
        
        return {
            'image_path': str(image_path),
            'topic': topic,
            'education': education,
            'timestamp': datetime.now().isoformat(),
            'model': self.model_name
        }

class VisionPhishGuardManager:
    """Manager for vision-enabled PhishGuard system"""
    
    def __init__(self):
        self.vision_client = VisionOllamaClient()
        self.rag_system = RAGSystem()
        self.phishguard_ai = VisionPhishGuardAI(self.vision_client, self.rag_system)
        self.haru = VisionHaru(self.vision_client, self.rag_system)
    
    def setup_vision_system(self) -> bool:
        """Setup the vision-enabled system"""
        logger.info("🚀 Setting up Vision-Enabled PhishGuard AI")
        logger.info("=" * 50)
        
        # Pull LLaVA model
        if not self.vision_client.pull_vision_model():
            logger.error("Failed to pull LLaVA vision model")
            return False
        
        # Test vision capabilities
        logger.info("Testing vision capabilities...")
        
        # Create a simple test image (you can replace this with actual test)
        try:
            # Create a simple test image
            test_image = Image.new('RGB', (100, 100), color='red')
            test_image_path = Path("./test_image.png")
            test_image.save(test_image_path)
            
            # Test image analysis
            result = self.vision_client.analyze_pil_image(
                test_image, 
                "What color is this image?"
            )
            
            if result and "red" in result.lower():
                logger.info("✅ Vision capabilities working correctly")
            else:
                logger.warning("⚠️ Vision test inconclusive")
            
            # Clean up test image
            test_image_path.unlink(missing_ok=True)
            
        except Exception as e:
            logger.warning(f"⚠️ Vision test failed: {e}")
        
        logger.info("✅ Vision system setup completed!")
        return True
    
    def test_system(self) -> Dict[str, bool]:
        """Test all system components"""
        results = {}
        
        # Test vision client
        try:
            models = self.vision_client.list_models()
            results['vision_client'] = any('llava' in model.get('name', '') for model in models)
        except Exception as e:
            logger.error(f"Vision client test failed: {e}")
            results['vision_client'] = False
        
        # Test RAG system
        try:
            test_added = self.rag_system.add_knowledge("Test knowledge entry")
            test_retrieved = self.rag_system.retrieve_relevant_context("test")
            results['rag_system'] = test_added and len(test_retrieved) >= 0
        except Exception as e:
            logger.error(f"RAG system test failed: {e}")
            results['rag_system'] = False
        
        # Test AI components
        try:
            test_result = self.phishguard_ai.analyze_url_with_context("https://example.com")
            results['phishguard_ai'] = test_result is not None
        except Exception as e:
            logger.error(f"PhishGuard AI test failed: {e}")
            results['phishguard_ai'] = False
        
        return results

def main():
    """Main function to setup and test vision system"""
    manager = VisionPhishGuardManager()
    
    # Setup vision system
    if manager.setup_vision_system():
        logger.info("Vision system setup completed")
        
        # Test system
        test_results = manager.test_system()
        logger.info(f"Test results: {test_results}")
        
        # Example usage
        logger.info("Example vision analysis:")
        # You can add example usage here with actual images
        
    else:
        logger.error("Failed to setup vision system")

if __name__ == "__main__":
    main() 
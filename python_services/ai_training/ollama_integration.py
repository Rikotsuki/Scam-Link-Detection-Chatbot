"""
Ollama Integration for PhishGuard AI Training
Handles communication with Ollama and provides interfaces for both chatbots
"""

import requests
import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
import time
from datetime import datetime

from config import phishing_ai_config, haru_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
    
    def list_models(self) -> List[Dict]:
        """List available models in Ollama"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            return response.json().get('models', [])
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
    
    def pull_model(self, model_name: str) -> bool:
        """Pull a model from Ollama"""
        try:
            logger.info(f"Pulling model: {model_name}")
            response = self.session.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name}
            )
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error pulling model {model_name}: {e}")
            return False
    
    def generate_response(self, model_name: str, prompt: str, **kwargs) -> Optional[str]:
        """Generate response from a model"""
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
    
    def create_model(self, model_name: str, modelfile_path: Path) -> bool:
        """Create a custom model from a Modelfile"""
        try:
            logger.info(f"Creating model: {model_name}")
            
            # Read Modelfile
            with open(modelfile_path, 'r') as f:
                modelfile_content = f.read()
            
            # Create model
            response = self.session.post(
                f"{self.base_url}/api/create",
                json={
                    "name": model_name,
                    "modelfile": modelfile_content
                }
            )
            response.raise_for_status()
            
            logger.info(f"Model {model_name} created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error creating model {model_name}: {e}")
            return False

class PhishGuardAI:
    """AI (Phishing Detection) chatbot interface"""
    
    def __init__(self, ollama_client: OllamaClient):
        self.client = ollama_client
        self.model_name = "phishguard-ai"
        self.system_prompt = phishing_ai_config.system_prompt
    
    def analyze_url(self, url: str) -> Dict[str, Any]:
        """Analyze a URL for phishing threats"""
        prompt = f"""<|system|>
{self.system_prompt}

<|user|>
Analyze this URL for phishing threats: {url}

<|assistant|>"""
        
        response = self.client.generate_response(
            self.model_name,
            prompt,
            temperature=0.3,  # Lower temperature for more focused analysis
            max_tokens=500
        )
        
        return {
            'url': url,
            'analysis': response,
            'timestamp': datetime.now().isoformat(),
            'model': self.model_name
        }
    
    def explain_threat(self, url: str, threat_type: str) -> Dict[str, Any]:
        """Explain why a URL is considered a threat"""
        prompt = f"""<|system|>
{self.system_prompt}

<|user|>
Explain why this URL is considered a {threat_type} threat: {url}

<|assistant|>"""
        
        response = self.client.generate_response(
            self.model_name,
            prompt,
            temperature=0.5,
            max_tokens=400
        )
        
        return {
            'url': url,
            'threat_type': threat_type,
            'explanation': response,
            'timestamp': datetime.now().isoformat(),
            'model': self.model_name
        }
    
    def provide_safety_tips(self, context: str = "") -> Dict[str, Any]:
        """Provide safety tips based on context"""
        if context:
            prompt = f"""<|system|>
{self.system_prompt}

<|user|>
Provide safety tips for: {context}

<|assistant|>"""
        else:
            prompt = f"""<|system|>
{self.system_prompt}

<|user|>
What are some general safety tips for avoiding phishing attacks?

<|assistant|>"""
        
        response = self.client.generate_response(
            self.model_name,
            prompt,
            temperature=0.7,
            max_tokens=600
        )
        
        return {
            'context': context,
            'safety_tips': response,
            'timestamp': datetime.now().isoformat(),
            'model': self.model_name
        }

class Haru:
    """Haru (Recovery & Education) chatbot interface"""
    
    def __init__(self, ollama_client: OllamaClient):
        self.client = ollama_client
        self.model_name = "phishguard-haru"
        self.system_prompt = haru_config.system_prompt
    
    def help_victim(self, situation: str) -> Dict[str, Any]:
        """Help a victim of phishing/scam"""
        prompt = f"""<|system|>
{self.system_prompt}

<|user|>
I need help with this situation: {situation}

<|assistant|>"""
        
        response = self.client.generate_response(
            self.model_name,
            prompt,
            temperature=0.8,  # Higher temperature for more empathetic responses
            max_tokens=800
        )
        
        return {
            'situation': situation,
            'guidance': response,
            'timestamp': datetime.now().isoformat(),
            'model': self.model_name
        }
    
    def educate_user(self, topic: str) -> Dict[str, Any]:
        """Educate user about cybersecurity topics"""
        prompt = f"""<|system|>
{self.system_prompt}

<|user|>
Can you teach me about {topic}?

<|assistant|>"""
        
        response = self.client.generate_response(
            self.model_name,
            prompt,
            temperature=0.6,
            max_tokens=700
        )
        
        return {
            'topic': topic,
            'education': response,
            'timestamp': datetime.now().isoformat(),
            'model': self.model_name
        }
    
    def recovery_plan(self, incident_type: str) -> Dict[str, Any]:
        """Create a recovery plan for specific incident types"""
        prompt = f"""<|system|>
{self.system_prompt}

<|user|>
I've been a victim of {incident_type}. What should I do to recover?

<|assistant|>"""
        
        response = self.client.generate_response(
            self.model_name,
            prompt,
            temperature=0.7,
            max_tokens=1000
        )
        
        return {
            'incident_type': incident_type,
            'recovery_plan': response,
            'timestamp': datetime.now().isoformat(),
            'model': self.model_name
        }
    
    def emotional_support(self, user_message: str) -> Dict[str, Any]:
        """Provide emotional support to victims"""
        prompt = f"""<|system|>
{self.system_prompt}

<|user|>
{user_message}

<|assistant|>"""
        
        response = self.client.generate_response(
            self.model_name,
            prompt,
            temperature=0.9,  # Highest temperature for most empathetic responses
            max_tokens=600
        )
        
        return {
            'user_message': user_message,
            'support_response': response,
            'timestamp': datetime.now().isoformat(),
            'model': self.model_name
        }

class ModelfileGenerator:
    """Generate Modelfiles for Ollama models"""
    
    @staticmethod
    def create_ai_modelfile(model_path: Path) -> str:
        """Create Modelfile for AI (Phishing Detection) model"""
        return f"""FROM gemma2:4b

# Set system prompt
SYSTEM """{phishing_ai_config.system_prompt}"""

# Set parameters
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 50
PARAMETER repeat_penalty 1.1

# Set template
TEMPLATE """<|system|>
{{ .System }}

<|user|>
{{ .Prompt }}

<|assistant|>"""

# Add model files
ADAPTER {model_path}"""
    
    @staticmethod
    def create_haru_modelfile(model_path: Path) -> str:
        """Create Modelfile for Haru (Recovery & Education) model"""
        return f"""FROM gemma2:4b

# Set system prompt
SYSTEM """{haru_config.system_prompt}"""

# Set parameters
PARAMETER temperature 0.8
PARAMETER top_p 0.9
PARAMETER top_k 50
PARAMETER repeat_penalty 1.1

# Set template
TEMPLATE """<|system|>
{{ .System }}

<|user|>
{{ .Prompt }}

<|assistant|>"""

# Add model files
ADAPTER {model_path}"""

class PhishGuardOllamaManager:
    """Manager for PhishGuard Ollama integration"""
    
    def __init__(self):
        self.client = OllamaClient()
        self.ai_chatbot = PhishGuardAI(self.client)
        self.haru_chatbot = Haru(self.client)
    
    def setup_models(self) -> bool:
        """Setup both models in Ollama"""
        logger.info("Setting up PhishGuard models in Ollama...")
        
        # Check if base model is available
        models = self.client.list_models()
        base_model_available = any('gemma2:4b' in model.get('name', '') for model in models)
        
        if not base_model_available:
            logger.info("Pulling base Gemma2:4b model...")
            if not self.client.pull_model("gemma2:4b"):
                logger.error("Failed to pull base model")
                return False
        
        # Create AI model
        ai_modelfile_path = phishing_ai_config.model_path / "Modelfile"
        if ai_modelfile_path.exists():
            if not self.client.create_model("phishguard-ai", ai_modelfile_path):
                logger.error("Failed to create AI model")
                return False
        
        # Create Haru model
        haru_modelfile_path = haru_config.model_path / "Modelfile"
        if haru_modelfile_path.exists():
            if not self.client.create_model("phishguard-haru", haru_modelfile_path):
                logger.error("Failed to create Haru model")
                return False
        
        logger.info("All models setup successfully")
        return True
    
    def test_models(self) -> Dict[str, bool]:
        """Test both models"""
        results = {}
        
        # Test AI model
        try:
            test_result = self.ai_chatbot.analyze_url("https://example.com")
            results['ai_model'] = test_result is not None
        except Exception as e:
            logger.error(f"AI model test failed: {e}")
            results['ai_model'] = False
        
        # Test Haru model
        try:
            test_result = self.haru_chatbot.help_victim("I clicked a suspicious link")
            results['haru_model'] = test_result is not None
        except Exception as e:
            logger.error(f"Haru model test failed: {e}")
            results['haru_model'] = False
        
        return results

def main():
    """Main function to setup and test Ollama integration"""
    manager = PhishGuardOllamaManager()
    
    # Setup models
    if manager.setup_models():
        logger.info("Models setup completed")
        
        # Test models
        test_results = manager.test_models()
        logger.info(f"Test results: {test_results}")
        
        # Example usage
        logger.info("Example AI analysis:")
        ai_result = manager.ai_chatbot.analyze_url("https://suspicious-link.com")
        print(json.dumps(ai_result, indent=2))
        
        logger.info("Example Haru help:")
        haru_result = manager.haru_chatbot.help_victim("I think I've been scammed")
        print(json.dumps(haru_result, indent=2))
    else:
        logger.error("Failed to setup models")

if __name__ == "__main__":
    main() 
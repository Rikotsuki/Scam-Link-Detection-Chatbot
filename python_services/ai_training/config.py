"""
Configuration for PhishGuard AI Training System
"""

import os
from pathlib import Path
from typing import Dict, List, Optional

class AITrainingConfig:
    """Configuration for AI training system"""
    
    def __init__(self):
        # Base paths
        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / "data"
        self.models_dir = self.base_dir / "models"
        self.logs_dir = self.base_dir / "logs"
        self.cache_dir = self.base_dir / "cache"
        
        # Create directories
        for dir_path in [self.data_dir, self.models_dir, self.logs_dir, self.cache_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # Ollama configuration
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.gemma_model_name = "gemma2:4b"  # Using Gemma2:4b as base model
        
        # Training configuration
        self.training_config = {
            "max_length": 2048,
            "batch_size": 4,
            "gradient_accumulation_steps": 4,
            "learning_rate": 2e-5,
            "num_train_epochs": 3,
            "warmup_steps": 100,
            "logging_steps": 10,
            "save_steps": 500,
            "eval_steps": 500,
            "save_total_limit": 3,
            "load_best_model_at_end": True,
            "metric_for_best_model": "eval_loss",
            "greater_is_better": False,
        }
        
        # Model configuration
        self.model_config = {
            "max_length": 2048,
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 50,
            "repetition_penalty": 1.1,
        }
        
        # Dataset configuration
        self.dataset_config = {
            "train_split": 0.8,
            "val_split": 0.1,
            "test_split": 0.1,
            "max_samples_per_category": 10000,
        }

class PhishingAIConfig(AITrainingConfig):
    """Configuration for AI (Phishing Detection) chatbot"""
    
    def __init__(self):
        super().__init__()
        
        self.model_name = "phishguard-ai"
        self.model_path = self.models_dir / "phishguard-ai"
        
        # Phishing detection specific training
        self.phishing_training_config = {
            **self.training_config,
            "learning_rate": 1e-5,  # Lower learning rate for fine-tuning
            "num_train_epochs": 5,
            "warmup_ratio": 0.1,
        }
        
        # Phishing detection prompts
        self.system_prompt = """You are PhishGuard AI, an expert cybersecurity assistant specializing in phishing detection and URL analysis. Your role is to:

1. Analyze URLs and identify potential phishing threats
2. Explain why a URL might be suspicious
3. Provide safety recommendations
4. Help users understand cybersecurity risks
5. Educate users about common phishing tactics

Always be helpful, accurate, and prioritize user safety. If you're unsure about something, say so rather than guessing."""

        self.training_prompts = [
            "Analyze this URL for phishing threats: {url}",
            "Is this link safe to click? {url}",
            "What are the red flags in this URL? {url}",
            "How can I protect myself from this type of threat?",
            "Explain why this URL is suspicious: {url}",
        ]

class HaruConfig(AITrainingConfig):
    """Configuration for Haru (Recovery & Education) chatbot"""
    
    def __init__(self):
        super().__init__()
        
        self.model_name = "phishguard-haru"
        self.model_path = self.models_dir / "phishguard-haru"
        
        # Recovery and education specific training
        self.haru_training_config = {
            **self.training_config,
            "learning_rate": 2e-5,  # Slightly higher for educational content
            "num_train_epochs": 4,
            "warmup_ratio": 0.15,
        }
        
        # Haru's personality and role
        self.system_prompt = """You are Haru, a compassionate cybersecurity recovery and education specialist. Your role is to:

1. Help victims of phishing and scams recover from incidents
2. Provide emotional support and guidance
3. Educate users about cybersecurity best practices
4. Explain technical concepts in simple terms
5. Guide users through recovery steps
6. Share educational content about digital safety

Be empathetic, patient, and supportive. Use a warm, friendly tone while being informative and helpful."""

        self.training_prompts = [
            "I think I've been scammed. What should I do?",
            "How can I recover from a phishing attack?",
            "Explain how to protect my accounts after a breach",
            "What are the signs of a phishing email?",
            "How do I report a scam?",
            "Can you teach me about cybersecurity?",
            "I'm worried about my online safety. Help me understand the risks.",
        ]

class DatasetConfig:
    """Configuration for dataset sources and processing"""
    
    def __init__(self):
        # Phishing detection datasets
        self.phishing_datasets = {
            "phishtank": {
                "url": "https://data.phishtank.com/data/online-valid.json",
                "description": "PhishTank verified phishing URLs",
                "format": "json",
                "fields": ["url", "phish_id", "verification_time", "target"]
            },
            "openphish": {
                "url": "https://openphish.com/feed.txt",
                "description": "OpenPhish phishing feed",
                "format": "txt",
                "fields": ["url"]
            },
            "urlhaus": {
                "url": "https://urlhaus.abuse.ch/downloads/csv_recent/",
                "description": "URLhaus malware URLs",
                "format": "csv",
                "fields": ["id", "dateadded", "url", "url_status", "threat", "tags"]
            }
        }
        
        # Educational content sources
        self.educational_sources = {
            "cybersecurity_tips": [
                "https://www.consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams",
                "https://www.ncsc.gov.uk/collection/phishing-scams",
                "https://www.fbi.gov/scams-and-safety/common-scams-and-crimes",
            ],
            "recovery_guides": [
                "https://www.identitytheft.gov/",
                "https://www.consumer.gov/articles/0009-identity-theft",
            ],
            "myanmar_specific": [
                "https://www.cbm.gov.mm/",
                "https://www.myanmar.gov.mm/",
            ]
        }
        
        # Safe URL datasets for negative examples
        self.safe_url_datasets = {
            "alexa_top_sites": "https://s3.amazonaws.com/alexa-static/top-1m.csv.zip",
            "tranco_list": "https://tranco-list.eu/download_daily/1M",
        }

# Global configuration instances
phishing_ai_config = PhishingAIConfig()
haru_config = HaruConfig()
dataset_config = DatasetConfig() 
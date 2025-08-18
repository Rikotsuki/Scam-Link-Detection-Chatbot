#!/usr/bin/env python3
"""
PhishGuard AI Training Script
Complete training pipeline for both AI and Haru chatbots
"""

import os
import sys
import logging
import argparse
from pathlib import Path
from datetime import datetime
import subprocess
import json

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from dataset_collector import DatasetCollector
from model_trainer import train_phishing_ai_model, train_haru_model
from ollama_integration import PhishGuardOllamaManager, ModelfileGenerator
from config import phishing_ai_config, haru_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PhishGuardTrainer:
    """Complete training pipeline for PhishGuard AI models"""
    
    def __init__(self):
        self.collector = DatasetCollector(phishing_ai_config.data_dir)
        self.ollama_manager = PhishGuardOllamaManager()
        
    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met"""
        logger.info("Checking prerequisites...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            logger.error("Python 3.8+ required")
            return False
        
        # Check if Ollama is running
        try:
            models = self.ollama_manager.client.list_models()
            logger.info("✅ Ollama is running")
        except Exception as e:
            logger.error(f"❌ Ollama is not running: {e}")
            logger.info("Please start Ollama: ollama serve")
            return False
        
        # Check if base model is available
        base_model_available = any('gemma2:4b' in model.get('name', '') for model in models)
        if not base_model_available:
            logger.warning("⚠️ Base Gemma2:4b model not found. Will pull during setup.")
        
        # Check disk space (at least 10GB free)
        import shutil
        total, used, free = shutil.disk_usage("/")
        free_gb = free // (1024**3)
        if free_gb < 10:
            logger.error(f"❌ Insufficient disk space. Need at least 10GB, have {free_gb}GB")
            return False
        
        logger.info(f"✅ Disk space available: {free_gb}GB")
        return True
    
    def collect_datasets(self, force: bool = False) -> bool:
        """Collect training datasets"""
        logger.info("Starting dataset collection...")
        
        try:
            # Check if datasets already exist
            processed_dir = phishing_ai_config.data_dir / "processed"
            existing_datasets = list(processed_dir.glob("*.csv"))
            
            if existing_datasets and not force:
                logger.info(f"Found existing datasets: {len(existing_datasets)}")
                logger.info("Use --force to recollect datasets")
                return True
            
            # Collect phishing datasets
            logger.info("Collecting phishing datasets...")
            phishing_data = self.collector.collect_phishing_datasets()
            
            # Collect educational content
            logger.info("Collecting educational content...")
            educational_data = self.collector.collect_educational_content()
            
            # Collect safe URLs
            logger.info("Collecting safe URLs...")
            safe_data = self.collector.collect_safe_urls()
            
            # Create training datasets
            logger.info("Creating training datasets...")
            training_datasets = self.collector.create_training_datasets()
            
            logger.info("✅ Dataset collection completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Dataset collection failed: {e}")
            return False
    
    def train_ai_model(self) -> bool:
        """Train the AI (Phishing Detection) model"""
        logger.info("Training AI (Phishing Detection) model...")
        
        try:
            # Find latest AI dataset
            processed_dir = phishing_ai_config.data_dir / "processed"
            ai_datasets = list(processed_dir.glob("ai_training_dataset_*.csv"))
            
            if not ai_datasets:
                logger.error("❌ No AI training dataset found!")
                return False
            
            # Use the latest dataset
            latest_dataset = max(ai_datasets, key=lambda x: x.stat().st_mtime)
            logger.info(f"Using dataset: {latest_dataset}")
            
            # Train the model
            train_phishing_ai_model(latest_dataset)
            
            logger.info("✅ AI model training completed!")
            return True
            
        except Exception as e:
            logger.error(f"❌ AI model training failed: {e}")
            return False
    
    def train_haru_model(self) -> bool:
        """Train the Haru (Recovery & Education) model"""
        logger.info("Training Haru (Recovery & Education) model...")
        
        try:
            # Find latest Haru dataset
            processed_dir = haru_config.data_dir / "processed"
            haru_datasets = list(processed_dir.glob("haru_training_dataset_*.csv"))
            
            if not haru_datasets:
                logger.error("❌ No Haru training dataset found!")
                return False
            
            # Use the latest dataset
            latest_dataset = max(haru_datasets, key=lambda x: x.stat().st_mtime)
            logger.info(f"Using dataset: {latest_dataset}")
            
            # Train the model
            train_haru_model(latest_dataset)
            
            logger.info("✅ Haru model training completed!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Haru model training failed: {e}")
            return False
    
    def setup_ollama_models(self) -> bool:
        """Setup models in Ollama"""
        logger.info("Setting up models in Ollama...")
        
        try:
            # Generate Modelfiles
            self._generate_modelfiles()
            
            # Setup models in Ollama
            success = self.ollama_manager.setup_models()
            
            if success:
                logger.info("✅ Ollama models setup completed!")
                return True
            else:
                logger.error("❌ Ollama models setup failed!")
                return False
                
        except Exception as e:
            logger.error(f"❌ Ollama setup failed: {e}")
            return False
    
    def _generate_modelfiles(self):
        """Generate Modelfiles for both models"""
        logger.info("Generating Modelfiles...")
        
        # Generate AI Modelfile
        ai_modelfile_content = ModelfileGenerator.create_ai_modelfile(
            phishing_ai_config.model_path
        )
        ai_modelfile_path = phishing_ai_config.model_path / "Modelfile"
        with open(ai_modelfile_path, 'w') as f:
            f.write(ai_modelfile_content)
        
        # Generate Haru Modelfile
        haru_modelfile_content = ModelfileGenerator.create_haru_modelfile(
            haru_config.model_path
        )
        haru_modelfile_path = haru_config.model_path / "Modelfile"
        with open(haru_modelfile_path, 'w') as f:
            f.write(haru_modelfile_content)
        
        logger.info("✅ Modelfiles generated!")
    
    def test_models(self) -> bool:
        """Test the trained models"""
        logger.info("Testing trained models...")
        
        try:
            test_results = self.ollama_manager.test_models()
            
            if test_results.get('ai_model', False):
                logger.info("✅ AI model test passed!")
            else:
                logger.error("❌ AI model test failed!")
            
            if test_results.get('haru_model', False):
                logger.info("✅ Haru model test passed!")
            else:
                logger.error("❌ Haru model test failed!")
            
            return all(test_results.values())
            
        except Exception as e:
            logger.error(f"❌ Model testing failed: {e}")
            return False
    
    def run_complete_pipeline(self, force_collect: bool = False) -> bool:
        """Run the complete training pipeline"""
        logger.info("🚀 Starting PhishGuard AI Training Pipeline")
        logger.info("=" * 50)
        
        # Step 1: Check prerequisites
        if not self.check_prerequisites():
            return False
        
        # Step 2: Collect datasets
        if not self.collect_datasets(force=force_collect):
            return False
        
        # Step 3: Train AI model
        if not self.train_ai_model():
            return False
        
        # Step 4: Train Haru model
        if not self.train_haru_model():
            return False
        
        # Step 5: Setup Ollama models
        if not self.setup_ollama_models():
            return False
        
        # Step 6: Test models
        if not self.test_models():
            return False
        
        logger.info("=" * 50)
        logger.info("🎉 PhishGuard AI Training Pipeline Completed Successfully!")
        logger.info("Your models are ready to use!")
        
        return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="PhishGuard AI Training Pipeline")
    parser.add_argument(
        "--step",
        choices=["collect", "train-ai", "train-haru", "setup-ollama", "test", "all"],
        default="all",
        help="Training step to run"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force dataset collection even if datasets exist"
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check prerequisites"
    )
    
    args = parser.parse_args()
    
    trainer = PhishGuardTrainer()
    
    if args.check_only:
        success = trainer.check_prerequisites()
        sys.exit(0 if success else 1)
    
    if args.step == "all":
        success = trainer.run_complete_pipeline(force_collect=args.force)
    elif args.step == "collect":
        success = trainer.collect_datasets(force=args.force)
    elif args.step == "train-ai":
        success = trainer.train_ai_model()
    elif args.step == "train-haru":
        success = trainer.train_haru_model()
    elif args.step == "setup-ollama":
        success = trainer.setup_ollama_models()
    elif args.step == "test":
        success = trainer.test_models()
    else:
        logger.error(f"Unknown step: {args.step}")
        sys.exit(1)
    
    if success:
        logger.info("✅ Operation completed successfully!")
        sys.exit(0)
    else:
        logger.error("❌ Operation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 
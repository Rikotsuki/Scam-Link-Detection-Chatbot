"""
Model Trainer for PhishGuard AI Training
Fine-tunes Gemma3:4b for both AI (phishing detection) and Haru (recovery/education) chatbots
"""

import os
import json
import logging
import torch
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import wandb
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    TrainingArguments, 
    Trainer,
    DataCollatorForLanguageModeling,
    EarlyStoppingCallback
)
from peft import (
    LoraConfig, 
    get_peft_model, 
    TaskType,
    prepare_model_for_kbit_training
)
from datasets import Dataset
import numpy as np
from sklearn.model_selection import train_test_split

from config import phishing_ai_config, haru_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelTrainer:
    """Trains fine-tuned models for both chatbots"""
    
    def __init__(self, config, model_name: str):
        self.config = config
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        logger.info(f"Using device: {self.device}")
        logger.info(f"Training model: {model_name}")
        
        # Initialize wandb for experiment tracking
        if os.getenv("WANDB_API_KEY"):
            wandb.init(project="phishguard-ai", name=model_name)
        
        # Load base model and tokenizer
        self.tokenizer = None
        self.model = None
        self._load_base_model()
    
    def _load_base_model(self):
        """Load the base Gemma model and tokenizer"""
        try:
            logger.info("Loading base Gemma model...")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                "google/gemma-2b",  # Using Gemma-2b as base (more manageable for fine-tuning)
                trust_remote_code=True,
                padding_side="right"
            )
            
            # Add padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                "google/gemma-2b",
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True,
                load_in_8bit=True  # Use 8-bit quantization for memory efficiency
            )
            
            # Prepare model for training
            self.model = prepare_model_for_kbit_training(self.model)
            
            logger.info("Base model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading base model: {e}")
            raise
    
    def prepare_dataset(self, dataset_path: Path) -> Tuple[Dataset, Dataset]:
        """Prepare dataset for training"""
        logger.info(f"Loading dataset from {dataset_path}")
        
        # Load CSV dataset
        df = pd.read_csv(dataset_path)
        
        # Create training and validation splits
        train_df, val_df = train_test_split(
            df, 
            test_size=0.1, 
            random_state=42,
            stratify=df['category'] if 'category' in df.columns else None
        )
        
        # Format data for instruction tuning
        train_data = self._format_instruction_data(train_df)
        val_data = self._format_instruction_data(val_df)
        
        # Convert to HuggingFace datasets
        train_dataset = Dataset.from_list(train_data)
        val_dataset = Dataset.from_list(val_data)
        
        logger.info(f"Prepared {len(train_dataset)} training samples and {len(val_dataset)} validation samples")
        
        return train_dataset, val_dataset
    
    def _format_instruction_data(self, df: pd.DataFrame) -> List[Dict]:
        """Format data for instruction tuning"""
        formatted_data = []
        
        for _, row in df.iterrows():
            # Create instruction format
            if self.model_name == "phishguard-ai":
                # For AI chatbot - focus on URL analysis
                instruction = row['instruction']
                response = row['output']
                
                # Create system prompt + instruction format
                formatted_text = f"""<|system|>
{self.config.system_prompt}
<|user|>
{instruction}
<|assistant|>
{response}
<|endoftext|>"""
                
            else:  # Haru chatbot
                # For Haru chatbot - focus on recovery and education
                instruction = row['instruction']
                response = row['output']
                
                formatted_text = f"""<|system|>
{self.config.system_prompt}
<|user|>
{instruction}
<|assistant|>
{response}
<|endoftext|>"""
            
            formatted_data.append({
                'text': formatted_text,
                'instruction': instruction,
                'response': response,
                'category': row.get('category', 'general')
            })
        
        return formatted_data
    
    def tokenize_function(self, examples):
        """Tokenize the examples"""
        return self.tokenizer(
            examples['text'],
            truncation=True,
            padding=True,
            max_length=self.config.training_config['max_length'],
            return_tensors="pt"
        )
    
    def setup_lora_config(self) -> LoraConfig:
        """Setup LoRA configuration for efficient fine-tuning"""
        return LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            inference_mode=False,
            r=16,  # Rank
            lora_alpha=32,  # Alpha parameter
            lora_dropout=0.1,  # Dropout
            target_modules=[
                "q_proj",
                "v_proj",
                "k_proj",
                "o_proj",
                "gate_proj",
                "up_proj",
                "down_proj",
            ]
        )
    
    def train_model(self, train_dataset: Dataset, val_dataset: Dataset):
        """Train the fine-tuned model"""
        logger.info("Starting model training...")
        
        # Apply LoRA configuration
        lora_config = self.setup_lora_config()
        self.model = get_peft_model(self.model, lora_config)
        
        # Print trainable parameters
        self.model.print_trainable_parameters()
        
        # Setup training arguments
        training_args = TrainingArguments(
            output_dir=self.config.model_path,
            num_train_epochs=self.config.training_config['num_train_epochs'],
            per_device_train_batch_size=self.config.training_config['batch_size'],
            per_device_eval_batch_size=self.config.training_config['batch_size'],
            gradient_accumulation_steps=self.config.training_config['gradient_accumulation_steps'],
            learning_rate=self.config.training_config['learning_rate'],
            warmup_steps=self.config.training_config['warmup_steps'],
            logging_steps=self.config.training_config['logging_steps'],
            save_steps=self.config.training_config['save_steps'],
            eval_steps=self.config.training_config['eval_steps'],
            evaluation_strategy="steps",
            save_strategy="steps",
            save_total_limit=self.config.training_config['save_total_limit'],
            load_best_model_at_end=self.config.training_config['load_best_model_at_end'],
            metric_for_best_model=self.config.training_config['metric_for_best_model'],
            greater_is_better=self.config.training_config['greater_is_better'],
            fp16=True,
            report_to="wandb" if os.getenv("WANDB_API_KEY") else None,
            remove_unused_columns=False,
            dataloader_pin_memory=False,
        )
        
        # Setup data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False,
        )
        
        # Setup trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            data_collator=data_collator,
            tokenizer=self.tokenizer,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
        )
        
        # Train the model
        logger.info("Starting training...")
        trainer.train()
        
        # Save the model
        logger.info("Saving model...")
        trainer.save_model()
        self.tokenizer.save_pretrained(self.config.model_path)
        
        # Save training configuration
        self._save_training_config()
        
        logger.info(f"Training completed! Model saved to {self.config.model_path}")
        
        return trainer
    
    def _save_training_config(self):
        """Save training configuration"""
        config_data = {
            'model_name': self.model_name,
            'base_model': 'google/gemma-2b',
            'training_config': self.config.training_config,
            'model_config': self.config.model_config,
            'system_prompt': self.config.system_prompt,
            'training_date': datetime.now().isoformat(),
            'device': self.device,
        }
        
        config_path = self.config.model_path / 'training_config.json'
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=2)
    
    def evaluate_model(self, test_dataset: Dataset) -> Dict:
        """Evaluate the trained model"""
        logger.info("Evaluating model...")
        
        # Load the trained model
        model = AutoModelForCausalLM.from_pretrained(
            self.config.model_path,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
        
        tokenizer = AutoTokenizer.from_pretrained(self.config.model_path)
        
        # Generate responses for test samples
        results = []
        
        for i, example in enumerate(test_dataset):
            if i >= 10:  # Evaluate first 10 examples
                break
                
            # Prepare input
            input_text = example['instruction']
            expected_output = example['response']
            
            # Generate response
            inputs = tokenizer(
                input_text, 
                return_tensors="pt", 
                truncation=True, 
                max_length=512
            ).to(self.device)
            
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_length=512,
                    temperature=self.config.model_config['temperature'],
                    top_p=self.config.model_config['top_p'],
                    top_k=self.config.model_config['top_k'],
                    repetition_penalty=self.config.model_config['repetition_penalty'],
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            results.append({
                'input': input_text,
                'expected': expected_output,
                'generated': generated_text,
                'category': example.get('category', 'general')
            })
        
        # Save evaluation results
        eval_path = self.config.model_path / 'evaluation_results.json'
        with open(eval_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Evaluation completed. Results saved to {eval_path}")
        
        return results

class PhishingAITrainer(ModelTrainer):
    """Trainer specifically for AI (Phishing Detection) chatbot"""
    
    def __init__(self):
        super().__init__(phishing_ai_config, "phishguard-ai")
    
    def _format_instruction_data(self, df: pd.DataFrame) -> List[Dict]:
        """Format data specifically for phishing detection"""
        formatted_data = []
        
        for _, row in df.iterrows():
            instruction = row['instruction']
            response = row['output']
            
            # Create phishing detection specific format
            formatted_text = f"""<|system|>
You are PhishGuard AI, an expert cybersecurity assistant specializing in phishing detection and URL analysis. Your role is to analyze URLs and identify potential phishing threats, explain why a URL might be suspicious, and provide safety recommendations.

<|user|>
{instruction}

<|assistant|>
{response}

<|endoftext|>"""
            
            formatted_data.append({
                'text': formatted_text,
                'instruction': instruction,
                'response': response,
                'category': row.get('category', 'phishing_detection')
            })
        
        return formatted_data

class HaruTrainer(ModelTrainer):
    """Trainer specifically for Haru (Recovery & Education) chatbot"""
    
    def __init__(self):
        super().__init__(haru_config, "phishguard-haru")
    
    def _format_instruction_data(self, df: pd.DataFrame) -> List[Dict]:
        """Format data specifically for recovery and education"""
        formatted_data = []
        
        for _, row in df.iterrows():
            instruction = row['instruction']
            response = row['output']
            
            # Create recovery and education specific format
            formatted_text = f"""<|system|>
You are Haru, a compassionate cybersecurity recovery and education specialist. Your role is to help victims of phishing and scams recover from incidents, provide emotional support and guidance, educate users about cybersecurity best practices, and explain technical concepts in simple terms.

<|user|>
{instruction}

<|assistant|>
{response}

<|endoftext|>"""
            
            formatted_data.append({
                'text': formatted_text,
                'instruction': instruction,
                'response': response,
                'category': row.get('category', 'recovery_education')
            })
        
        return formatted_data

def train_phishing_ai_model(dataset_path: Path):
    """Train the AI (Phishing Detection) model"""
    logger.info("Training PhishGuard AI model...")
    
    trainer = PhishingAITrainer()
    
    # Prepare dataset
    train_dataset, val_dataset = trainer.prepare_dataset(dataset_path)
    
    # Train model
    trainer.train_model(train_dataset, val_dataset)
    
    logger.info("PhishGuard AI model training completed!")

def train_haru_model(dataset_path: Path):
    """Train the Haru (Recovery & Education) model"""
    logger.info("Training Haru model...")
    
    trainer = HaruTrainer()
    
    # Prepare dataset
    train_dataset, val_dataset = trainer.prepare_dataset(dataset_path)
    
    # Train model
    trainer.train_model(train_dataset, val_dataset)
    
    logger.info("Haru model training completed!")

def main():
    """Main function to train both models"""
    from config import phishing_ai_config, haru_config
    
    # Find latest datasets
    processed_dir = phishing_ai_config.data_dir / "processed"
    
    ai_dataset_path = None
    haru_dataset_path = None
    
    # Find AI dataset
    for file_path in processed_dir.glob("ai_training_dataset_*.csv"):
        if ai_dataset_path is None or file_path.stat().st_mtime > ai_dataset_path.stat().st_mtime:
            ai_dataset_path = file_path
    
    # Find Haru dataset
    for file_path in processed_dir.glob("haru_training_dataset_*.csv"):
        if haru_dataset_path is None or file_path.stat().st_mtime > haru_dataset_path.stat().st_mtime:
            haru_dataset_path = file_path
    
    if ai_dataset_path and ai_dataset_path.exists():
        logger.info(f"Training AI model with dataset: {ai_dataset_path}")
        train_phishing_ai_model(ai_dataset_path)
    else:
        logger.error("AI training dataset not found!")
    
    if haru_dataset_path and haru_dataset_path.exists():
        logger.info(f"Training Haru model with dataset: {haru_dataset_path}")
        train_haru_model(haru_dataset_path)
    else:
        logger.error("Haru training dataset not found!")

if __name__ == "__main__":
    main() 
"""
Advanced Model Trainer for PhishGuard AI Training
Updated for LangChain 0.3+ and latest best practices
"""

import os
import json
import logging
import torch
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import wandb
import asyncio
from dataclasses import dataclass

# Latest transformers and training libraries
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    TrainingArguments, 
    Trainer,
    DataCollatorForLanguageModeling,
    EarlyStoppingCallback,
    BitsAndBytesConfig,
    AutoConfig
)
from peft import (
    LoraConfig, 
    get_peft_model, 
    TaskType,
    prepare_model_for_kbit_training,
    PeftModel
)
from datasets import Dataset, load_dataset
import numpy as np
from sklearn.model_selection import train_test_split

# LangChain 0.3+ imports
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Performance optimization
import bitsandbytes as bnb
from accelerate import Accelerator

from config import phishing_ai_config, haru_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TrainingConfig:
    """Advanced training configuration"""
    model_name: str
    base_model: str = "google/gemma-2b"
    max_length: int = 2048
    batch_size: int = 4
    gradient_accumulation_steps: int = 4
    learning_rate: float = 2e-5
    num_train_epochs: int = 3
    warmup_ratio: float = 0.1
    logging_steps: int = 10
    save_steps: int = 500
    eval_steps: int = 500
    save_total_limit: int = 3
    load_best_model_at_end: bool = True
    metric_for_best_model: str = "eval_loss"
    greater_is_better: bool = False
    fp16: bool = True
    bf16: bool = False
    load_in_8bit: bool = True
    load_in_4bit: bool = False
    use_flash_attention: bool = True
    gradient_checkpointing: bool = True
    dataloader_pin_memory: bool = False
    remove_unused_columns: bool = False

class AdvancedModelTrainer:
    """Advanced model trainer with latest techniques"""
    
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.accelerator = Accelerator()
        
        logger.info(f"Using device: {self.device}")
        logger.info(f"Training model: {config.model_name}")
        
        # Initialize wandb for experiment tracking
        if os.getenv("WANDB_API_KEY"):
            wandb.init(
                project="phishguard-ai", 
                name=config.model_name,
                config=vars(config)
            )
        
        # Load base model and tokenizer
        self.tokenizer = None
        self.model = None
        self._load_base_model()
    
    def _load_base_model(self):
        """Load the base model with advanced optimizations"""
        try:
            logger.info("Loading base model with optimizations...")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.config.base_model,
                trust_remote_code=True,
                padding_side="right"
            )
            
            # Add padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Configure quantization
            quantization_config = None
            if self.config.load_in_4bit:
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_use_double_quant=True,
                )
            elif self.config.load_in_8bit:
                quantization_config = BitsAndBytesConfig(
                    load_in_8bit=True,
                    llm_int8_threshold=6.0,
                    llm_int8_has_fp16_weight=False,
                )
            
            # Load model with optimizations
            model_kwargs = {
                "torch_dtype": torch.float16,
                "device_map": "auto",
                "trust_remote_code": True,
            }
            
            if quantization_config:
                model_kwargs["quantization_config"] = quantization_config
            
            if self.config.use_flash_attention:
                model_kwargs["attn_implementation"] = "flash_attention_2"
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.base_model,
                **model_kwargs
            )
            
            # Prepare model for training
            if quantization_config:
                self.model = prepare_model_for_kbit_training(self.model)
            
            # Enable gradient checkpointing for memory efficiency
            if self.config.gradient_checkpointing:
                self.model.gradient_checkpointing_enable()
            
            logger.info("Base model loaded successfully with optimizations")
            
        except Exception as e:
            logger.error(f"Error loading base model: {e}")
            raise
    
    def setup_lora_config(self) -> LoraConfig:
        """Setup advanced LoRA configuration"""
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
            ],
            bias="none",
            use_rslora=True,  # Use RSLoRA for better performance
            init_lora_weights=True,
        )
    
    def prepare_advanced_dataset(self, dataset_path: Path) -> Tuple[Dataset, Dataset]:
        """Prepare dataset with advanced preprocessing"""
        logger.info(f"Loading dataset from {dataset_path}")
        
        # Load CSV dataset
        df = pd.read_csv(dataset_path)
        
        # Advanced data preprocessing
        df = self._preprocess_dataset(df)
        
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
    
    def _preprocess_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        """Advanced dataset preprocessing"""
        # Remove duplicates
        df = df.drop_duplicates(subset=['instruction', 'output'])
        
        # Filter out very short or very long responses
        df = df[df['output'].str.len() > 10]
        df = df[df['output'].str.len() < 2000]
        
        # Balance dataset if needed
        if 'category' in df.columns:
            category_counts = df['category'].value_counts()
            min_count = category_counts.min()
            if category_counts.max() > min_count * 2:  # If imbalance > 2x
                df = df.groupby('category').apply(
                    lambda x: x.sample(n=min(len(x), min_count * 2))
                ).reset_index(drop=True)
        
        return df
    
    def _format_instruction_data(self, df: pd.DataFrame) -> List[Dict]:
        """Format data for advanced instruction tuning"""
        formatted_data = []
        
        for _, row in df.iterrows():
            instruction = row['instruction']
            response = row['output']
            
            # Create advanced instruction format
            if self.config.model_name == "phishguard-ai":
                formatted_text = self._create_ai_prompt(instruction, response)
            else:  # Haru
                formatted_text = self._create_haru_prompt(instruction, response)
            
            formatted_data.append({
                'text': formatted_text,
                'instruction': instruction,
                'response': response,
                'category': row.get('category', 'general')
            })
        
        return formatted_data
    
    def _create_ai_prompt(self, instruction: str, response: str) -> str:
        """Create AI (Phishing Detection) prompt"""
        return f"""<|system|>
You are PhishGuard AI, an expert cybersecurity assistant specializing in phishing detection and URL analysis. Your role is to analyze URLs and identify potential phishing threats, explain why a URL might be suspicious, and provide safety recommendations.

Always be helpful, accurate, and prioritize user safety. If you're unsure about something, say so rather than guessing.

<|user|>
{instruction}

<|assistant|>
{response}

<|endoftext|>"""
    
    def _create_haru_prompt(self, instruction: str, response: str) -> str:
        """Create Haru (Recovery & Education) prompt"""
        return f"""<|system|>
You are Haru, a compassionate cybersecurity recovery and education specialist. Your role is to help victims of phishing and scams recover from incidents, provide emotional support and guidance, educate users about cybersecurity best practices, and explain technical concepts in simple terms.

Be empathetic, patient, and supportive. Use a warm, friendly tone while being informative and helpful.

<|user|>
{instruction}

<|assistant|>
{response}

<|endoftext|>"""
    
    def tokenize_function(self, examples):
        """Advanced tokenization function"""
        return self.tokenizer(
            examples['text'],
            truncation=True,
            padding=True,
            max_length=self.config.max_length,
            return_tensors="pt"
        )
    
    def train_model(self, train_dataset: Dataset, val_dataset: Dataset) -> Trainer:
        """Train the model with advanced techniques"""
        logger.info("Starting advanced model training...")
        
        # Apply LoRA configuration
        lora_config = self.setup_lora_config()
        self.model = get_peft_model(self.model, lora_config)
        
        # Print trainable parameters
        self.model.print_trainable_parameters()
        
        # Setup advanced training arguments
        training_args = TrainingArguments(
            output_dir=self.config.model_name,
            num_train_epochs=self.config.num_train_epochs,
            per_device_train_batch_size=self.config.batch_size,
            per_device_eval_batch_size=self.config.batch_size,
            gradient_accumulation_steps=self.config.gradient_accumulation_steps,
            learning_rate=self.config.learning_rate,
            warmup_ratio=self.config.warmup_ratio,
            logging_steps=self.config.logging_steps,
            save_steps=self.config.save_steps,
            eval_steps=self.config.eval_steps,
            evaluation_strategy="steps",
            save_strategy="steps",
            save_total_limit=self.config.save_total_limit,
            load_best_model_at_end=self.config.load_best_model_at_end,
            metric_for_best_model=self.config.metric_for_best_model,
            greater_is_better=self.config.greater_is_better,
            fp16=self.config.fp16,
            bf16=self.config.bf16,
            report_to="wandb" if os.getenv("WANDB_API_KEY") else None,
            remove_unused_columns=self.config.remove_unused_columns,
            dataloader_pin_memory=self.config.dataloader_pin_memory,
            gradient_checkpointing=self.config.gradient_checkpointing,
            optim="adamw_torch",
            lr_scheduler_type="cosine",
            weight_decay=0.01,
            max_grad_norm=1.0,
            dataloader_num_workers=4,
            group_by_length=True,  # Group similar length sequences
        )
        
        # Setup data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False,
        )
        
        # Setup trainer with advanced callbacks
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            data_collator=data_collator,
            tokenizer=self.tokenizer,
            callbacks=[
                EarlyStoppingCallback(early_stopping_patience=3),
            ]
        )
        
        # Train the model
        logger.info("Starting training...")
        trainer.train()
        
        # Save the model
        logger.info("Saving model...")
        trainer.save_model()
        self.tokenizer.save_pretrained(self.config.model_name)
        
        # Save training configuration
        self._save_training_config()
        
        logger.info(f"Training completed! Model saved to {self.config.model_name}")
        
        return trainer
    
    def _save_training_config(self):
        """Save training configuration"""
        config_data = {
            'model_name': self.config.model_name,
            'base_model': self.config.base_model,
            'training_config': vars(self.config),
            'training_date': datetime.now().isoformat(),
            'device': self.device,
        }
        
        config_path = Path(self.config.model_name) / 'training_config.json'
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=2)
    
    def evaluate_model(self, test_dataset: Dataset) -> Dict[str, Any]:
        """Advanced model evaluation"""
        logger.info("Evaluating model...")
        
        # Load the trained model
        model = AutoModelForCausalLM.from_pretrained(
            self.config.model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
        
        tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)
        
        # Generate responses for test samples
        results = []
        metrics = {
            'total_samples': 0,
            'successful_generations': 0,
            'average_response_length': 0,
            'response_times': []
        }
        
        for i, example in enumerate(test_dataset):
            if i >= 20:  # Evaluate first 20 examples
                break
                
            start_time = datetime.now()
            
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
                    temperature=0.7,
                    top_p=0.9,
                    top_k=50,
                    repetition_penalty=1.1,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            response_time = (datetime.now() - start_time).total_seconds()
            
            # Calculate metrics
            metrics['total_samples'] += 1
            if generated_text.strip():
                metrics['successful_generations'] += 1
                metrics['average_response_length'] += len(generated_text)
                metrics['response_times'].append(response_time)
            
            results.append({
                'input': input_text,
                'expected': expected_output,
                'generated': generated_text,
                'category': example.get('category', 'general'),
                'response_time': response_time
            })
        
        # Calculate final metrics
        if metrics['successful_generations'] > 0:
            metrics['average_response_length'] /= metrics['successful_generations']
            metrics['average_response_time'] = np.mean(metrics['response_times'])
            metrics['success_rate'] = metrics['successful_generations'] / metrics['total_samples']
        
        # Save evaluation results
        eval_path = Path(self.config.model_name) / 'evaluation_results.json'
        with open(eval_path, 'w') as f:
            json.dump({
                'results': results,
                'metrics': metrics
            }, f, indent=2)
        
        logger.info(f"Evaluation completed. Results saved to {eval_path}")
        logger.info(f"Success rate: {metrics.get('success_rate', 0):.2%}")
        logger.info(f"Average response time: {metrics.get('average_response_time', 0):.2f}s")
        
        return metrics

class LangChainIntegration:
    """LangChain 0.3+ integration for advanced features"""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.llm = Ollama(model=model_name)
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    def create_rag_chain(self, knowledge_base_path: str):
        """Create RAG chain with LangChain 0.3+"""
        # Load knowledge base
        with open(knowledge_base_path, 'r') as f:
            knowledge_base = f.read()
        
        # Split text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_text(knowledge_base)
        
        # Create vector store
        vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=self.embeddings
        )
        
        # Create RAG chain
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        
        template = """Answer the question based on the following context:

Context: {context}

Question: {question}

Answer:"""
        
        prompt = PromptTemplate.from_template(template)
        
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        return chain
    
    async def async_generate(self, prompt: str) -> str:
        """Async generation with LangChain"""
        return await self.llm.ainvoke(prompt)

def train_phishing_ai_advanced(dataset_path: Path):
    """Train AI model with advanced techniques"""
    config = TrainingConfig(
        model_name="phishguard-ai-advanced",
        base_model="google/gemma-2b",
        batch_size=2,  # Smaller batch size for memory efficiency
        gradient_accumulation_steps=8,
        learning_rate=1e-5,
        num_train_epochs=5,
        load_in_8bit=True,
        use_flash_attention=True,
        gradient_checkpointing=True
    )
    
    trainer = AdvancedModelTrainer(config)
    train_dataset, val_dataset = trainer.prepare_advanced_dataset(dataset_path)
    trainer.train_model(train_dataset, val_dataset)
    
    # Evaluate model
    test_dataset = val_dataset  # Use validation as test for now
    metrics = trainer.evaluate_model(test_dataset)
    
    return trainer, metrics

def train_haru_advanced(dataset_path: Path):
    """Train Haru model with advanced techniques"""
    config = TrainingConfig(
        model_name="phishguard-haru-advanced",
        base_model="google/gemma-2b",
        batch_size=2,
        gradient_accumulation_steps=8,
        learning_rate=2e-5,
        num_train_epochs=4,
        load_in_8bit=True,
        use_flash_attention=True,
        gradient_checkpointing=True
    )
    
    trainer = AdvancedModelTrainer(config)
    train_dataset, val_dataset = trainer.prepare_advanced_dataset(dataset_path)
    trainer.train_model(train_dataset, val_dataset)
    
    # Evaluate model
    test_dataset = val_dataset
    metrics = trainer.evaluate_model(test_dataset)
    
    return trainer, metrics

def main():
    """Main function for advanced training"""
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
        trainer, metrics = train_phishing_ai_advanced(ai_dataset_path)
        logger.info(f"AI training completed with metrics: {metrics}")
    else:
        logger.error("AI training dataset not found!")
    
    if haru_dataset_path and haru_dataset_path.exists():
        logger.info(f"Training Haru model with dataset: {haru_dataset_path}")
        trainer, metrics = train_haru_advanced(haru_dataset_path)
        logger.info(f"Haru training completed with metrics: {metrics}")
    else:
        logger.error("Haru training dataset not found!")

if __name__ == "__main__":
    main() 
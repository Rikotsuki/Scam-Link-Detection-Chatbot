# Complete Training Guide for PhishGuard AI Models

This guide provides step-by-step instructions for training both AI (Phishing Detection) and Haru (Recovery & Education) chatbots using the latest techniques and best practices.

## 🎯 Overview

You'll be training two specialized models:
1. **AI (Phishing Detection)** - Expert cybersecurity assistant
2. **Haru (Recovery & Education)** - Compassionate recovery specialist

## 📋 Prerequisites

### System Requirements
- **RAM**: Minimum 16GB, Recommended 32GB+
- **Storage**: At least 20GB free space
- **GPU**: NVIDIA GPU with 8GB+ VRAM (recommended)
- **Python**: 3.8 or higher
- **Ollama**: Latest version

### Software Setup
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Verify installation
ollama --version
```

## 🚀 Step-by-Step Training Process

### Step 1: Environment Setup

#### 1.1 Create Virtual Environment
```bash
cd ai_training
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

#### 1.2 Install Dependencies
```bash
# Install with latest versions
pip install -r requirements.txt

# Install additional tools for GPU support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

#### 1.3 Verify Installation
```bash
# Check CUDA availability
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"

# Check GPU memory
python -c "import torch; print(f'GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB')"
```

### Step 2: Dataset Collection

#### 2.1 Run Automated Collection
```bash
# Collect all datasets
python train_models.py --step collect

# Or collect individually
python dataset_collector.py
```

#### 2.2 Manual Dataset Enhancement
```python
# Add Myanmar-specific data
myanmar_data = [
    {
        'url': 'https://fake-kbz-verify.com',
        'description': 'KBZ Bank impersonation scam',
        'source': 'manual',
        'category': 'banking_scam'
    },
    # Add more local scam patterns
]

# Save to dataset
import json
with open('data/phishing/myanmar_scams.json', 'w') as f:
    json.dump(myanmar_data, f, indent=2)
```

#### 2.3 Verify Dataset Quality
```bash
# Check dataset statistics
python -c "
import pandas as pd
df = pd.read_csv('data/processed/ai_training_dataset_*.csv')
print(f'Total samples: {len(df)}')
print(f'Categories: {df[\"category\"].value_counts()}')
"
```

### Step 3: Model Training

#### 3.1 Basic Training (Recommended for First Run)
```bash
# Train AI model
python train_models.py --step train-ai

# Train Haru model
python train_models.py --step train-haru
```

#### 3.2 Advanced Training (For Better Performance)
```bash
# Use advanced trainer with optimizations
python advanced_model_trainer.py
```

#### 3.3 Training Configuration

Edit `config.py` for custom training:

```python
# For low memory systems
training_config = {
    "batch_size": 1,
    "gradient_accumulation_steps": 16,
    "load_in_8bit": True,
    "gradient_checkpointing": True,
}

# For high performance systems
training_config = {
    "batch_size": 8,
    "gradient_accumulation_steps": 2,
    "load_in_4bit": True,
    "use_flash_attention": True,
}
```

### Step 4: Model Evaluation

#### 4.1 Run Evaluation
```bash
# Evaluate trained models
python train_models.py --step test

# Detailed evaluation
python advanced_model_trainer.py --evaluate
```

#### 4.2 Check Training Metrics
```bash
# View training logs
tail -f logs/training.log

# Check model performance
python -c "
import json
with open('models/phishguard-ai/evaluation_results.json') as f:
    results = json.load(f)
print(f'Success rate: {results[\"metrics\"][\"success_rate\"]:.2%}')
"
```

### Step 5: Ollama Integration

#### 5.1 Setup Ollama Models
```bash
# Create custom models in Ollama
python train_models.py --step setup-ollama

# Or manually
ollama create phishguard-ai -f models/phishguard-ai/Modelfile
ollama create phishguard-haru -f models/phishguard-haru/Modelfile
```

#### 5.2 Test Ollama Models
```bash
# Test AI model
ollama run phishguard-ai "Analyze this URL: https://suspicious-link.com"

# Test Haru model
ollama run phishguard-haru "I think I've been scammed, what should I do?"
```

## 🔧 Advanced Training Techniques

### 1. Hyperparameter Optimization

#### 1.1 Learning Rate Scheduling
```python
# Cosine annealing with warmup
training_args = TrainingArguments(
    learning_rate=2e-5,
    lr_scheduler_type="cosine",
    warmup_ratio=0.1,
    weight_decay=0.01,
)
```

#### 1.2 Gradient Accumulation
```python
# For memory efficiency
training_args = TrainingArguments(
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    gradient_checkpointing=True,
)
```

### 2. Data Augmentation

#### 2.1 Text Augmentation
```python
import nlpaug.augmenter.word as naw
import nlpaug.augmenter.sentence as nas

def augment_training_data(texts):
    # Synonym replacement
    aug = naw.SynonymAug(aug_src='wordnet')
    augmented = aug.augment(texts)
    
    # Back translation
    back_translation_aug = naw.BackTranslationAug(
        from_model_name='facebook/wmt19-en-de',
        to_model_name='facebook/wmt19-de-en'
    )
    augmented += back_translation_aug.augment(texts)
    
    return augmented
```

#### 2.2 URL Pattern Variation
```python
def generate_url_variations(url):
    variations = []
    
    # Add common parameters
    variations.append(f"{url}?utm_source=test")
    variations.append(f"{url}#section")
    
    # URL encoding variations
    variations.append(url.replace('@', '%40'))
    
    return variations
```

### 3. Model Optimization

#### 3.1 Quantization
```python
# 4-bit quantization for memory efficiency
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)
```

#### 3.2 Flash Attention
```python
# Enable flash attention for faster training
model_kwargs = {
    "attn_implementation": "flash_attention_2",
    "torch_dtype": torch.float16,
}
```

### 4. Advanced LoRA Configuration

#### 4.1 RSLoRA (Rank-Stabilized LoRA)
```python
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,
    lora_alpha=32,
    lora_dropout=0.1,
    use_rslora=True,  # Enable RSLoRA
    target_modules=[
        "q_proj", "v_proj", "k_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ],
)
```

#### 4.2 AdaLoRA (Adaptive LoRA)
```python
from peft import AdaLoraConfig

adalora_config = AdaLoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    init_r=12,
    target_r=8,
    beta1=0.85,
    beta2=0.85,
    tinit=200,
    tfinal=1000,
    deltaT=10,
    orth_reg_weight=0.5,
)
```

## 📊 Training Monitoring

### 1. WandB Integration
```python
# Initialize WandB
import wandb
wandb.init(
    project="phishguard-ai",
    name="experiment-1",
    config={
        "model": "gemma-2b",
        "dataset_size": len(train_dataset),
        "batch_size": 4,
        "learning_rate": 2e-5,
    }
)

# Log metrics during training
wandb.log({
    "train_loss": train_loss,
    "eval_loss": eval_loss,
    "learning_rate": lr,
})
```

### 2. Custom Callbacks
```python
from transformers import TrainerCallback

class CustomCallback(TrainerCallback):
    def on_step_end(self, args, state, control, **kwargs):
        if state.global_step % 100 == 0:
            # Log custom metrics
            wandb.log({
                "custom_metric": calculate_custom_metric(),
                "step": state.global_step,
            })
```

### 3. Training Visualization
```python
import matplotlib.pyplot as plt

def plot_training_curves(logs):
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(logs['train_loss'], label='Train Loss')
    plt.plot(logs['eval_loss'], label='Eval Loss')
    plt.title('Training and Validation Loss')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(logs['learning_rate'], label='Learning Rate')
    plt.title('Learning Rate Schedule')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('training_curves.png')
```

## 🚀 Performance Optimization

### 1. Memory Optimization

#### 1.1 Gradient Checkpointing
```python
# Enable gradient checkpointing
model.gradient_checkpointing_enable()

# In training arguments
training_args = TrainingArguments(
    gradient_checkpointing=True,
    dataloader_pin_memory=False,
)
```

#### 1.2 Mixed Precision Training
```python
# Enable mixed precision
training_args = TrainingArguments(
    fp16=True,  # For NVIDIA GPUs
    bf16=True,  # For newer GPUs (A100, H100)
)
```

### 2. Speed Optimization

#### 2.1 DataLoader Optimization
```python
training_args = TrainingArguments(
    dataloader_num_workers=4,
    dataloader_pin_memory=True,
    group_by_length=True,  # Group similar length sequences
)
```

#### 2.2 Model Compilation (PyTorch 2.0+)
```python
# Compile model for faster training
model = torch.compile(model)
```

### 3. Distributed Training

#### 3.1 Multi-GPU Training
```bash
# Use accelerate for multi-GPU
accelerate launch --multi_gpu train_models.py
```

#### 3.2 DeepSpeed Integration
```bash
# Use DeepSpeed for memory efficiency
deepspeed --num_gpus=2 train_models.py --deepspeed ds_config.json
```

## 🔍 Model Evaluation

### 1. Automated Evaluation
```python
def evaluate_model_performance(model, test_dataset):
    metrics = {
        'accuracy': 0.0,
        'response_time': 0.0,
        'success_rate': 0.0,
    }
    
    for example in test_dataset:
        start_time = time.time()
        response = model.generate(example['input'])
        response_time = time.time() - start_time
        
        # Calculate metrics
        metrics['response_time'] += response_time
        if is_valid_response(response, example['expected']):
            metrics['success_rate'] += 1
    
    # Normalize metrics
    metrics['success_rate'] /= len(test_dataset)
    metrics['response_time'] /= len(test_dataset)
    
    return metrics
```

### 2. Human Evaluation
```python
def human_evaluation_samples(model, num_samples=50):
    """Generate samples for human evaluation"""
    samples = []
    
    for i in range(num_samples):
        sample = {
            'input': test_dataset[i]['instruction'],
            'expected': test_dataset[i]['output'],
            'generated': model.generate(test_dataset[i]['instruction']),
            'category': test_dataset[i]['category'],
        }
        samples.append(sample)
    
    return samples
```

### 3. A/B Testing
```python
def ab_test_models(model_a, model_b, test_dataset):
    """Compare two models"""
    results = {
        'model_a': {'wins': 0, 'total': 0},
        'model_b': {'wins': 0, 'total': 0},
    }
    
    for example in test_dataset:
        response_a = model_a.generate(example['input'])
        response_b = model_b.generate(example['input'])
        
        # Human or automated evaluation
        winner = evaluate_responses(response_a, response_b, example['expected'])
        results[winner]['wins'] += 1
        results['model_a']['total'] += 1
        results['model_b']['total'] += 1
    
    return results
```

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### 1. Out of Memory (OOM)
```bash
# Reduce batch size
python train_models.py --batch-size 1

# Enable gradient checkpointing
python train_models.py --gradient-checkpointing

# Use 8-bit quantization
python train_models.py --load-in-8bit
```

#### 2. Slow Training
```bash
# Enable flash attention
python train_models.py --use-flash-attention

# Increase batch size if memory allows
python train_models.py --batch-size 8

# Use mixed precision
python train_models.py --fp16
```

#### 3. Poor Model Performance
```bash
# Increase training epochs
python train_models.py --epochs 10

# Adjust learning rate
python train_models.py --learning-rate 1e-5

# Use more training data
python train_models.py --step collect --force
```

#### 4. Ollama Integration Issues
```bash
# Restart Ollama service
ollama serve

# Recreate models
ollama rm phishguard-ai
ollama create phishguard-ai -f models/phishguard-ai/Modelfile

# Check model status
ollama list
```

## 📈 Training Best Practices

### 1. Data Quality
- **Diversity**: Ensure balanced representation across categories
- **Freshness**: Use recent data for better performance
- **Quality**: Manually validate random samples
- **Size**: Aim for 10K+ samples per category

### 2. Training Strategy
- **Start Small**: Begin with smaller models and datasets
- **Iterate**: Train, evaluate, improve, repeat
- **Monitor**: Track metrics throughout training
- **Validate**: Use separate validation set

### 3. Model Selection
- **Base Model**: Choose appropriate base model size
- **Fine-tuning**: Use LoRA for efficiency
- **Evaluation**: Compare multiple approaches
- **Deployment**: Consider inference requirements

### 4. Continuous Improvement
- **Feedback Loop**: Collect user feedback
- **Data Updates**: Regularly update training data
- **Model Retraining**: Retrain with new data
- **A/B Testing**: Compare model versions

## 🎯 Success Metrics

### Target Performance Indicators
- **Response Accuracy**: >90% for phishing detection
- **Response Time**: <2 seconds for URL analysis
- **User Satisfaction**: >4.5/5 rating
- **False Positives**: <5% for safe URLs
- **False Negatives**: <10% for phishing URLs

### Monitoring Dashboard
```python
def create_monitoring_dashboard():
    """Create real-time monitoring dashboard"""
    dashboard = {
        'model_performance': {
            'accuracy': 0.92,
            'response_time': 1.8,
            'success_rate': 0.95,
        },
        'system_health': {
            'ollama_status': 'healthy',
            'api_uptime': 99.9,
            'memory_usage': 75.2,
        },
        'user_metrics': {
            'total_requests': 15420,
            'unique_users': 3240,
            'satisfaction_score': 4.7,
        }
    }
    return dashboard
```

---

**Remember**: Training AI models is an iterative process. Start with the basic setup, then gradually add advanced techniques based on your performance requirements and available resources. 
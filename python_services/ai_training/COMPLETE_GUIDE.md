# Complete PhishGuard AI Training System Guide

## 🎯 Overview

This guide provides everything you need to train two specialized AI chatbots for PhishGuard:

1. **AI (Phishing Detection)** - Expert cybersecurity assistant for URL analysis
2. **Haru (Recovery & Education)** - Compassionate specialist for victim recovery and education

## 🚀 Quick Start (5 Steps)

### Step 1: Install Prerequisites
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Verify installation
ollama --version
```

### Step 2: Setup Python Environment
```bash
cd ai_training
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### Step 3: Collect Datasets
```bash
# Automated collection from multiple sources
python train_models.py --step collect
```

### Step 4: Train Models
```bash
# Complete training pipeline
python train_models.py --step all
```

### Step 5: Start AI Service
```bash
# Start the AI service
python ai_service_integration.py
```

## 📊 Dataset Sources

### **Primary Phishing Datasets (Free APIs)**

| Source | URL | Format | Size | Access |
|--------|-----|--------|------|--------|
| **PhishTank** | https://data.phishtank.com/data/online-valid.json | JSON | 10K+ URLs | Free API |
| **OpenPhish** | https://openphish.com/feed.txt | TXT | Real-time | Free feed |
| **URLhaus** | https://urlhaus.abuse.ch/downloads/csv_recent/ | CSV | 100K+ URLs | Free API |
| **PhishStats** | https://phishstats.info/phish_score.csv | CSV | 50K+ URLs | Free |

### **Research Datasets**

| Source | URL | Format | Size | Access |
|--------|-----|--------|------|--------|
| **Kaggle Phishing** | https://www.kaggle.com/datasets/shashwatwork/phishing-dataset | CSV | 10K+ URLs | Free |
| **UCI Phishing** | https://archive.ics.uci.edu/dataset/327/phishing+websites | CSV | 11K URLs | Free |
| **IEEE DataPort** | https://ieee-dataport.org/ | Various | Large | Free |

### **Educational Content Sources**

| Source | URL | Type | Content |
|--------|-----|------|---------|
| **FTC Consumer** | https://www.consumer.ftc.gov/ | Recovery | Official guides |
| **NCSC UK** | https://www.ncsc.gov.uk/collection/phishing-scams | Education | Cybersecurity |
| **FBI Scams** | https://www.fbi.gov/scams-and-safety | Recovery | Law enforcement |
| **IdentityTheft.gov** | https://www.identitytheft.gov/ | Recovery | Official recovery |

### **Myanmar-Specific Sources**

| Source | URL | Type | Content |
|--------|-----|------|---------|
| **Myanmar CERT** | https://cert.gov.mm/ | Alerts | Local threats |
| **CBM Security** | https://www.cbm.gov.mm/ | Banking | Security notices |
| **Local News** | Various | Reports | Scam reports |

### **Safe URL Datasets**

| Source | URL | Format | Size |
|--------|-----|--------|------|
| **Alexa Top Sites** | https://s3.amazonaws.com/alexa-static/top-1m.csv.zip | CSV | 1M sites |
| **Tranco List** | https://tranco-list.eu/download_daily/1M | TXT | 1M sites |
| **Majestic Million** | https://majestic.com/reports/majestic-million | CSV | 1M sites |

## 🔧 Training Process

### **Basic Training (Recommended for First Run)**

```bash
# 1. Collect datasets
python train_models.py --step collect

# 2. Train AI model
python train_models.py --step train-ai

# 3. Train Haru model
python train_models.py --step train-haru

# 4. Setup Ollama models
python train_models.py --step setup-ollama

# 5. Test models
python train_models.py --step test
```

### **Advanced Training (For Better Performance)**

```bash
# Use advanced trainer with optimizations
python advanced_model_trainer.py
```

### **Training Configuration**

#### **For Low Memory Systems (8GB RAM)**
```python
training_config = {
    "batch_size": 1,
    "gradient_accumulation_steps": 16,
    "load_in_8bit": True,
    "gradient_checkpointing": True,
    "learning_rate": 1e-5,
    "num_train_epochs": 3,
}
```

#### **For High Performance Systems (32GB+ RAM, GPU)**
```python
training_config = {
    "batch_size": 8,
    "gradient_accumulation_steps": 2,
    "load_in_4bit": True,
    "use_flash_attention": True,
    "learning_rate": 2e-5,
    "num_train_epochs": 5,
}
```

## 🛠️ Advanced Techniques

### **1. LangChain 0.3+ Integration**

```python
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnablePassthrough

# Create RAG chain
template = """Answer the question based on the context:

Context: {context}
Question: {question}

Answer:"""

prompt = PromptTemplate.from_template(template)
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

### **2. Advanced LoRA Configuration**

```python
# RSLoRA (Rank-Stabilized LoRA)
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

### **3. Performance Optimizations**

```python
# 4-bit quantization
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)

# Flash attention
model_kwargs = {
    "attn_implementation": "flash_attention_2",
    "torch_dtype": torch.float16,
}
```

## 📈 Monitoring and Evaluation

### **Training Metrics**
- **Loss**: Training and validation loss
- **Accuracy**: Model performance on test set
- **Response Time**: Generation speed
- **Memory Usage**: GPU/RAM utilization

### **Quality Metrics**
- **Success Rate**: >90% for phishing detection
- **False Positives**: <5% for safe URLs
- **False Negatives**: <10% for phishing URLs
- **User Satisfaction**: >4.5/5 rating

### **Monitoring Dashboard**
```python
def create_dashboard():
    return {
        'model_performance': {
            'accuracy': 0.92,
            'response_time': 1.8,
            'success_rate': 0.95,
        },
        'system_health': {
            'ollama_status': 'healthy',
            'api_uptime': 99.9,
            'memory_usage': 75.2,
        }
    }
```

## 🔄 Continuous Improvement

### **Data Collection Schedule**
```python
import schedule

def schedule_collection():
    # Daily phishing data collection
    schedule.every().day.at("00:00").do(collect_phishtank_data)
    schedule.every().day.at("06:00").do(collect_openphish_data)
    schedule.every().day.at("12:00").do(collect_urlhaus_data)
    
    # Weekly educational content
    schedule.every().sunday.at("02:00").do(collect_educational_content)
```

### **Model Retraining**
```bash
# Retrain with new data
python train_models.py --step collect --force
python train_models.py --step all

# A/B test new model
python advanced_model_trainer.py --ab-test
```

## 🚀 Deployment

### **Integration with Existing Backend**

#### **Update Backend Configuration**
```javascript
// backend/services/aiService.js
const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:8001';
```

#### **Add Environment Variable**
```env
# backend/.env
AI_SERVICE_URL=http://localhost:8001
```

### **API Endpoints**

| Endpoint | Method | Purpose | Chatbot |
|----------|--------|---------|---------|
| `/analyze` | POST | URL threat analysis | AI |
| `/chat` | POST | General chat | AI/Haru |
| `/ai/analyze` | POST | Direct AI analysis | AI |
| `/haru/help` | POST | Victim assistance | Haru |
| `/haru/educate` | POST | Cybersecurity education | Haru |
| `/haru/recovery` | POST | Recovery plans | Haru |
| `/health` | GET | Service health check | Both |

### **Example API Usage**
```bash
# Test AI analysis
curl -X POST http://localhost:8001/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://suspicious-link.com"}'

# Test Haru help
curl -X POST http://localhost:8001/haru/help \
  -H "Content-Type: application/json" \
  -d '{"message": "I think I\'ve been scammed"}'
```

## 🛠️ Troubleshooting

### **Common Issues**

#### **1. Out of Memory (OOM)**
```bash
# Reduce batch size
python train_models.py --batch-size 1

# Enable gradient checkpointing
python train_models.py --gradient-checkpointing

# Use 8-bit quantization
python train_models.py --load-in-8bit
```

#### **2. Slow Training**
```bash
# Enable flash attention
python train_models.py --use-flash-attention

# Increase batch size if memory allows
python train_models.py --batch-size 8

# Use mixed precision
python train_models.py --fp16
```

#### **3. Poor Model Performance**
```bash
# Increase training epochs
python train_models.py --epochs 10

# Adjust learning rate
python train_models.py --learning-rate 1e-5

# Use more training data
python train_models.py --step collect --force
```

#### **4. Ollama Issues**
```bash
# Restart Ollama service
ollama serve

# Recreate models
ollama rm phishguard-ai
ollama create phishguard-ai -f models/phishguard-ai/Modelfile

# Check model status
ollama list
```

## 📋 System Requirements

### **Minimum Requirements**
- **RAM**: 16GB
- **Storage**: 20GB free space
- **Python**: 3.8+
- **Ollama**: Latest version

### **Recommended Requirements**
- **RAM**: 32GB+
- **Storage**: 50GB free space
- **GPU**: NVIDIA GPU with 8GB+ VRAM
- **Python**: 3.9+
- **Ollama**: Latest version

### **Performance Optimization**
- **SSD Storage**: For faster data loading
- **High-speed Internet**: For dataset collection
- **Multiple CPU Cores**: For parallel processing

## 🎯 Success Metrics

### **Target Performance**
- **Response Accuracy**: >90% for phishing detection
- **Response Time**: <2 seconds for URL analysis
- **User Satisfaction**: >4.5/5 rating
- **False Positives**: <5% for safe URLs
- **False Negatives**: <10% for phishing URLs

### **Monitoring Checklist**
- [ ] Model accuracy >90%
- [ ] Response time <2 seconds
- [ ] System uptime >99%
- [ ] Memory usage <80%
- [ ] User satisfaction >4.5/5

## 🔗 Additional Resources

### **Documentation**
- [LangChain 0.3 Documentation](https://python.langchain.com/)
- [Transformers Documentation](https://huggingface.co/docs/transformers)
- [Ollama Documentation](https://ollama.ai/docs)
- [PEFT Documentation](https://huggingface.co/docs/peft)

### **Research Papers**
- [LoRA Paper](https://arxiv.org/abs/2106.09685)
- [RSLoRA Paper](https://arxiv.org/abs/2308.11372)
- [Flash Attention Paper](https://arxiv.org/abs/2205.14135)

### **Community Resources**
- [Hugging Face Community](https://huggingface.co/community)
- [Ollama Discord](https://discord.gg/ollama)
- [Myanmar Cybersecurity Community](https://t.me/myanmar_cybersecurity)

---

## 🎉 Quick Commands Summary

```bash
# Complete setup and training
cd ai_training
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python train_models.py --step all
python ai_service_integration.py

# Test the system
curl http://localhost:8001/health
curl -X POST http://localhost:8001/ai/analyze -H "Content-Type: application/json" -d '{"url": "https://example.com"}'
```

**Your PhishGuard AI system is now ready to protect users from phishing threats! 🛡️**

---

**Made with ❤️ for Myanmar by Team Vaultaris**

*Protecting digital lives with AI-powered cybersecurity.* 
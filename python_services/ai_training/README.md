# PhishGuard AI Training System

This directory contains the complete AI training system for PhishGuard, featuring two specialized chatbots:

1. **AI (Phishing Detection)** - Expert cybersecurity assistant for URL analysis and threat detection
2. **Haru (Recovery & Education)** - Compassionate specialist for victim recovery and cybersecurity education

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **Ollama** - Install from [ollama.ai](https://ollama.ai)
3. **Git LFS** (for large model files)
4. **At least 10GB free disk space**

### Installation

1. **Clone and setup the training environment:**
```bash
cd ai_training
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Start Ollama:**
```bash
ollama serve
```

3. **Pull the base model:**
```bash
ollama pull gemma2:4b
```

4. **Run the complete training pipeline:**
```bash
python train_models.py
```

## 📊 Dataset Sources

### Phishing Detection Datasets

| Source | Description | Format | Access |
|--------|-------------|--------|--------|
| **PhishTank** | Verified phishing URLs | JSON | Free API |
| **OpenPhish** | Real-time phishing feed | TXT | Free feed |
| **URLhaus** | Malware URL database | CSV | Free API |
| **Custom Myanmar** | Local scam patterns | JSON | Manual collection |

### Educational Content Sources

| Source | Description | Type |
|--------|-------------|------|
| **FTC Consumer** | Official scam prevention guides | Recovery |
| **NCSC UK** | National cybersecurity guidance | Education |
| **FBI Scams** | Law enforcement resources | Recovery |
| **Myanmar CBM** | Local banking security | Local |

### Safe URL Datasets

| Source | Description | Size |
|--------|-------------|------|
| **Alexa Top Sites** | Most visited legitimate sites | 1M+ |
| **Tranco List** | Domain popularity ranking | 1M+ |

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Dataset       │    │   Model         │    │   Ollama        │
│   Collector     │───►│   Trainer       │───►│   Integration   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Phishing      │    │   Fine-tuned    │    │   AI Service    │
│   URLs          │    │   Models        │    │   API           │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Directory Structure

```
ai_training/
├── config.py                 # Configuration settings
├── dataset_collector.py      # Dataset collection and processing
├── model_trainer.py          # Model training pipeline
├── ollama_integration.py     # Ollama API integration
├── ai_service_integration.py # FastAPI service integration
├── train_models.py           # Main training script
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── data/                     # Collected datasets
│   ├── phishing/            # Phishing URL datasets
│   ├── educational/         # Educational content
│   ├── safe/               # Safe URL datasets
│   └── processed/          # Processed training data
├── models/                  # Trained models
│   ├── phishguard-ai/      # AI model files
│   └── phishguard-haru/    # Haru model files
├── logs/                    # Training logs
└── cache/                   # Model cache
```

## 🤖 Model Details

### AI (Phishing Detection) Model

**Purpose:** URL analysis and threat detection
**Base Model:** Gemma2:4b
**Training Data:** 10,000+ phishing URLs + safe URLs
**Specialization:** Cybersecurity threat analysis

**Key Features:**
- URL pattern analysis
- Threat level classification
- Safety recommendations
- Myanmar-specific scam detection

### Haru (Recovery & Education) Model

**Purpose:** Victim recovery and cybersecurity education
**Base Model:** Gemma2:4b
**Training Data:** Recovery guides + educational content
**Specialization:** Empathetic support and education

**Key Features:**
- Victim recovery guidance
- Emotional support
- Educational content
- Step-by-step recovery plans

## 🛠️ Training Commands

### Complete Pipeline
```bash
python train_models.py --step all
```

### Individual Steps
```bash
# Collect datasets
python train_models.py --step collect

# Train AI model
python train_models.py --step train-ai

# Train Haru model
python train_models.py --step train-haru

# Setup Ollama models
python train_models.py --step setup-ollama

# Test models
python train_models.py --step test
```

### Force Dataset Collection
```bash
python train_models.py --step collect --force
```

### Check Prerequisites Only
```bash
python train_models.py --check-only
```

## 🔧 Configuration

### Model Configuration

Edit `config.py` to customize:

- **Training parameters** (learning rate, epochs, batch size)
- **Model parameters** (temperature, top_p, max_length)
- **System prompts** for each chatbot
- **Dataset sources** and processing options

### Environment Variables

```bash
export OLLAMA_BASE_URL="http://localhost:11434"
export WANDB_API_KEY="your_wandb_key"  # Optional for experiment tracking
```

## 📈 Training Process

### 1. Dataset Collection (30-60 minutes)
- Collects phishing URLs from multiple sources
- Gathers educational content and recovery guides
- Downloads safe URL datasets for negative examples
- Processes and formats data for training

### 2. Model Training (2-4 hours per model)
- Fine-tunes Gemma2:4b using LoRA (Low-Rank Adaptation)
- Uses instruction tuning format
- Implements early stopping and model checkpointing
- Supports gradient accumulation for memory efficiency

### 3. Ollama Integration (5-10 minutes)
- Generates Modelfiles for both models
- Creates custom models in Ollama
- Tests model functionality

## 🚀 Deployment

### Start AI Service
```bash
python ai_service_integration.py
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/analyze` | POST | Analyze URL for threats |
| `/chat` | POST | Chat with AI or Haru |
| `/ai/analyze` | POST | Direct AI analysis |
| `/haru/help` | POST | Haru victim assistance |
| `/haru/educate` | POST | Haru education |
| `/haru/recovery` | POST | Haru recovery plans |
| `/health` | GET | Service health check |

### Integration with Existing Backend

Update your existing backend configuration:

```javascript
// backend/services/aiService.js
const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:8001';
```

## 📊 Monitoring and Logging

### Training Logs
- All training logs are saved to `logs/training.log`
- WandB integration for experiment tracking (optional)
- Model performance metrics and evaluation results

### Health Monitoring
```bash
curl http://localhost:8001/health
```

### Model Testing
```bash
# Test AI model
curl -X POST http://localhost:8001/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://suspicious-link.com"}'

# Test Haru model
curl -X POST http://localhost:8001/haru/help \
  -H "Content-Type: application/json" \
  -d '{"message": "I think I\'ve been scammed"}'
```

## 🔍 Troubleshooting

### Common Issues

1. **Ollama not running**
   ```bash
   ollama serve
   ```

2. **Insufficient memory**
   - Reduce batch size in config.py
   - Use gradient accumulation
   - Enable 8-bit quantization

3. **Dataset collection fails**
   - Check internet connection
   - Verify API endpoints are accessible
   - Check rate limits

4. **Model training fails**
   - Ensure sufficient disk space
   - Check GPU memory (if using GPU)
   - Verify Python dependencies

### Performance Optimization

- **GPU Training:** Set `device_map="auto"` for automatic GPU detection
- **Memory Optimization:** Use 8-bit quantization and gradient accumulation
- **Speed Optimization:** Increase batch size if memory allows

## 📚 Additional Resources

### Dataset Sources
- [PhishTank API](https://www.phishtank.com/developer_info.php)
- [OpenPhish Feed](https://openphish.com/)
- [URLhaus API](https://urlhaus.abuse.ch/api/)
- [Alexa Top Sites](https://aws.amazon.com/alexa/)

### Model Resources
- [Gemma Model Card](https://huggingface.co/google/gemma-2b)
- [Ollama Documentation](https://ollama.ai/docs)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)

### Security Considerations
- All training data is collected from public sources
- Models are trained on anonymized data
- No personal information is stored or processed
- Follow responsible AI practices

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the main LICENSE file for details.

## 🙏 Acknowledgments

- **Google** for the Gemma model
- **Ollama** for the local inference framework
- **PhishTank, OpenPhish, URLhaus** for threat intelligence
- **Myanmar cybersecurity community** for local context

---

**Made with ❤️ for Myanmar by Team Vaultaris**

*Protecting digital lives with AI-powered cybersecurity.* 
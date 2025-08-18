# PhishGuard AI Training Setup Guide

This guide will walk you through setting up the complete AI training system for PhishGuard with two specialized chatbots.

## 🎯 Overview

You'll be setting up:
1. **AI (Phishing Detection)** - Expert cybersecurity assistant
2. **Haru (Recovery & Education)** - Compassionate recovery specialist

## 📋 Prerequisites

### System Requirements
- **OS:** Windows 10/11, macOS 10.15+, or Ubuntu 18.04+
- **RAM:** Minimum 8GB, Recommended 16GB+
- **Storage:** At least 10GB free space
- **Python:** 3.8 or higher
- **Internet:** Stable connection for downloading models and datasets

### Software Requirements
- **Ollama** - Local AI model runner
- **Git** - Version control
- **Command Prompt/Terminal** - Command line interface

## 🚀 Step-by-Step Setup

### Step 1: Install Ollama

#### Windows
1. Download from [ollama.ai](https://ollama.ai)
2. Run the installer
3. Open Command Prompt and verify:
```cmd
ollama --version
```

#### macOS
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Linux (Ubuntu/Debian)
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Step 2: Setup Python Environment

1. **Navigate to the ai_training directory:**
```bash
cd ai_training
```

2. **Create virtual environment:**
```bash
python -m venv venv
```

3. **Activate virtual environment:**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Step 3: Setup Ollama Environment

1. **Start Ollama service:**
```bash
ollama serve
```

2. **In a new terminal, run the setup script:**
```bash
python setup_ollama.py
```

This will:
- Verify Ollama installation
- Start the Ollama service
- Pull the base Gemma2:4b model
- Test the setup

### Step 4: Collect Training Datasets

1. **Run dataset collection:**
```bash
python train_models.py --step collect
```

This will collect:
- **Phishing URLs** from PhishTank, OpenPhish, and URLhaus
- **Educational content** from cybersecurity resources
- **Safe URLs** from Alexa and Tranco lists
- **Myanmar-specific** scam patterns

**Expected time:** 30-60 minutes

### Step 5: Train the Models

1. **Train AI (Phishing Detection) model:**
```bash
python train_models.py --step train-ai
```

2. **Train Haru (Recovery & Education) model:**
```bash
python train_models.py --step train-haru
```

**Expected time:** 2-4 hours per model

### Step 6: Setup Ollama Models

1. **Create custom models in Ollama:**
```bash
python train_models.py --step setup-ollama
```

This creates:
- `phishguard-ai` - Phishing detection model
- `phishguard-haru` - Recovery and education model

### Step 7: Test the Models

1. **Test both models:**
```bash
python train_models.py --step test
```

2. **Start the AI service:**
```bash
python ai_service_integration.py
```

3. **Test the API endpoints:**
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

## 🔧 Integration with Existing Backend

### Update Backend Configuration

1. **Edit `backend/services/aiService.js`:**
```javascript
// Update AI service URL
const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://localhost:8001';
```

2. **Add environment variable to `backend/.env`:**
```env
AI_SERVICE_URL=http://localhost:8001
```

### Update Frontend (if needed)

If your frontend needs to distinguish between AI and Haru:

```javascript
// For AI (Phishing Detection)
const aiResponse = await fetch('/api/ai/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ url: suspiciousUrl })
});

// For Haru (Recovery & Education)
const haruResponse = await fetch('/api/ai/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ 
    message: userMessage, 
    chatbot_type: 'haru' 
  })
});
```

## 📊 Dataset Sources

### Where to Find Additional Datasets

#### Phishing Detection
- **PhishTank API:** https://www.phishtank.com/developer_info.php
- **OpenPhish Feed:** https://openphish.com/
- **URLhaus API:** https://urlhaus.abuse.ch/api/
- **Myanmar-specific:** Local cybersecurity reports

#### Educational Content
- **FTC Consumer:** https://www.consumer.ftc.gov/
- **NCSC UK:** https://www.ncsc.gov.uk/
- **FBI Scams:** https://www.fbi.gov/scams-and-safety
- **Myanmar CBM:** https://www.cbm.gov.mm/

#### Safe URLs
- **Alexa Top Sites:** https://aws.amazon.com/alexa/
- **Tranco List:** https://tranco-list.eu/

## 🛠️ Troubleshooting

### Common Issues

#### 1. Ollama Not Starting
```bash
# Check if Ollama is installed
ollama --version

# Start Ollama service
ollama serve

# Check if service is running
curl http://localhost:11434/api/tags
```

#### 2. Insufficient Memory
```bash
# Reduce batch size in config.py
"batch_size": 2,  # Instead of 4

# Use gradient accumulation
"gradient_accumulation_steps": 8,  # Instead of 4
```

#### 3. Dataset Collection Fails
```bash
# Check internet connection
ping google.com

# Check API endpoints
curl https://data.phishtank.com/data/online-valid.json

# Use --force to recollect
python train_models.py --step collect --force
```

#### 4. Model Training Fails
```bash
# Check disk space
df -h

# Check Python dependencies
pip list | grep transformers

# Check GPU memory (if using GPU)
nvidia-smi
```

### Performance Optimization

#### For Low Memory Systems
```python
# In config.py
"batch_size": 1,
"gradient_accumulation_steps": 16,
"load_in_8bit": True,
```

#### For Faster Training
```python
# In config.py
"batch_size": 8,
"gradient_accumulation_steps": 2,
"num_train_epochs": 2,
```

## 📈 Monitoring Training

### Check Training Progress
```bash
# View training logs
tail -f logs/training.log

# Check model files
ls -la models/phishguard-ai/
ls -la models/phishguard-haru/
```

### Monitor System Resources
```bash
# Check CPU and memory usage
htop

# Check disk usage
df -h

# Check GPU usage (if available)
nvidia-smi
```

## 🔍 Testing Your Models

### Test AI Model
```bash
# Test URL analysis
curl -X POST http://localhost:8001/ai/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# Test safety tips
curl -X POST http://localhost:8001/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How can I protect myself from phishing?"}'
```

### Test Haru Model
```bash
# Test victim help
curl -X POST http://localhost:8001/haru/help \
  -H "Content-Type: application/json" \
  -d '{"message": "I clicked a suspicious link, what should I do?"}'

# Test education
curl -X POST http://localhost:8001/haru/educate \
  -H "Content-Type: application/json" \
  -d '{"message": "Teach me about two-factor authentication"}'
```

## 🚀 Production Deployment

### Environment Variables
```bash
export OLLAMA_BASE_URL="http://localhost:11434"
export AI_SERVICE_URL="http://localhost:8001"
export WANDB_API_KEY="your_wandb_key"  # Optional
```

### Service Management
```bash
# Start Ollama service
ollama serve &

# Start AI service
python ai_service_integration.py &

# Monitor services
ps aux | grep ollama
ps aux | grep python
```

### Health Checks
```bash
# Check Ollama
curl http://localhost:11434/api/tags

# Check AI service
curl http://localhost:8001/health

# Check main backend
curl http://localhost:3000/health
```

## 📚 Additional Resources

### Documentation
- [Ollama Documentation](https://ollama.ai/docs)
- [Gemma Model Card](https://huggingface.co/google/gemma-2b)
- [Transformers Documentation](https://huggingface.co/docs/transformers)

### Community Support
- [PhishGuard GitHub Issues](https://github.com/your-repo/issues)
- [Ollama Discord](https://discord.gg/ollama)
- [Myanmar Cybersecurity Community](https://t.me/myanmar_cybersecurity)

## 🎉 Congratulations!

You've successfully set up the PhishGuard AI training system! Your two specialized chatbots are now ready to:

1. **AI (Phishing Detection)** - Analyze URLs and detect threats
2. **Haru (Recovery & Education)** - Help victims and educate users

### Next Steps
1. Monitor model performance
2. Collect user feedback
3. Retrain models with new data
4. Expand to more languages (Burmese)
5. Add voice interaction capabilities

---

**Need help?** Check the troubleshooting section or create an issue on GitHub.

**Made with ❤️ for Myanmar by Team Vaultaris** 
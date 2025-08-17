# PhishGuard Setup Guide

## 🚀 Quick Start

### 1. Download and Install

```bash
# Clone the repository
git clone https://github.com/your-username/phishguard.git
cd phishguard

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Basic Configuration

```bash
# Copy environment template
copy env.example .env

# Edit .env file with your settings
notepad .env  # Windows
nano .env     # Linux/macOS
```

### 3. Test Basic Functionality

```bash
# Test basic URL analysis (works without API keys)
python -m app.cli analyze https://suspicious-link.com

# Test safety tips
python -m app.cli tips

# Start interactive chat
python -m app.cli chat
```

## 🔑 URLhaus API Setup (Recommended)

URLhaus provides comprehensive malware detection. Follow these steps to enable it:

### Step 1: Get Free Auth Key

1. **Visit URLhaus API Portal**
   ```
   https://urlhaus.abuse.ch/api/
   ```

2. **Create Account**
   - Click "abuse.ch Authentication Portal"
   - Sign up for a free account
   - Verify your email address

3. **Generate Auth Key**
   - Log into your account
   - Navigate to API section
   - Click "Generate new Auth-Key"
   - Copy the generated key

### Step 2: Configure PhishGuard

#### Option A: Automated Setup (Recommended)
```bash
python setup_urlhaus.py
```
This script will:
- Guide you through the process
- Test your auth key
- Save it securely to .env file

#### Option B: Manual Setup
1. **Edit .env file**
   ```bash
   # Replace 'your_auth_key_here' with your actual key
   URLHAUS_AUTH_KEY=your_actual_auth_key_here
   ```

2. **Test the configuration**
   ```bash
   python demo_urlhaus.py
   ```

### Step 3: Verify URLhaus Integration

```bash
# Test intelligence summary
python -m app.cli intel summary

# Test recent threats
python -m app.cli intel recent --limit 10

# Test host checking
python -m app.cli intel host suspicious-domain.com

# Test tag search
python -m app.cli intel tag emotet
```

## 🖥️ Running PhishGuard

### Command Line Interface

```bash
# Analyze URLs
python -m app.cli analyze https://example.com

# Get safety tips
python -m app.cli tips

# Report scams
python -m app.cli report "https://scam.com" "Description of scam"

# Interactive mode
python -m app.cli chat

# Threat intelligence (requires URLhaus)
python -m app.cli intel summary
python -m app.cli intel recent --limit 20
python -m app.cli intel tag phishing
python -m app.cli intel host malicious-domain.com
```

### API Server

```bash
# Start the FastAPI server
python -m app.api

# Server will be available at:
# http://localhost:8000

# API documentation at:
# http://localhost:8000/docs
```

### Demos

```bash
# Basic demo (works without URLhaus)
python demo.py

# URLhaus integration demo (requires auth key)
python demo_urlhaus.py
```

## 📊 API Usage Examples

### Basic URL Analysis
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://suspicious-link.com"}'
```

### URLhaus Intelligence
```bash
# Get threat summary
curl "http://localhost:8000/intelligence/summary"

# Get recent malware URLs
curl "http://localhost:8000/intelligence/recent-urls?limit=10"

# Check host reputation
curl -X POST "http://localhost:8000/intelligence/check-host" \
  -H "Content-Type: application/json" \
  -d '{"host": "suspicious-domain.com"}'

# Search by malware tag
curl -X POST "http://localhost:8000/intelligence/search-tag" \
  -H "Content-Type: application/json" \
  -d '{"tag": "emotet"}'
```

## 🛡️ Detection Capabilities

### Without URLhaus (Free)
- ✅ **Pattern Analysis**: Detects suspicious URL patterns
- ✅ **PhishTank API**: Community-verified phishing URLs
- ✅ **URL Structure**: Analyzes domain characteristics
- ✅ **Myanmar-Specific**: Local scam pattern detection

### With URLhaus (Free + Enhanced)
- ✅ **All above features**
- ✅ **Malware URLs**: Comprehensive malware detection
- ✅ **Host Reputation**: Domain reputation checking
- ✅ **Threat Intelligence**: Recent threats and trends
- ✅ **Tag Search**: Search by malware families
- ✅ **Blacklist Status**: SURBL and Spamhaus integration

## 🔧 Configuration Options

### Environment Variables (.env file)

```bash
# URLhaus API Configuration
URLHAUS_AUTH_KEY=your_auth_key_here

# Logging Level
LOG_LEVEL=INFO

# Database URL (for future use)
DATABASE_URL=sqlite:///phishguard.db
```

### Detection Thresholds (config.py)

```python
# Pattern detection threshold
PATTERN_THRESHOLD = 0.3

# URL structure analysis threshold
STRUCTURE_THRESHOLD = 0.6

# Myanmar-specific detection threshold
MYANMAR_THRESHOLD = 0.7

# API request timeout
REQUEST_TIMEOUT = 15
```

## 🚨 Troubleshooting

### Common Issues

#### 1. URLhaus Auth Key Issues
```
WARNING: URLhaus API requires auth key
```
**Solution**: 
- Get auth key from https://urlhaus.abuse.ch/api/
- Run `python setup_urlhaus.py`
- Or manually edit .env file

#### 2. Module Import Errors
```
ModuleNotFoundError: No module named 'app'
```
**Solution**: 
- Ensure you're in the PhishGuard directory
- Activate virtual environment
- Install requirements: `pip install -r requirements.txt`

#### 3. API Server Issues
```
uvicorn.error.Startup failed
```
**Solution**: 
- Check if port 8000 is available
- Try different port: `uvicorn app.api:app --port 8001`

#### 4. Network/Firewall Issues
```
requests.exceptions.RequestException
```
**Solution**: 
- Check internet connection
- Verify firewall allows outbound HTTPS
- Try with different network

### Getting Help

1. **Check logs**: Look for error messages in terminal
2. **Test basic functionality**: Use commands without URLhaus first
3. **Verify configuration**: Run `python setup_urlhaus.py`
4. **Check documentation**: Read API docs at `/docs` endpoint
5. **Report issues**: Create GitHub issue with error details

## 📈 Performance Tips

### For Better Speed
- Use `--limit` parameter to reduce API calls
- Cache results locally when possible
- Run API server for multiple analyses

### For Better Accuracy
- Configure URLhaus API for comprehensive detection
- Combine multiple detection methods
- Keep patterns and signatures updated

## 🔮 Next Steps

Once you have PhishGuard running:

1. **Integrate with Browser**: Create browser extension
2. **Deploy to Cloud**: Use AWS/DigitalOcean for production
3. **Add Database**: Store reports and analytics
4. **Customize Patterns**: Add your own threat patterns
5. **Scale Up**: Use load balancer for high traffic

## 📞 Support

- **Documentation**: README.md and API docs
- **Examples**: demo.py and demo_urlhaus.py
- **Configuration**: setup_urlhaus.py
- **Issues**: GitHub repository issues
- **URLhaus Support**: https://abuse.ch/contact/

---

**You're now ready to protect Myanmar from phishing threats!** 🛡️ 
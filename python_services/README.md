# PhishGuard 🛡️

**AI-powered phishing detection chatbot for Myanmar**

PhishGuard is a secure, AI-powered chatbot designed to detect phishing threats, assist scam victims, and educate users on digital safety. Built specifically for the Myanmar context, it helps protect users from common scams like fake bank logins, lottery frauds, and investment traps.

## 🌟 Key Features

- **🔍 Real-time URL Analysis**: Detect malicious links using multiple free APIs
- **🇲🇲 Myanmar-Specific Detection**: Recognize local scam patterns and keywords
- **🤖 Interactive Chatbot**: Get instant guidance and safety advice
- **📝 Community Reporting**: Report scams to help protect others
- **🛡️ Safety Education**: Learn digital safety best practices
- **⚡ Fast & Free**: Uses free APIs and local processing

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/phishguard.git
   cd phishguard
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup URLhaus API (Optional but Recommended)**
   ```bash
   python setup_urlhaus.py
   ```
   
   This will guide you through getting a free URLhaus API key for enhanced malware detection.

### Running the Application

#### Option 1: API Server
```bash
# Start the FastAPI server
python -m app.api

# Server will be available at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

#### Option 2: Command Line Interface
```bash
# Analyze a URL
python -m app.cli analyze https://suspicious-link.com

# Get safety tips
python -m app.cli tips

# Report a scam
python -m app.cli report "https://scam.com" "Fake bank login page"

# Interactive chat mode
python -m app.cli chat

# URLhaus Intelligence Commands
python -m app.cli intel summary
python -m app.cli intel recent --limit 20
python -m app.cli intel tag emotet
python -m app.cli intel host suspicious-domain.com
```

#### Option 3: Run Tests
```bash
# Run comprehensive test suite
python -m app.webrisk_test
```

## 🔧 API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and status |
| `/analyze` | POST | Analyze URL for threats |
| `/report` | POST | Report a scam URL |
| `/tips` | GET | Get digital safety tips |
| `/chat` | POST | Chat with the bot |
| `/stats` | GET | System statistics |
| `/health` | GET | Health check |

### URLhaus Intelligence Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/intelligence/recent-urls` | GET | Get recent malware URLs from URLhaus |
| `/intelligence/recent-payloads` | GET | Get recent malware payloads |
| `/intelligence/summary` | GET | Get threat intelligence summary |
| `/intelligence/search-tag` | POST | Search URLs by malware tag |
| `/intelligence/check-host` | POST | Check host reputation |

### Example API Usage

```bash
# Analyze a URL
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://suspicious-link.com"}'

# Get safety tips
curl "http://localhost:8000/tips"

# Chat with bot
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "How can I protect myself from scams?"}'

# Get threat intelligence summary
curl "http://localhost:8000/intelligence/summary"

# Get recent malware URLs
curl "http://localhost:8000/intelligence/recent-urls?limit=10"

# Check host reputation
curl -X POST "http://localhost:8000/intelligence/check-host" \
  -H "Content-Type: application/json" \
  -d '{"host": "suspicious-domain.com"}'
```

## 🛡️ Detection Methods

PhishGuard uses multiple detection methods:

1. **Pattern Analysis**: Detects suspicious URL patterns and keywords
2. **PhishTank API**: Checks against verified phishing database
3. **URL Structure Analysis**: Analyzes domain characteristics
4. **Myanmar-Specific Detection**: Recognizes local scam patterns

### Free API Alternatives

Since Google Web Risk API is not free, PhishGuard uses:

- **PhishTank API**: Free, community-driven phishing database
- **URLhaus API**: Free malware URL database with comprehensive threat intelligence
- **URLVoid API**: Free tier available
- **OpenPhish API**: Free for non-commercial use

## 🇲🇲 Myanmar-Specific Features

### Local Scam Detection
- KBZ Bank impersonation scams
- Myanmar lottery frauds
- Investment and money doubling schemes
- Government impersonation scams
- Gaming-related frauds

### Local Keywords
- Myanmar banks: KBZ, Ayeyarwady, CB, MAB, UAB
- Currency: Kyat, MMK, Dollar, USD
- Cities: Yangon, Mandalay, Naypyidaw
- Common scam terms: lottery, inheritance, refund, tax

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React.js      │    │   FastAPI       │    │   PhishGuard    │
│   Frontend      │◄──►│   Backend       │◄──►│   Core Engine   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Free APIs     │
                       │ • PhishTank     │
                       │ • URLVoid       │
                       │ • OpenPhish     │
                       │ • URLhaus       │
                       └─────────────────┘
```

## 🔒 Security Features

- **Input Validation**: All URLs and inputs are validated
- **Rate Limiting**: Built-in protection against abuse
- **Error Handling**: Graceful handling of API failures
- **Privacy Protection**: User data anonymization
- **CORS Support**: Configurable cross-origin requests

## 📊 Usage Examples

### CLI Examples

```bash
# Analyze a suspicious URL
python -m app.cli analyze "https://kbz-verify-account.secure-banking.cf"

# Get detailed analysis
python -m app.cli analyze --verbose "https://bit.ly/suspicious-link"

# Report a scam
python -m app.cli report "https://fake-lottery.mm" "Fake lottery claiming I won money"

# Interactive chat
python -m app.cli chat
```

### API Examples

```python
import requests

# Analyze URL
response = requests.post("http://localhost:8000/analyze", 
    json={"url": "https://suspicious-link.com"})
result = response.json()
print(f"Threat Level: {result['threat_level']}")
print(f"Message: {result['message']}")

# Chat with bot
response = requests.post("http://localhost:8000/chat",
    json={"message": "I clicked a suspicious link, what should I do?"})
chat_result = response.json()
print(f"Bot: {chat_result['response']}")
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
python -m app.webrisk_test
```

This will test:
- URL analysis with various threat levels
- Safety tips functionality
- Scam reporting system
- Myanmar-specific detection patterns

## 🚀 Deployment

### Local Deployment
```bash
# Install dependencies
pip install -r requirements.txt

# Start server
python -m app.api
```

### Production Deployment
1. Set up a production server (AWS, DigitalOcean, etc.)
2. Install Python 3.8+ and dependencies
3. Configure environment variables
4. Use a process manager like PM2 or systemd
5. Set up reverse proxy (nginx/Apache)
6. Enable HTTPS with SSL certificates

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "-m", "app.api"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **PhishTank**: For providing free phishing database access
- **OpenPhish**: For community-driven threat intelligence
- **URLhaus**: For malware URL feeds
- **University of Information Technology**: For academic support

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/phishguard/issues)
- **Email**: support@phishguard.mm
- **Documentation**: [API Docs](http://localhost:8000/docs)

## 🔮 Future Enhancements

- [ ] Burmese language support
- [ ] Voice interaction capabilities
- [ ] Mobile app development
- [ ] Advanced ML threat prediction
- [ ] Real-time social media monitoring
- [ ] Community moderation system

---

**Made with ❤️ for Myanmar by Team Vaultaris**

*Protecting digital lives, one link at a time.*

# Comprehensive Dataset Sources Guide for PhishGuard AI Training

This guide provides extensive sources for collecting training data for both AI (Phishing Detection) and Haru (Recovery & Education) chatbots.

## 🎯 Dataset Categories

### 1. Phishing Detection Datasets

#### **Primary Sources (Free APIs)**

| Source | URL | Format | Access | Description |
|--------|-----|--------|--------|-------------|
| **PhishTank** | https://data.phishtank.com/data/online-valid.json | JSON | Free API | Verified phishing URLs with metadata |
| **OpenPhish** | https://openphish.com/feed.txt | TXT | Free feed | Real-time phishing feed |
| **URLhaus** | https://urlhaus.abuse.ch/downloads/csv_recent/ | CSV | Free API | Malware URL database |
| **PhishStats** | https://phishstats.info/phish_score.csv | CSV | Free | Phishing statistics and scores |

#### **Secondary Sources (Research Datasets)**

| Source | URL | Format | Access | Description |
|--------|-----|--------|--------|-------------|
| **Kaggle Phishing Dataset** | https://www.kaggle.com/datasets/shashwatwork/phishing-dataset | CSV | Free | 10K+ phishing URLs with features |
| **UCI Phishing Websites** | https://archive.ics.uci.edu/dataset/327/phishing+websites | CSV | Free | Academic dataset with 11K samples |
| **PhishTank Historical** | https://data.phishtank.com/data/ | JSON | Free | Historical phishing data |
| **OpenPhish Archive** | https://openphish.com/ | TXT | Free | Archived phishing feeds |

#### **Myanmar-Specific Sources**

| Source | URL | Format | Access | Description |
|--------|-----|--------|--------|-------------|
| **Myanmar CERT** | https://cert.gov.mm/ | HTML | Public | Myanmar cybersecurity alerts |
| **CBM Security** | https://www.cbm.gov.mm/ | HTML | Public | Central Bank security notices |
| **Local News Sites** | Various | HTML | Public | Local scam reports |

### 2. Educational Content Datasets

#### **Cybersecurity Education**

| Source | URL | Format | Access | Description |
|--------|-----|--------|--------|-------------|
| **FTC Consumer** | https://www.consumer.ftc.gov/ | HTML | Free | Official scam prevention guides |
| **NCSC UK** | https://www.ncsc.gov.uk/collection/phishing-scams | HTML | Free | National cybersecurity guidance |
| **FBI Scams** | https://www.fbi.gov/scams-and-safety | HTML | Free | Law enforcement resources |
| **CISA** | https://www.cisa.gov/topics/cybersecurity | HTML | Free | US cybersecurity resources |

#### **Recovery Guides**

| Source | URL | Format | Access | Description |
|--------|-----|--------|--------|-------------|
| **IdentityTheft.gov** | https://www.identitytheft.gov/ | HTML | Free | Official recovery guides |
| **Consumer.gov** | https://www.consumer.gov/articles/0009-identity-theft | HTML | Free | Consumer protection resources |
| **Better Business Bureau** | https://www.bbb.org/ | HTML | Free | Scam recovery assistance |

#### **Myanmar-Specific Education**

| Source | URL | Format | Access | Description |
|--------|-----|--------|--------|-------------|
| **Myanmar CBM** | https://www.cbm.gov.mm/ | HTML | Public | Banking security guidelines |
| **Myanmar Police** | https://www.myanmar.gov.mm/ | HTML | Public | Law enforcement resources |
| **Local Media** | Various | HTML | Public | Local cybersecurity news |

### 3. Safe URL Datasets

#### **Legitimate Website Lists**

| Source | URL | Format | Access | Description |
|--------|-----|--------|--------|-------------|
| **Alexa Top Sites** | https://s3.amazonaws.com/alexa-static/top-1m.csv.zip | CSV | Free | Most visited legitimate sites |
| **Tranco List** | https://tranco-list.eu/download_daily/1M | TXT | Free | Domain popularity ranking |
| **Majestic Million** | https://majestic.com/reports/majestic-million | CSV | Free | Top million domains |
| **Umbrella Popularity** | https://umbrella.cisco.com/blog/cisco-umbrella-1-million | CSV | Free | Cisco's popular domains |

## 🔧 Data Collection Methods

### 1. Automated Collection Scripts

#### **PhishTank Collection**
```python
import requests
import json
import pandas as pd

def collect_phishtank_data():
    url = "https://data.phishtank.com/data/online-valid.json"
    response = requests.get(url)
    data = response.json()
    
    df = pd.DataFrame(data)
    df.to_csv("phishtank_data.csv", index=False)
    return df
```

#### **OpenPhish Collection**
```python
def collect_openphish_data():
    url = "https://openphish.com/feed.txt"
    response = requests.get(url)
    urls = response.text.strip().split('\n')
    
    df = pd.DataFrame({'url': urls})
    df.to_csv("openphish_data.csv", index=False)
    return df
```

#### **URLhaus Collection**
```python
def collect_urlhaus_data():
    url = "https://urlhaus.abuse.ch/downloads/csv_recent/"
    df = pd.read_csv(url, skiprows=8)  # Skip header rows
    df.to_csv("urlhaus_data.csv", index=False)
    return df
```

### 2. Web Scraping for Educational Content

#### **BeautifulSoup Scraper**
```python
import requests
from bs4 import BeautifulSoup
import time

def scrape_educational_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract main content
    content = soup.find('main') or soup.find('article') or soup.find('body')
    text = content.get_text() if content else ""
    
    return text.strip()

def collect_ftc_content():
    urls = [
        "https://www.consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams",
        "https://www.consumer.ftc.gov/articles/0009-identity-theft",
        # Add more URLs
    ]
    
    content_list = []
    for url in urls:
        content = scrape_educational_content(url)
        content_list.append({
            'source': url,
            'content': content,
            'category': 'recovery_guide'
        })
        time.sleep(1)  # Be respectful
    
    return content_list
```

### 3. Manual Collection for Myanmar-Specific Data

#### **Local News Monitoring**
```python
def collect_myanmar_scam_data():
    # Manual collection from local sources
    myanmar_scams = [
        {
            'url': 'https://fake-kbz-verify.com',
            'description': 'KBZ Bank impersonation scam',
            'source': 'local_news',
            'category': 'banking_scam'
        },
        # Add more manually collected data
    ]
    return myanmar_scams
```

## 📊 Data Processing and Cleaning

### 1. URL Normalization
```python
from urllib.parse import urlparse, urljoin
import re

def normalize_url(url):
    """Normalize URLs for consistent analysis"""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Remove tracking parameters
    parsed = urlparse(url)
    clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    
    return clean_url.lower()
```

### 2. Text Cleaning
```python
import re
import html

def clean_text(text):
    """Clean and normalize text content"""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Decode HTML entities
    text = html.unescape(text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
```

### 3. Data Validation
```python
import validators

def validate_url(url):
    """Validate URL format"""
    return validators.url(url)

def validate_dataset(df):
    """Validate dataset quality"""
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Remove invalid URLs
    df = df[df['url'].apply(validate_url)]
    
    # Remove very short or long content
    df = df[df['content'].str.len() > 50]
    df = df[df['content'].str.len() < 10000]
    
    return df
```

## 🗂️ Dataset Organization

### Directory Structure
```
datasets/
├── raw/
│   ├── phishing/
│   │   ├── phishtank_2024.json
│   │   ├── openphish_2024.txt
│   │   └── urlhaus_2024.csv
│   ├── educational/
│   │   ├── ftc_guides.json
│   │   ├── ncsc_resources.json
│   │   └── myanmar_content.json
│   └── safe/
│       ├── alexa_top_sites.csv
│       └── tranco_list.txt
├── processed/
│   ├── ai_training_data.csv
│   ├── haru_training_data.csv
│   └── validation_data.csv
└── metadata/
    ├── dataset_stats.json
    └── collection_logs.json
```

### Data Format Standards

#### **Phishing URLs Format**
```json
{
    "url": "https://example.com",
    "source": "phishtank",
    "threat_type": "phishing",
    "confidence": 0.95,
    "timestamp": "2024-01-01T00:00:00Z",
    "metadata": {
        "target": "banking",
        "verification_time": "2024-01-01T00:00:00Z"
    }
}
```

#### **Educational Content Format**
```json
{
    "title": "How to Avoid Phishing Scams",
    "content": "Educational content here...",
    "source_url": "https://example.com",
    "category": "recovery_guide",
    "language": "en",
    "tags": ["phishing", "recovery", "safety"]
}
```

## 🔄 Continuous Data Collection

### 1. Automated Scheduling
```python
import schedule
import time

def schedule_data_collection():
    # Collect phishing data daily
    schedule.every().day.at("00:00").do(collect_phishtank_data)
    schedule.every().day.at("06:00").do(collect_openphish_data)
    schedule.every().day.at("12:00").do(collect_urlhaus_data)
    
    # Collect educational content weekly
    schedule.every().sunday.at("02:00").do(collect_educational_content)
    
    while True:
        schedule.run_pending()
        time.sleep(60)
```

### 2. Data Versioning
```python
import git
from datetime import datetime

def version_dataset(dataset_path):
    """Version control for datasets"""
    repo = git.Repo('.')
    
    # Commit new dataset
    repo.index.add([dataset_path])
    commit_message = f"Update dataset - {datetime.now().isoformat()}"
    repo.index.commit(commit_message)
    
    # Tag with version
    version = f"v{datetime.now().strftime('%Y%m%d')}"
    repo.create_tag(version)
```

## 📈 Quality Metrics

### 1. Dataset Quality Indicators
- **Completeness**: Percentage of non-null values
- **Accuracy**: Manual validation of random samples
- **Freshness**: Age of data collection
- **Diversity**: Distribution across categories
- **Size**: Total number of samples

### 2. Monitoring Dashboard
```python
def generate_dataset_report():
    """Generate dataset quality report"""
    report = {
        'total_samples': len(df),
        'completeness': df.notna().mean().to_dict(),
        'category_distribution': df['category'].value_counts().to_dict(),
        'freshness': {
            'oldest': df['timestamp'].min(),
            'newest': df['timestamp'].max()
        },
        'quality_score': calculate_quality_score(df)
    }
    return report
```

## 🚀 Advanced Collection Techniques

### 1. API Rate Limiting
```python
import asyncio
import aiohttp
from asyncio_throttle import Throttler

async def collect_with_rate_limiting(urls):
    """Collect data with rate limiting"""
    throttler = Throttler(rate_limit=10, period=1)  # 10 requests per second
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = throttler.acquire(session.get(url))
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        return responses
```

### 2. Distributed Collection
```python
import multiprocessing as mp

def collect_distributed(urls):
    """Distribute collection across multiple processes"""
    with mp.Pool(processes=4) as pool:
        results = pool.map(collect_single_url, urls)
    return results
```

## 📋 Collection Checklist

### Before Starting
- [ ] Set up data storage directory
- [ ] Configure API keys and access
- [ ] Set up monitoring and logging
- [ ] Plan rate limiting strategy
- [ ] Backup existing data

### During Collection
- [ ] Monitor collection progress
- [ ] Validate data quality
- [ ] Handle API errors gracefully
- [ ] Respect rate limits
- [ ] Log collection activities

### After Collection
- [ ] Clean and normalize data
- [ ] Validate dataset quality
- [ ] Generate quality reports
- [ ] Backup collected data
- [ ] Update dataset metadata

## 🔗 Additional Resources

### Academic Datasets
- **IEEE DataPort**: https://ieee-dataport.org/
- **Kaggle Datasets**: https://www.kaggle.com/datasets
- **UCI Machine Learning Repository**: https://archive.ics.uci.edu/

### Industry Sources
- **VirusTotal**: https://www.virustotal.com/
- **AbuseIPDB**: https://abuseipdb.com/
- **Spamhaus**: https://www.spamhaus.org/

### Research Papers
- **Phishing Detection Research**: Search Google Scholar for recent papers
- **Cybersecurity Datasets**: Academic repositories
- **Myanmar Cybersecurity**: Local research institutions

---

**Remember**: Always respect terms of service, rate limits, and data usage policies when collecting data from external sources. 
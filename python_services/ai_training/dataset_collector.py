"""
Dataset Collector for PhishGuard AI Training
Collects phishing URLs, educational content, and safe URLs for training
"""

import requests
import json
import csv
import pandas as pd
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
import hashlib
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import zipfile
import io

from config import dataset_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatasetCollector:
    """Collects and processes datasets for AI training"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.data_dir / "phishing").mkdir(exist_ok=True)
        (self.data_dir / "educational").mkdir(exist_ok=True)
        (self.data_dir / "safe").mkdir(exist_ok=True)
        (self.data_dir / "processed").mkdir(exist_ok=True)
        
        # Session for requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PhishGuard-Dataset-Collector/1.0 (Educational Project)'
        })
        
        # Rate limiting
        self.request_delay = 1  # seconds between requests
        
    def collect_phishing_datasets(self) -> Dict[str, List[Dict]]:
        """Collect phishing URLs from various sources"""
        logger.info("Starting phishing dataset collection...")
        
        collected_data = {}
        
        # 1. PhishTank dataset
        try:
            logger.info("Collecting PhishTank data...")
            phishtank_data = self._collect_phishtank()
            collected_data['phishtank'] = phishtank_data
            logger.info(f"Collected {len(phishtank_data)} PhishTank URLs")
        except Exception as e:
            logger.error(f"Error collecting PhishTank data: {e}")
        
        # 2. OpenPhish dataset
        try:
            logger.info("Collecting OpenPhish data...")
            openphish_data = self._collect_openphish()
            collected_data['openphish'] = openphish_data
            logger.info(f"Collected {len(openphish_data)} OpenPhish URLs")
        except Exception as e:
            logger.error(f"Error collecting OpenPhish data: {e}")
        
        # 3. URLhaus dataset
        try:
            logger.info("Collecting URLhaus data...")
            urlhaus_data = self._collect_urlhaus()
            collected_data['urlhaus'] = urlhaus_data
            logger.info(f"Collected {len(urlhaus_data)} URLhaus URLs")
        except Exception as e:
            logger.error(f"Error collecting URLhaus data: {e}")
        
        # Save collected data
        self._save_phishing_data(collected_data)
        
        return collected_data
    
    def _collect_phishtank(self) -> List[Dict]:
        """Collect data from PhishTank"""
        url = dataset_config.phishing_datasets['phishtank']['url']
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            processed_data = []
            
            for item in data:
                processed_item = {
                    'url': item.get('url', ''),
                    'phish_id': item.get('phish_id', ''),
                    'verification_time': item.get('verification_time', ''),
                    'target': item.get('target', ''),
                    'source': 'phishtank',
                    'label': 'phishing',
                    'confidence': 0.95
                }
                processed_data.append(processed_item)
                
                # Rate limiting
                time.sleep(self.request_delay)
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Error collecting PhishTank data: {e}")
            return []
    
    def _collect_openphish(self) -> List[Dict]:
        """Collect data from OpenPhish"""
        url = dataset_config.phishing_datasets['openphish']['url']
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            urls = response.text.strip().split('\n')
            processed_data = []
            
            for url_line in urls:
                if url_line.strip():
                    processed_item = {
                        'url': url_line.strip(),
                        'source': 'openphish',
                        'label': 'phishing',
                        'confidence': 0.9
                    }
                    processed_data.append(processed_item)
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Error collecting OpenPhish data: {e}")
            return []
    
    def _collect_urlhaus(self) -> List[Dict]:
        """Collect data from URLhaus"""
        url = dataset_config.phishing_datasets['urlhaus']['url']
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse CSV data
            csv_data = response.text.split('\n')
            reader = csv.DictReader(csv_data)
            
            processed_data = []
            for row in reader:
                if row.get('url'):
                    processed_item = {
                        'url': row.get('url', ''),
                        'threat': row.get('threat', ''),
                        'tags': row.get('tags', ''),
                        'url_status': row.get('url_status', ''),
                        'date_added': row.get('dateadded', ''),
                        'source': 'urlhaus',
                        'label': 'malware',
                        'confidence': 0.95
                    }
                    processed_data.append(processed_item)
            
            return processed_data
            
        except Exception as e:
            logger.error(f"Error collecting URLhaus data: {e}")
            return []
    
    def collect_educational_content(self) -> Dict[str, List[Dict]]:
        """Collect educational content for Haru chatbot"""
        logger.info("Starting educational content collection...")
        
        collected_data = {}
        
        # 1. Cybersecurity tips
        try:
            logger.info("Collecting cybersecurity tips...")
            tips_data = self._collect_cybersecurity_tips()
            collected_data['cybersecurity_tips'] = tips_data
            logger.info(f"Collected {len(tips_data)} cybersecurity tips")
        except Exception as e:
            logger.error(f"Error collecting cybersecurity tips: {e}")
        
        # 2. Recovery guides
        try:
            logger.info("Collecting recovery guides...")
            recovery_data = self._collect_recovery_guides()
            collected_data['recovery_guides'] = recovery_data
            logger.info(f"Collected {len(recovery_data)} recovery guides")
        except Exception as e:
            logger.error(f"Error collecting recovery guides: {e}")
        
        # 3. Myanmar-specific content
        try:
            logger.info("Collecting Myanmar-specific content...")
            myanmar_data = self._collect_myanmar_content()
            collected_data['myanmar_specific'] = myanmar_data
            logger.info(f"Collected {len(myanmar_data)} Myanmar-specific items")
        except Exception as e:
            logger.error(f"Error collecting Myanmar content: {e}")
        
        # Save collected data
        self._save_educational_data(collected_data)
        
        return collected_data
    
    def _collect_cybersecurity_tips(self) -> List[Dict]:
        """Collect cybersecurity tips from various sources"""
        tips_data = []
        
        for source_url in dataset_config.educational_sources['cybersecurity_tips']:
            try:
                logger.info(f"Collecting from: {source_url}")
                content = self._scrape_webpage(source_url)
                
                if content:
                    tips_data.append({
                        'title': f"Cybersecurity Tips from {urlparse(source_url).netloc}",
                        'content': content,
                        'source_url': source_url,
                        'category': 'cybersecurity_tips',
                        'label': 'educational'
                    })
                
                time.sleep(self.request_delay)
                
            except Exception as e:
                logger.error(f"Error collecting from {source_url}: {e}")
        
        return tips_data
    
    def _collect_recovery_guides(self) -> List[Dict]:
        """Collect recovery guides"""
        recovery_data = []
        
        for source_url in dataset_config.educational_sources['recovery_guides']:
            try:
                logger.info(f"Collecting recovery guide from: {source_url}")
                content = self._scrape_webpage(source_url)
                
                if content:
                    recovery_data.append({
                        'title': f"Recovery Guide from {urlparse(source_url).netloc}",
                        'content': content,
                        'source_url': source_url,
                        'category': 'recovery_guide',
                        'label': 'educational'
                    })
                
                time.sleep(self.request_delay)
                
            except Exception as e:
                logger.error(f"Error collecting from {source_url}: {e}")
        
        return recovery_data
    
    def _collect_myanmar_content(self) -> List[Dict]:
        """Collect Myanmar-specific content"""
        myanmar_data = []
        
        for source_url in dataset_config.educational_sources['myanmar_specific']:
            try:
                logger.info(f"Collecting Myanmar content from: {source_url}")
                content = self._scrape_webpage(source_url)
                
                if content:
                    myanmar_data.append({
                        'title': f"Myanmar Content from {urlparse(source_url).netloc}",
                        'content': content,
                        'source_url': source_url,
                        'category': 'myanmar_specific',
                        'label': 'educational'
                    })
                
                time.sleep(self.request_delay)
                
            except Exception as e:
                logger.error(f"Error collecting from {source_url}: {e}")
        
        return myanmar_data
    
    def _scrape_webpage(self, url: str) -> Optional[str]:
        """Scrape content from a webpage"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:5000]  # Limit content length
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return None
    
    def collect_safe_urls(self) -> List[Dict]:
        """Collect safe URLs for negative examples"""
        logger.info("Starting safe URL collection...")
        
        safe_urls = []
        
        # 1. Alexa Top Sites
        try:
            logger.info("Collecting Alexa top sites...")
            alexa_urls = self._collect_alexa_top_sites()
            safe_urls.extend(alexa_urls)
            logger.info(f"Collected {len(alexa_urls)} Alexa top sites")
        except Exception as e:
            logger.error(f"Error collecting Alexa data: {e}")
        
        # 2. Tranco List
        try:
            logger.info("Collecting Tranco list...")
            tranco_urls = self._collect_tranco_list()
            safe_urls.extend(tranco_urls)
            logger.info(f"Collected {len(tranco_urls)} Tranco URLs")
        except Exception as e:
            logger.error(f"Error collecting Tranco data: {e}")
        
        # Save safe URLs
        self._save_safe_urls(safe_urls)
        
        return safe_urls
    
    def _collect_alexa_top_sites(self) -> List[Dict]:
        """Collect Alexa top sites"""
        url = dataset_config.safe_url_datasets['alexa_top_sites']
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Extract from zip file
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                csv_filename = zip_file.namelist()[0]
                with zip_file.open(csv_filename) as csv_file:
                    df = pd.read_csv(csv_file, header=None, names=['rank', 'domain'])
            
            safe_urls = []
            for _, row in df.head(1000).iterrows():  # Top 1000 sites
                safe_urls.append({
                    'url': f"https://{row['domain']}",
                    'domain': row['domain'],
                    'rank': row['rank'],
                    'source': 'alexa',
                    'label': 'safe',
                    'confidence': 0.9
                })
            
            return safe_urls
            
        except Exception as e:
            logger.error(f"Error collecting Alexa data: {e}")
            return []
    
    def _collect_tranco_list(self) -> List[Dict]:
        """Collect Tranco list"""
        url = dataset_config.safe_url_datasets['tranco_list']
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            lines = response.text.strip().split('\n')
            safe_urls = []
            
            for i, line in enumerate(lines[:1000]):  # Top 1000 sites
                if line.strip():
                    domain = line.strip()
                    safe_urls.append({
                        'url': f"https://{domain}",
                        'domain': domain,
                        'rank': i + 1,
                        'source': 'tranco',
                        'label': 'safe',
                        'confidence': 0.9
                    })
            
            return safe_urls
            
        except Exception as e:
            logger.error(f"Error collecting Tranco data: {e}")
            return []
    
    def _save_phishing_data(self, data: Dict[str, List[Dict]]):
        """Save phishing data to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for source, items in data.items():
            if items:
                filename = self.data_dir / "phishing" / f"{source}_{timestamp}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(items, f, indent=2, ensure_ascii=False)
                
                logger.info(f"Saved {len(items)} items to {filename}")
    
    def _save_educational_data(self, data: Dict[str, List[Dict]]):
        """Save educational data to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for category, items in data.items():
            if items:
                filename = self.data_dir / "educational" / f"{category}_{timestamp}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(items, f, indent=2, ensure_ascii=False)
                
                logger.info(f"Saved {len(items)} items to {filename}")
    
    def _save_safe_urls(self, data: List[Dict]):
        """Save safe URLs to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.data_dir / "safe" / f"safe_urls_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(data)} safe URLs to {filename}")
    
    def create_training_datasets(self) -> Dict[str, pd.DataFrame]:
        """Create training datasets for both chatbots"""
        logger.info("Creating training datasets...")
        
        # Load collected data
        phishing_data = self._load_phishing_data()
        educational_data = self._load_educational_data()
        safe_data = self._load_safe_data()
        
        # Create AI (Phishing Detection) dataset
        ai_dataset = self._create_ai_dataset(phishing_data, safe_data)
        
        # Create Haru (Recovery & Education) dataset
        haru_dataset = self._create_haru_dataset(educational_data, phishing_data)
        
        # Save datasets
        self._save_training_datasets(ai_dataset, haru_dataset)
        
        return {
            'ai_dataset': ai_dataset,
            'haru_dataset': haru_dataset
        }
    
    def _load_phishing_data(self) -> List[Dict]:
        """Load all phishing data"""
        phishing_dir = self.data_dir / "phishing"
        all_data = []
        
        for file_path in phishing_dir.glob("*.json"):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_data.extend(data)
        
        return all_data
    
    def _load_educational_data(self) -> List[Dict]:
        """Load all educational data"""
        educational_dir = self.data_dir / "educational"
        all_data = []
        
        for file_path in educational_dir.glob("*.json"):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_data.extend(data)
        
        return all_data
    
    def _load_safe_data(self) -> List[Dict]:
        """Load safe URL data"""
        safe_dir = self.data_dir / "safe"
        all_data = []
        
        for file_path in safe_dir.glob("*.json"):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_data.extend(data)
        
        return all_data
    
    def _create_ai_dataset(self, phishing_data: List[Dict], safe_data: List[Dict]) -> pd.DataFrame:
        """Create dataset for AI (Phishing Detection) chatbot"""
        training_data = []
        
        # Add phishing examples
        for item in phishing_data:
            training_data.append({
                'instruction': f"Analyze this URL for phishing threats: {item['url']}",
                'input': '',
                'output': f"This URL is a confirmed phishing/malware threat. It was detected by {item['source']} with {item['confidence']} confidence. Do not click this link and report it immediately.",
                'category': 'phishing_detection'
            })
        
        # Add safe examples
        for item in safe_data[:len(phishing_data)]:  # Balance the dataset
            training_data.append({
                'instruction': f"Analyze this URL for phishing threats: {item['url']}",
                'input': '',
                'output': f"This URL appears to be safe. It's from {item['source']} and is ranked {item.get('rank', 'N/A')}. However, always remain cautious and verify the source.",
                'category': 'safe_detection'
            })
        
        return pd.DataFrame(training_data)
    
    def _create_haru_dataset(self, educational_data: List[Dict], phishing_data: List[Dict]) -> pd.DataFrame:
        """Create dataset for Haru (Recovery & Education) chatbot"""
        training_data = []
        
        # Add educational content
        for item in educational_data:
            training_data.append({
                'instruction': f"Teach me about {item['category']}",
                'input': '',
                'output': f"Here's what you need to know about {item['category']}: {item['content'][:500]}...",
                'category': 'education'
            })
        
        # Add recovery scenarios
        recovery_scenarios = [
            "I think I've been scammed. What should I do?",
            "How can I recover from a phishing attack?",
            "I clicked a suspicious link. What now?",
            "My account was compromised. Help me recover.",
        ]
        
        recovery_responses = [
            "I'm here to help you through this. First, don't panic. Here are the immediate steps: 1) Change your passwords immediately, 2) Contact your bank if financial info was involved, 3) Enable two-factor authentication, 4) Monitor your accounts for suspicious activity, 5) Report the incident to relevant authorities.",
            "Recovering from a phishing attack requires immediate action. Start by securing your accounts, then document everything, and finally report the incident. Would you like me to guide you through each step?",
            "Don't worry, we can handle this together. First, let's assess what information might have been compromised. Then I'll guide you through the recovery process step by step.",
            "I understand this is stressful. Let's work through this systematically. First, let's secure your accounts, then we'll work on recovery and prevention for the future."
        ]
        
        for scenario, response in zip(recovery_scenarios, recovery_responses):
            training_data.append({
                'instruction': scenario,
                'input': '',
                'output': response,
                'category': 'recovery'
            })
        
        return pd.DataFrame(training_data)
    
    def _save_training_datasets(self, ai_dataset: pd.DataFrame, haru_dataset: pd.DataFrame):
        """Save training datasets"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save AI dataset
        ai_filename = self.data_dir / "processed" / f"ai_training_dataset_{timestamp}.csv"
        ai_dataset.to_csv(ai_filename, index=False)
        logger.info(f"Saved AI training dataset with {len(ai_dataset)} samples to {ai_filename}")
        
        # Save Haru dataset
        haru_filename = self.data_dir / "processed" / f"haru_training_dataset_{timestamp}.csv"
        haru_dataset.to_csv(haru_filename, index=False)
        logger.info(f"Saved Haru training dataset with {len(haru_dataset)} samples to {haru_filename}")
        
        # Save statistics
        stats = {
            'ai_dataset_stats': {
                'total_samples': len(ai_dataset),
                'categories': ai_dataset['category'].value_counts().to_dict()
            },
            'haru_dataset_stats': {
                'total_samples': len(haru_dataset),
                'categories': haru_dataset['category'].value_counts().to_dict()
            },
            'timestamp': timestamp
        }
        
        stats_filename = self.data_dir / "processed" / f"dataset_stats_{timestamp}.json"
        with open(stats_filename, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved dataset statistics to {stats_filename}")

def main():
    """Main function to run dataset collection"""
    from config import phishing_ai_config
    
    collector = DatasetCollector(phishing_ai_config.data_dir)
    
    # Collect all datasets
    logger.info("Starting comprehensive dataset collection...")
    
    # 1. Collect phishing data
    phishing_data = collector.collect_phishing_datasets()
    
    # 2. Collect educational content
    educational_data = collector.collect_educational_content()
    
    # 3. Collect safe URLs
    safe_data = collector.collect_safe_urls()
    
    # 4. Create training datasets
    training_datasets = collector.create_training_datasets()
    
    logger.info("Dataset collection completed successfully!")
    logger.info(f"AI Dataset: {len(training_datasets['ai_dataset'])} samples")
    logger.info(f"Haru Dataset: {len(training_datasets['haru_dataset'])} samples")

if __name__ == "__main__":
    main() 
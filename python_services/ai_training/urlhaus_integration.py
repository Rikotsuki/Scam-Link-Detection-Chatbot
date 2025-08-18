#!/usr/bin/env python3
"""
URLhaus API Integration for PhishGuard AI
Integrates URLhaus threat intelligence for enhanced phishing detection
"""

import os
import requests
import logging
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import hashlib
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class URLhausClient:
    """
    Client for interacting with URLhaus API
    Provides threat intelligence for URL analysis
    """
    
    def __init__(self, auth_key: Optional[str] = None):
        self.base_url = "https://urlhaus-api.abuse.ch/v1"
        self.auth_key = auth_key or os.getenv('URLHAUS_AUTH_KEY')
        self.session = requests.Session()
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0  # 1 second between requests
        
        if self.auth_key:
            logger.info("✅ URLhaus client initialized with authentication")
        else:
            logger.warning("⚠️ URLhaus client initialized without authentication (limited functionality)")
    
    def _rate_limit(self):
        """Enforce rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, data: Optional[Dict] = None, method: str = "POST") -> Optional[Dict]:
        """Make authenticated request to URLhaus API"""
        self._rate_limit()
        
        url = f"{self.base_url}/{endpoint}"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'PhishGuard-AI/1.0'
        }
        
        try:
            if method == "POST":
                if data and self.auth_key:
                    data['auth-key'] = self.auth_key
                response = self.session.post(url, data=data, headers=headers, timeout=10)
            else:
                response = self.session.get(url, headers=headers, timeout=10)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"URLhaus API request failed: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode URLhaus response: {e}")
            return None
    
    def query_url(self, url: str) -> Dict[str, Any]:
        """
        Query URLhaus for information about a specific URL
        
        Args:
            url (str): The URL to query
            
        Returns:
            Dict containing URL analysis results
        """
        logger.info(f"🔍 Querying URLhaus for URL: {url}")
        
        data = {'url': url}
        response = self._make_request('url/', data)
        
        if not response:
            return {
                'status': 'error',
                'message': 'Failed to query URLhaus',
                'is_malicious': False,
                'confidence': 0.0
            }
        
        query_status = response.get('query_status', 'no_results')
        
        if query_status == 'ok':
            # URL found in URLhaus database
            url_status = response.get('url_status', 'unknown')
            threat = response.get('threat', 'unknown')
            date_added = response.get('date_added', '')
            tags = response.get('tags', [])
            
            # Determine confidence based on status and recency
            confidence = self._calculate_confidence(url_status, date_added, tags)
            
            return {
                'status': 'found',
                'is_malicious': True,
                'confidence': confidence,
                'threat_type': threat,
                'url_status': url_status,
                'date_added': date_added,
                'tags': tags,
                'source': 'URLhaus',
                'details': {
                    'urlhaus_reference': response.get('urlhaus_reference', ''),
                    'blacklists': response.get('blacklists', {}),
                    'reporter': response.get('reporter', 'unknown')
                }
            }
        
        elif query_status == 'no_results':
            # URL not found - potentially safe
            return {
                'status': 'not_found',
                'is_malicious': False,
                'confidence': 0.8,  # High confidence it's not malicious if not in URLhaus
                'message': 'URL not found in URLhaus database',
                'source': 'URLhaus'
            }
        
        else:
            # Error or invalid URL
            return {
                'status': 'error',
                'is_malicious': False,
                'confidence': 0.0,
                'message': f'URLhaus query status: {query_status}',
                'source': 'URLhaus'
            }
    
    def _calculate_confidence(self, url_status: str, date_added: str, tags: List[str]) -> float:
        """Calculate confidence score based on URLhaus data"""
        base_confidence = 0.9  # High confidence for URLhaus data
        
        # Adjust based on URL status
        status_modifiers = {
            'online': 0.0,      # No reduction for online threats
            'offline': -0.1,    # Slight reduction for offline threats
            'unknown': -0.2     # More reduction for unknown status
        }
        
        confidence = base_confidence + status_modifiers.get(url_status, -0.2)
        
        # Adjust based on recency
        if date_added:
            try:
                added_date = datetime.strptime(date_added, '%Y-%m-%d %H:%M:%S')
                days_old = (datetime.now() - added_date).days
                
                if days_old > 30:
                    confidence -= 0.1  # Reduce confidence for old entries
            except ValueError:
                pass  # Invalid date format
        
        # Boost confidence for certain tags
        high_risk_tags = ['exe', 'dll', 'zip', 'rar', 'malware', 'trojan', 'ransomware']
        if any(tag in tags for tag in high_risk_tags):
            confidence = min(0.95, confidence + 0.05)
        
        return max(0.0, min(1.0, confidence))
    
    def query_host(self, hostname: str) -> Dict[str, Any]:
        """Query URLhaus for information about a hostname"""
        logger.info(f"🔍 Querying URLhaus for host: {hostname}")
        
        data = {'host': hostname}
        response = self._make_request('host/', data)
        
        if not response:
            return {
                'status': 'error',
                'message': 'Failed to query URLhaus for host',
                'is_malicious': False,
                'confidence': 0.0
            }
        
        query_status = response.get('query_status', 'no_results')
        
        if query_status == 'ok':
            urls = response.get('urls', [])
            
            if urls:
                # Calculate overall threat level based on URLs
                active_threats = sum(1 for url in urls if url.get('url_status') == 'online')
                total_urls = len(urls)
                
                confidence = min(0.9, 0.7 + (active_threats / total_urls) * 0.2)
                
                return {
                    'status': 'found',
                    'is_malicious': True,
                    'confidence': confidence,
                    'total_urls': total_urls,
                    'active_threats': active_threats,
                    'source': 'URLhaus',
                    'urls': urls[:5]  # Return first 5 URLs
                }
        
        return {
            'status': 'not_found',
            'is_malicious': False,
            'confidence': 0.8,
            'message': 'Host not found in URLhaus database',
            'source': 'URLhaus'
        }
    
    def download_feed(self, feed_type: str = 'urls') -> Optional[List[Dict]]:
        """
        Download URLhaus feeds for offline analysis
        
        Args:
            feed_type (str): Type of feed ('urls', 'domains', 'hashes')
            
        Returns:
            List of threat indicators or None if failed
        """
        logger.info(f"📥 Downloading URLhaus {feed_type} feed")
        
        if feed_type == 'urls':
            url = "https://urlhaus.abuse.ch/downloads/csv_recent/"
        elif feed_type == 'domains':
            url = "https://urlhaus.abuse.ch/downloads/hostfile/"
        else:
            logger.error(f"Unsupported feed type: {feed_type}")
            return None
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            if feed_type == 'urls':
                # Parse CSV response
                lines = response.text.strip().split('\n')
                threats = []
                
                for line in lines[9:]:  # Skip header lines
                    if line.startswith('#') or not line.strip():
                        continue
                    
                    parts = line.split(',')
                    if len(parts) >= 4:
                        threats.append({
                            'id': parts[0].strip('"'),
                            'date_added': parts[1].strip('"'),
                            'url': parts[2].strip('"'),
                            'status': parts[3].strip('"'),
                            'threat': parts[4].strip('"') if len(parts) > 4 else 'unknown'
                        })
                
                return threats
            
            elif feed_type == 'domains':
                # Parse hostfile format
                lines = response.text.strip().split('\n')
                domains = []
                
                for line in lines:
                    if line.startswith('#') or not line.strip():
                        continue
                    
                    parts = line.split()
                    if len(parts) >= 2 and parts[0] == '0.0.0.0':
                        domains.append({'domain': parts[1]})
                
                return domains
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download URLhaus feed: {e}")
            return None
    
    def submit_url(self, url: str, threat: str = 'malware_download', tags: List[str] = None, anonymous: bool = True) -> bool:
        """
        Submit a malicious URL to URLhaus
        
        Args:
            url (str): The malicious URL to submit
            threat (str): Type of threat (default: 'malware_download')
            tags (List[str]): Optional tags to add
            anonymous (bool): Whether to make an anonymous submission
            
        Returns:
            bool: True if submission was successful
        """
        if not self.auth_key:
            logger.error("Cannot submit URL: Authentication key required")
            return False
        
        logger.info(f"📤 Submitting URL to URLhaus: {url}")
        
        submission_data = {
            'threat': threat,
            'anonymous': '1' if anonymous else '0',
            'submission': json.dumps([{
                'url': url,
                'threat': threat,
                'tags': tags or []
            }])
        }
        
        response = self._make_request('submit/', submission_data)
        
        if response and response.get('query_status') == 'ok':
            logger.info("✅ URL submitted successfully to URLhaus")
            return True
        else:
            logger.error("❌ Failed to submit URL to URLhaus")
            return False

class URLhausEnhancedAnalysis:
    """
    Enhanced URL analysis combining URLhaus with other techniques
    """
    
    def __init__(self, urlhaus_client: URLhausClient):
        self.urlhaus = urlhaus_client
        
        # Suspicious patterns
        self.suspicious_patterns = [
            r'bit\.ly/[a-zA-Z0-9]+',  # URL shorteners
            r'tinyurl\.com/',
            r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',  # IP addresses
            r'[a-zA-Z0-9-]+\.tk/',  # Free TLD domains
            r'[a-zA-Z0-9-]+\.ml/',
            r'[a-zA-Z0-9-]+\.ga/',
            r'[a-zA-Z0-9-]+\.cf/',
            r'secure.*update',  # Common phishing patterns
            r'verify.*account',
            r'suspend.*account',
            r'click.*here.*now',
        ]
    
    def analyze_url_comprehensive(self, url: str) -> Dict[str, Any]:
        """
        Perform comprehensive URL analysis using URLhaus and pattern matching
        
        Args:
            url (str): URL to analyze
            
        Returns:
            Dict containing comprehensive analysis results
        """
        logger.info(f"🔍 Performing comprehensive analysis for: {url}")
        
        # Get URLhaus analysis
        urlhaus_result = self.urlhaus.query_url(url)
        
        # Perform pattern analysis
        pattern_result = self._analyze_patterns(url)
        
        # Combine results
        is_malicious = urlhaus_result.get('is_malicious', False) or pattern_result.get('is_suspicious', False)
        
        # Calculate combined confidence
        urlhaus_confidence = urlhaus_result.get('confidence', 0.0)
        pattern_confidence = pattern_result.get('confidence', 0.0)
        
        # Weight URLhaus higher than pattern matching
        combined_confidence = (urlhaus_confidence * 0.8) + (pattern_confidence * 0.2)
        
        if urlhaus_result.get('status') == 'found':
            # URLhaus found the URL - high confidence
            combined_confidence = max(combined_confidence, 0.85)
        
        return {
            'url': url,
            'is_malicious': is_malicious,
            'confidence': combined_confidence,
            'analysis_timestamp': datetime.now().isoformat(),
            'sources': {
                'urlhaus': urlhaus_result,
                'pattern_analysis': pattern_result
            },
            'recommendation': self._get_recommendation(is_malicious, combined_confidence)
        }
    
    def _analyze_patterns(self, url: str) -> Dict[str, Any]:
        """Analyze URL for suspicious patterns"""
        import re
        
        suspicious_score = 0
        matched_patterns = []
        
        for pattern in self.suspicious_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                suspicious_score += 1
                matched_patterns.append(pattern)
        
        # Calculate confidence based on pattern matches
        confidence = min(0.7, suspicious_score * 0.15)  # Max 0.7 confidence from patterns
        is_suspicious = suspicious_score > 0
        
        return {
            'is_suspicious': is_suspicious,
            'confidence': confidence,
            'suspicious_score': suspicious_score,
            'matched_patterns': matched_patterns,
            'total_patterns_checked': len(self.suspicious_patterns)
        }
    
    def _get_recommendation(self, is_malicious: bool, confidence: float) -> str:
        """Get recommendation based on analysis results"""
        if is_malicious:
            if confidence >= 0.8:
                return "🚨 HIGH RISK: Block this URL immediately"
            elif confidence >= 0.6:
                return "⚠️ MEDIUM RISK: Exercise caution, consider blocking"
            else:
                return "❓ LOW RISK: Potentially suspicious, monitor closely"
        else:
            if confidence >= 0.8:
                return "✅ SAFE: URL appears to be legitimate"
            else:
                return "❔ UNKNOWN: Insufficient data for confident assessment"

# Example usage and testing
if __name__ == "__main__":
    # Initialize URLhaus client
    client = URLhausClient()
    analyzer = URLhausEnhancedAnalysis(client)
    
    # Test URLs
    test_urls = [
        "https://google.com",
        "https://bit.ly/suspicious123",
        "http://192.168.1.1/malware.exe"
    ]
    
    for test_url in test_urls:
        result = analyzer.analyze_url_comprehensive(test_url)
        print(f"\n🔍 Analysis for {test_url}:")
        print(f"Malicious: {result['is_malicious']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Recommendation: {result['recommendation']}") 
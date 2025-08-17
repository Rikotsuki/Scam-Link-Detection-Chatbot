import requests
import re
import json
import time
import os
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
import hashlib
import logging
from datetime import datetime, timedelta
from .database import PhishGuardDatabase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PhishGuardCore:
    """
    Core phishing detection engine using multiple free APIs
    """
    
    def __init__(self, urlhaus_auth_key=None):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PhishGuard/1.0 (Educational Project)'
        })
        
        # Initialize database
        self.db = PhishGuardDatabase()
        
        # Set URLhaus auth key if provided
        if urlhaus_auth_key:
            self.apis['urlhaus']['auth_key'] = urlhaus_auth_key
        
        # API endpoints and configurations
        self.apis = {
            'phish_tank': {
                'url': 'https://checkurl.phishtank.com/checkurl/',
                'free': True,
                'rate_limit': 1000  # requests per day
            },
            'urlhaus': {
                'url': 'https://urlhaus-api.abuse.ch/v1/url/',
                'free': True,
                'rate_limit': 1000,
                'requires_auth': True,
                'auth_key': None  # Will be set via environment variable
            }
        }
        
        # Local threat patterns
        self.threat_patterns = [
            r'bit\.ly|goo\.gl|tinyurl\.com',  # URL shorteners
            r'facebook.*login|fb.*login',     # Fake login pages
            r'bank.*verify|account.*secure',  # Banking scams
            r'free.*gift|win.*prize',         # Prize scams
            r'urgent.*action|immediate.*response',  # Urgency tactics
            r'myanmar.*bank|kbz.*verify',     # Myanmar-specific scams
            r'game.*hack|free.*diamonds',     # Gaming scams
            r'investment.*profit|money.*double'  # Investment scams
        ]
        
        # Myanmar-specific scam keywords
        self.myanmar_scam_keywords = [
            'kbz', 'ayeyarwady', 'cb', 'mab', 'uab', 'yoma', 'kanbawza',
            'myanmar', 'burma', 'yangon', 'mandalay', 'naypyidaw',
            'kyat', 'mmk', 'myanmar kyat', 'dollar', 'usd',
            'lottery', 'sweepstakes', 'inheritance', 'refund',
            'tax', 'customs', 'immigration', 'police', 'court'
        ]

    def analyze_url(self, url: str) -> Dict:
        """
        Comprehensive URL analysis using multiple detection methods
        """
        try:
            # Normalize URL
            normalized_url = self._normalize_url(url)
            
            # Initialize results
            results = {
                'url': normalized_url,
                'is_suspicious': False,
                'threat_level': 'safe',
                'detection_methods': [],
                'warnings': [],
                'confidence': 0.0,
                'analysis_time': time.time()
            }
            
            # Method 1: Local Database Check (FASTEST - Instant lookup)
            db_result = self.db.check_url_in_database(normalized_url)
            if db_result:
                results['is_suspicious'] = True
                results['threat_level'] = 'critical'
                results['detection_methods'].append('local_database')
                results['confidence'] += db_result['confidence']
                results['warnings'].append(f"🚨 Local DB: {db_result['threat_type']} - {db_result['source']}")
                
                # Log detection
                self.db.log_detection(normalized_url, results['threat_level'], 
                                    results['confidence'], results['detection_methods'], 
                                    results['is_suspicious'])
                
                # Generate response and return early for known threats
                results['confidence'] = min(results['confidence'], 1.0)
                results['message'] = self._generate_response_message(results)
                return results
            
            # Method 2: URLhaus API check (PRIMARY - Highest Priority)
            urlhaus_result = self._check_urlhaus(normalized_url)
            if urlhaus_result['is_malicious']:
                results['is_suspicious'] = True
                results['threat_level'] = 'critical'
                results['detection_methods'].append('urlhaus')
                results['confidence'] += 0.95
                results['warnings'].append(f"🚨 URLhaus: {urlhaus_result['details']}")
                
                # Add to database for future fast lookup
                self.db.add_user_report(normalized_url, f"Detected by URLhaus: {urlhaus_result['details']}")
                
                # If URLhaus detects it, we can skip other checks for efficiency
                # but still do host check for additional intelligence
                parsed_url = urlparse(normalized_url)
                if parsed_url.netloc:
                    host_result = self.check_urlhaus_host(parsed_url.netloc)
                    if host_result.get('success') and host_result.get('is_malicious'):
                        if 'urlhaus_host' not in results['detection_methods']:
                            results['detection_methods'].append('urlhaus_host')
                            results['confidence'] += 0.1  # Additional confidence
                            
                        url_count = host_result.get('url_count', 0)
                        results['warnings'].append(f"URLhaus Host: {url_count} malware URLs found on this domain")
                
                # Log detection
                self.db.log_detection(normalized_url, results['threat_level'], 
                                    results['confidence'], results['detection_methods'], 
                                    results['is_suspicious'])
                
                # Generate response and return early for critical threats
                results['confidence'] = min(results['confidence'], 1.0)
                results['message'] = self._generate_response_message(results)
                return results
            
            # Method 2: URLhaus host check (SECONDARY - Domain-level intelligence)
            parsed_url = urlparse(normalized_url)
            if parsed_url.netloc:
                host_result = self.check_urlhaus_host(parsed_url.netloc)
                if host_result.get('success') and host_result.get('is_malicious'):
                    results['is_suspicious'] = True
                    results['threat_level'] = 'high'
                    results['detection_methods'].append('urlhaus_host')
                    results['confidence'] += 0.85
                    
                    url_count = host_result.get('url_count', 0)
                    results['warnings'].append(f"⚠️ URLhaus Host: {url_count} malware URLs found on this domain")
            
            # Method 3: PhishTank API check (FALLBACK - Phishing-specific)
            phish_tank_result = self._check_phish_tank(normalized_url)
            if phish_tank_result['is_phishing']:
                results['is_suspicious'] = True
                if results['threat_level'] == 'safe':
                    results['threat_level'] = 'critical'
                elif results['threat_level'] == 'high':
                    results['threat_level'] = 'critical'
                results['detection_methods'].append('phish_tank')
                results['confidence'] += 0.8
                results['warnings'].append(f"PhishTank: {phish_tank_result['details']}")
            
            # Method 4: Pattern-based detection (FALLBACK - Local analysis)
            pattern_score = self._pattern_analysis(normalized_url)
            if pattern_score > 0.3:
                results['is_suspicious'] = True
                if results['threat_level'] == 'safe':
                    if pattern_score > 0.7:
                        results['threat_level'] = 'high'
                    else:
                        results['threat_level'] = 'medium'
                results['detection_methods'].append('pattern_analysis')
                results['confidence'] += pattern_score * 0.4  # Reduced weight as fallback
            
            # Method 5: URL structure analysis (FALLBACK - Technical analysis)
            structure_score = self._analyze_url_structure(normalized_url)
            if structure_score > 0.6:
                results['is_suspicious'] = True
                if results['threat_level'] == 'safe':
                    results['threat_level'] = 'medium'
                results['detection_methods'].append('url_structure')
                results['confidence'] += 0.2
            
            # Method 6: Myanmar-specific scam detection (FALLBACK - Local context)
            myanmar_score = self._detect_myanmar_scams(normalized_url)
            if myanmar_score > 0.7:
                results['is_suspicious'] = True
                if results['threat_level'] == 'safe':
                    results['threat_level'] = 'high'
                elif results['threat_level'] == 'medium':
                    results['threat_level'] = 'high'
                results['detection_methods'].append('myanmar_specific')
                results['confidence'] += 0.4
                results['warnings'].append("🇲🇲 Myanmar-specific scam pattern detected")
            
            # Cap confidence at 1.0
            results['confidence'] = min(results['confidence'], 1.0)
            
            # Generate response message
            results['message'] = self._generate_response_message(results)
            
            return results
            
        except Exception as e:
            logger.error(f"Error analyzing URL {url}: {str(e)}")
            return {
                'url': url,
                'is_suspicious': False,
                'threat_level': 'unknown',
                'error': str(e),
                'message': 'Unable to analyze this URL at the moment.'
            }

    def _normalize_url(self, url: str) -> str:
        """Normalize URL for consistent analysis"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Remove common tracking parameters
        tracking_params = ['utm_source', 'utm_medium', 'utm_campaign', 'ref', 'source']
        parsed = urlparse(url)
        query_params = parsed.query.split('&') if parsed.query else []
        filtered_params = [p for p in query_params if not any(tp in p for tp in tracking_params)]
        
        clean_query = '&'.join(filtered_params) if filtered_params else ''
        clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if clean_query:
            clean_url += f"?{clean_query}"
        
        return clean_url

    def _pattern_analysis(self, url: str) -> float:
        """Analyze URL for suspicious patterns"""
        score = 0.0
        url_lower = url.lower()
        
        # Check for URL shorteners
        if any(pattern in url_lower for pattern in ['bit.ly', 'goo.gl', 'tinyurl.com', 't.co']):
            score += 0.3
        
        # Check for suspicious keywords
        for pattern in self.threat_patterns:
            if re.search(pattern, url_lower, re.IGNORECASE):
                score += 0.2
        
        # Check for excessive special characters
        special_char_ratio = len(re.findall(r'[^a-zA-Z0-9./-]', url)) / len(url)
        if special_char_ratio > 0.3:
            score += 0.2
        
        # Check for suspicious TLDs
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq']
        if any(tld in url_lower for tld in suspicious_tlds):
            score += 0.4
        
        # Check for Myanmar-specific scam patterns
        myanmar_patterns = [
            r'kbz.*verify|kbz.*secure',
            r'myanmar.*bank.*login',
            r'lottery.*myanmar|sweepstakes.*burma',
            r'inheritance.*myanmar|refund.*kyat',
            r'police.*myanmar|court.*yangon'
        ]
        
        for pattern in myanmar_patterns:
            if re.search(pattern, url_lower, re.IGNORECASE):
                score += 0.5
        
        return min(score, 1.0)

    def _check_phish_tank(self, url: str) -> Dict:
        """Check URL against PhishTank database"""
        try:
            # PhishTank API call
            data = {
                'url': url,
                'format': 'json'
            }
            
            response = self.session.post(
                self.apis['phish_tank']['url'],
                data=data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'is_phishing': result.get('in_database', False),
                    'details': result.get('phish_id', 'Unknown'),
                    'verified': result.get('verified', False)
                }
            
        except Exception as e:
            logger.warning(f"PhishTank API error: {str(e)}")
        
        return {'is_phishing': False, 'details': 'API unavailable', 'verified': False}

    def _check_urlhaus(self, url: str) -> Dict:
        """Check URL against URLhaus malware database (PRIMARY METHOD)"""
        try:
            # Check if we have auth key
            auth_key = self.apis['urlhaus'].get('auth_key')
            if not auth_key:
                logger.info("URLhaus API not configured - falling back to other detection methods")
                return {'is_malicious': False, 'details': 'URLhaus not configured', 'threat': None, 'status': 'not_configured'}
            
            # Prepare headers with auth key
            headers = {
                'Auth-Key': auth_key,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            # Prepare data for POST request
            data = {
                'url': url
            }
            
            response = self.session.post(
                self.apis['urlhaus']['url'],
                headers=headers,
                data=data,
                timeout=10  # Reduced timeout for faster fallback
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('query_status') == 'ok':
                    # URL found in database - CRITICAL THREAT
                    url_info = result.get('urls', [{}])[0]
                    
                    return {
                        'is_malicious': True,
                        'details': f"🚨 MALWARE DETECTED - Threat: {url_info.get('threat', 'unknown')}",
                        'threat': url_info.get('threat'),
                        'url_status': url_info.get('url_status'),
                        'tags': url_info.get('tags', []),
                        'blacklists': url_info.get('blacklists', {}),
                        'date_added': url_info.get('date_added'),
                        'status': 'detected'
                    }
                elif result.get('query_status') == 'no_results':
                    # URL not found in database - SAFE
                    return {
                        'is_malicious': False,
                        'details': '✅ URL not found in malware database',
                        'threat': None,
                        'status': 'clean'
                    }
                else:
                    # API error - fallback to other methods
                    logger.warning(f"URLhaus API error: {result.get('query_status')}")
                    return {
                        'is_malicious': False,
                        'details': f"API error: {result.get('query_status')}",
                        'threat': None,
                        'status': 'api_error'
                    }
            
            elif response.status_code == 401:
                # Invalid auth key
                logger.error("URLhaus API: Invalid authentication key")
                return {
                    'is_malicious': False,
                    'details': 'Invalid auth key - check configuration',
                    'threat': None,
                    'status': 'auth_error'
                }
            
            elif response.status_code == 429:
                # Rate limit exceeded
                logger.warning("URLhaus API: Rate limit exceeded")
                return {
                    'is_malicious': False,
                    'details': 'Rate limit exceeded - falling back to other methods',
                    'threat': None,
                    'status': 'rate_limited'
                }
            
            else:
                # Other HTTP errors
                logger.warning(f"URLhaus API HTTP error: {response.status_code}")
                return {
                    'is_malicious': False,
                    'details': f'HTTP error {response.status_code} - falling back to other methods',
                    'threat': None,
                    'status': 'http_error'
                }
            
        except requests.exceptions.Timeout:
            logger.warning("URLhaus API timeout - falling back to other methods")
            return {
                'is_malicious': False,
                'details': 'API timeout - falling back to other methods',
                'threat': None,
                'status': 'timeout'
            }
        except requests.exceptions.ConnectionError:
            logger.warning("URLhaus API connection error - falling back to other methods")
            return {
                'is_malicious': False,
                'details': 'Connection error - falling back to other methods',
                'threat': None,
                'status': 'connection_error'
            }
        except Exception as e:
            logger.warning(f"URLhaus API unexpected error: {str(e)}")
            return {
                'is_malicious': False,
                'details': f'Unexpected error: {str(e)} - falling back to other methods',
                'threat': None,
                'status': 'error'
            }

    def get_recent_urlhaus_urls(self, limit: int = 10) -> Dict:
        """Get recent malware URLs from URLhaus"""
        try:
            auth_key = self.apis['urlhaus'].get('auth_key')
            if not auth_key:
                return {'success': False, 'error': 'No URLhaus auth key'}
            
            headers = {'Auth-Key': auth_key}
            
            if limit <= 1000:
                url = f"https://urlhaus-api.abuse.ch/v1/urls/recent/limit/{limit}/"
            else:
                url = "https://urlhaus-api.abuse.ch/v1/urls/recent/"
            
            response = self.session.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('query_status') == 'ok':
                    return {
                        'success': True,
                        'urls': data.get('urls', []),
                        'count': len(data.get('urls', [])),
                        'timestamp': datetime.now().isoformat()
                    }
            
            return {'success': False, 'error': 'API request failed'}
            
        except Exception as e:
            logger.error(f"Error getting recent URLhaus URLs: {str(e)}")
            return {'success': False, 'error': str(e)}

    def get_recent_urlhaus_payloads(self, limit: int = 10) -> Dict:
        """Get recent malware payloads from URLhaus"""
        try:
            auth_key = self.apis['urlhaus'].get('auth_key')
            if not auth_key:
                return {'success': False, 'error': 'No URLhaus auth key'}
            
            headers = {'Auth-Key': auth_key}
            
            if limit <= 1000:
                url = f"https://urlhaus-api.abuse.ch/v1/payloads/recent/limit/{limit}/"
            else:
                url = "https://urlhaus-api.abuse.ch/v1/payloads/recent/"
            
            response = self.session.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('query_status') == 'ok':
                    return {
                        'success': True,
                        'payloads': data.get('payloads', []),
                        'count': len(data.get('payloads', [])),
                        'timestamp': datetime.now().isoformat()
                    }
            
            return {'success': False, 'error': 'API request failed'}
            
        except Exception as e:
            logger.error(f"Error getting recent URLhaus payloads: {str(e)}")
            return {'success': False, 'error': str(e)}

    def check_urlhaus_host(self, host: str) -> Dict:
        """Check host information in URLhaus"""
        try:
            auth_key = self.apis['urlhaus'].get('auth_key')
            if not auth_key:
                return {'success': False, 'error': 'No URLhaus auth key'}
            
            headers = {
                'Auth-Key': auth_key,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {'host': host}
            
            response = self.session.post(
                'https://urlhaus-api.abuse.ch/v1/host/',
                headers=headers,
                data=data,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('query_status') == 'ok':
                    return {
                        'success': True,
                        'host_info': result,
                        'is_malicious': True,
                        'url_count': result.get('url_count', 0),
                        'blacklists': result.get('blacklists', {}),
                        'firstseen': result.get('firstseen')
                    }
                elif result.get('query_status') == 'no_results':
                    return {
                        'success': True,
                        'is_malicious': False,
                        'host_info': None
                    }
            
            return {'success': False, 'error': 'API request failed'}
            
        except Exception as e:
            logger.error(f"Error checking URLhaus host: {str(e)}")
            return {'success': False, 'error': str(e)}

    def search_urlhaus_tag(self, tag: str) -> Dict:
        """Search for URLs by tag in URLhaus"""
        try:
            auth_key = self.apis['urlhaus'].get('auth_key')
            if not auth_key:
                return {'success': False, 'error': 'No URLhaus auth key'}
            
            headers = {
                'Auth-Key': auth_key,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {'tag': tag}
            
            response = self.session.post(
                'https://urlhaus-api.abuse.ch/v1/tag/',
                headers=headers,
                data=data,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('query_status') == 'ok':
                    return {
                        'success': True,
                        'tag_info': result,
                        'url_count': result.get('url_count', 0),
                        'urls': result.get('urls', []),
                        'firstseen': result.get('firstseen'),
                        'lastseen': result.get('lastseen')
                    }
                elif result.get('query_status') == 'no_results':
                    return {
                        'success': True,
                        'tag_info': None,
                        'url_count': 0
                    }
            
            return {'success': False, 'error': 'API request failed'}
            
        except Exception as e:
            logger.error(f"Error searching URLhaus tag: {str(e)}")
            return {'success': False, 'error': str(e)}

    def get_urlhaus_intelligence_summary(self) -> Dict:
        """Get intelligence summary from URLhaus"""
        try:
            # Get recent URLs and payloads for threat intelligence
            recent_urls = self.get_recent_urlhaus_urls(limit=50)
            recent_payloads = self.get_recent_urlhaus_payloads(limit=20)
            
            if not recent_urls.get('success') or not recent_payloads.get('success'):
                return {'success': False, 'error': 'Failed to fetch threat intelligence'}
            
            # Analyze threat landscape
            threats = {}
            domains = {}
            tags = {}
            
            # Process URLs
            for url_data in recent_urls.get('urls', []):
                threat_type = url_data.get('threat', 'unknown')
                threats[threat_type] = threats.get(threat_type, 0) + 1
                
                host = url_data.get('host', '')
                if host:
                    domains[host] = domains.get(host, 0) + 1
                
                for tag in url_data.get('tags', []):
                    tags[tag] = tags.get(tag, 0) + 1
            
            # Process payloads
            file_types = {}
            signatures = {}
            
            for payload in recent_payloads.get('payloads', []):
                file_type = payload.get('file_type', 'unknown')
                file_types[file_type] = file_types.get(file_type, 0) + 1
                
                signature = payload.get('signature')
                if signature:
                    signatures[signature] = signatures.get(signature, 0) + 1
            
            return {
                'success': True,
                'summary': {
                    'threats': dict(sorted(threats.items(), key=lambda x: x[1], reverse=True)[:10]),
                    'top_domains': dict(sorted(domains.items(), key=lambda x: x[1], reverse=True)[:10]),
                    'top_tags': dict(sorted(tags.items(), key=lambda x: x[1], reverse=True)[:10]),
                    'file_types': dict(sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:5]),
                    'signatures': dict(sorted(signatures.items(), key=lambda x: x[1], reverse=True)[:5])
                },
                'stats': {
                    'recent_urls': len(recent_urls.get('urls', [])),
                    'recent_payloads': len(recent_payloads.get('payloads', [])),
                    'total_threats': sum(threats.values()),
                    'unique_domains': len(domains),
                    'unique_tags': len(tags)
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting URLhaus intelligence: {str(e)}")
            return {'success': False, 'error': str(e)}

    def _analyze_url_structure(self, url: str) -> float:
        """Analyze URL structure for suspicious characteristics"""
        score = 0.0
        parsed = urlparse(url)
        
        # Check domain length
        if len(parsed.netloc) > 50:
            score += 0.2
        
        # Check for IP addresses instead of domains
        if re.match(r'\d+\.\d+\.\d+\.\d+', parsed.netloc):
            score += 0.4
        
        # Check for suspicious TLDs
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq']
        if any(tld in parsed.netloc for tld in suspicious_tlds):
            score += 0.3
        
        # Check for excessive subdomains
        subdomain_count = len(parsed.netloc.split('.')) - 1
        if subdomain_count > 3:
            score += 0.2
        
        return min(score, 1.0)

    def _detect_myanmar_scams(self, url: str) -> float:
        """Detect Myanmar-specific scam patterns"""
        score = 0.0
        url_lower = url.lower()
        
        # Check for Myanmar-specific keywords
        myanmar_matches = sum(1 for keyword in self.myanmar_scam_keywords if keyword in url_lower)
        if myanmar_matches > 0:
            score += 0.3
        
        # Check for common Myanmar scam patterns
        myanmar_patterns = [
            r'kbz.*verify|kbz.*secure',
            r'myanmar.*bank.*login',
            r'lottery.*myanmar|sweepstakes.*burma',
            r'inheritance.*myanmar|refund.*kyat',
            r'police.*myanmar|court.*yangon'
        ]
        
        for pattern in myanmar_patterns:
            if re.search(pattern, url_lower, re.IGNORECASE):
                score += 0.4
        
        return min(score, 1.0)

    def get_detection_status(self) -> Dict:
        """Get the status of all detection methods"""
        status = {
            'urlhaus': {
                'enabled': bool(self.apis['urlhaus'].get('auth_key')),
                'priority': 'PRIMARY',
                'description': 'URLhaus malware database (most accurate)'
            },
            'phish_tank': {
                'enabled': True,
                'priority': 'FALLBACK',
                'description': 'PhishTank phishing database'
            },
            'pattern_analysis': {
                'enabled': True,
                'priority': 'FALLBACK',
                'description': 'Local pattern matching'
            },
            'url_structure': {
                'enabled': True,
                'priority': 'FALLBACK',
                'description': 'URL structure analysis'
            },
            'myanmar_specific': {
                'enabled': True,
                'priority': 'FALLBACK',
                'description': 'Myanmar-specific scam detection'
            }
        }
        
        return status

    def initialize_database(self):
        """Initialize database with default scam URLs"""
        try:
            self.db.add_default_scam_urls()
            logger.info("Database initialized with default scam URLs")
            return True
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
            return False

    def get_database_stats(self) -> Dict:
        """Get database statistics"""
        return self.db.get_database_stats()

    def _generate_response_message(self, results: Dict) -> str:
        """Generate user-friendly response message with detection method priority"""
        detection_methods = results.get('detection_methods', [])
        
        if results['threat_level'] == 'critical':
            if 'urlhaus' in detection_methods:
                return "🚨 CRITICAL WARNING: This link has been confirmed as MALWARE by URLhaus! Do NOT click it. Report it immediately."
            elif 'phish_tank' in detection_methods:
                return "🚨 CRITICAL WARNING: This link has been confirmed as a phishing scam! Do NOT click it. Report it immediately."
            else:
                return "🚨 CRITICAL WARNING: This link has been confirmed as dangerous! Do NOT click it. Report it immediately."
        
        elif results['threat_level'] == 'high':
            if 'urlhaus_host' in detection_methods:
                return "⚠️ HIGH RISK: This domain hosts multiple malware URLs. We strongly recommend avoiding this link."
            elif 'myanmar_specific' in detection_methods:
                return "⚠️ HIGH RISK: This link matches Myanmar-specific scam patterns. We recommend avoiding it and reporting it."
            else:
                return "⚠️ HIGH RISK: This link shows strong signs of being a scam. We recommend avoiding it and reporting it."
        
        elif results['threat_level'] == 'medium':
            if 'pattern_analysis' in detection_methods:
                return "⚠️ SUSPICIOUS: This link has concerning characteristics (URL shortener, suspicious patterns). Please be very careful and verify the source."
            else:
                return "⚠️ SUSPICIOUS: This link has some concerning characteristics. Please be very careful and verify the source."
        
        elif results['threat_level'] == 'safe':
            if 'urlhaus' in detection_methods:
                return "✅ SAFE: This link has been checked against URLhaus malware database and appears safe, but always remain cautious."
            else:
                return "✅ SAFE: This link appears to be safe, but always remain cautious and verify the source."
        
        else:
            return "❓ UNKNOWN: We couldn't determine the safety of this link. Please use caution and verify the source."

    def get_safety_tips(self) -> List[str]:
        """Get safety tips for users"""
        return [
            "Never click on links from unknown senders",
            "Check the URL carefully - look for misspellings",
            "Don't share personal information on suspicious websites",
            "Enable two-factor authentication on your accounts",
            "Keep your software and apps updated",
            "Be suspicious of urgent requests for money or information",
            "Verify bank communications directly with your bank",
            "Don't trust offers that seem too good to be true"
        ]

    def report_scam(self, url: str, description: str, user_id: str = None) -> Dict:
        """Report a scam URL for community protection"""
        try:
            # Add to database
            result = self.db.add_user_report(url, description, user_id)
            
            if result['success']:
                return {
                    'success': True,
                    'message': 'Scam reported successfully. Thank you for helping protect others!',
                    'report_id': result['report_id'],
                    'url_hash': result['url_hash']
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"Error reporting scam: {str(e)}")
            return {
                'success': False,
                'message': 'Failed to report scam. Please try again.'
            }

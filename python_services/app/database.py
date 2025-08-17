import sqlite3
import hashlib
import time
import json
import logging
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class PhishGuardDatabase:
    """Database for storing scam URLs and user reports"""
    
    def __init__(self, db_path: str = "phishguard.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Table for known scam URLs (default + user-reported)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS scam_urls (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        url_hash TEXT UNIQUE NOT NULL,
                        original_url TEXT NOT NULL,
                        domain TEXT NOT NULL,
                        threat_type TEXT NOT NULL,
                        confidence REAL DEFAULT 0.8,
                        source TEXT NOT NULL,
                        tags TEXT,
                        first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        report_count INTEGER DEFAULT 1,
                        is_active BOOLEAN DEFAULT 1
                    )
                ''')
                
                # Table for user reports
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_reports (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        url_hash TEXT NOT NULL,
                        original_url TEXT NOT NULL,
                        description TEXT,
                        user_id TEXT,
                        report_type TEXT DEFAULT 'scam',
                        status TEXT DEFAULT 'pending',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        reviewed_at TIMESTAMP,
                        reviewed_by TEXT
                    )
                ''')
                
                # Table for detection history (for analytics)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS detection_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        url_hash TEXT NOT NULL,
                        original_url TEXT NOT NULL,
                        threat_level TEXT NOT NULL,
                        confidence REAL NOT NULL,
                        detection_methods TEXT,
                        is_suspicious BOOLEAN NOT NULL,
                        response_time_ms INTEGER,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Table for API status tracking
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS api_status (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        api_name TEXT NOT NULL,
                        status TEXT NOT NULL,
                        last_check TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        error_message TEXT,
                        response_time_ms INTEGER
                    )
                ''')
                
                # Create indexes for faster queries
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_url_hash ON scam_urls(url_hash)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_domain ON scam_urls(domain)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_source ON scam_urls(source)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_active ON scam_urls(is_active)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_detection_url ON detection_history(url_hash)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_detection_time ON detection_history(timestamp)')
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Database initialization error: {str(e)}")
            raise
    
    def add_default_scam_urls(self):
        """Add default scam URLs to database"""
        default_scams = [
            # Myanmar-specific scams
            ("https://kbz-verify-account.secure-banking.cf", "phishing", "kbz_bank", ["myanmar", "bank", "kbz"]),
            ("https://myanmar-lottery-winner.com", "scam", "lottery", ["myanmar", "lottery", "fake"]),
            ("https://kbz-bank-secure-login.tk", "phishing", "kbz_bank", ["myanmar", "bank", "kbz"]),
            ("https://myanmar-inheritance-claim.ml", "scam", "inheritance", ["myanmar", "inheritance", "fake"]),
            ("https://police-myanmar-court-case.cf", "scam", "police", ["myanmar", "police", "court"]),
            
            # Common phishing patterns
            ("https://facebook-login-secure.com", "phishing", "facebook", ["social", "login", "fake"]),
            ("https://google-account-verify.tk", "phishing", "google", ["google", "account", "fake"]),
            ("https://paypal-secure-login.ml", "phishing", "paypal", ["payment", "paypal", "fake"]),
            ("https://amazon-account-verify.cf", "phishing", "amazon", ["shopping", "amazon", "fake"]),
            
            # Malware distribution
            ("https://free-software-download.tk", "malware", "software", ["malware", "fake_software"]),
            ("https://cracked-games-free.ml", "malware", "games", ["malware", "piracy", "fake"]),
            ("https://adult-content-free.cf", "malware", "adult", ["malware", "adult", "fake"]),
        ]
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for url, threat_type, source, tags in default_scams:
                    url_hash = self._hash_url(url)
                    domain = urlparse(url).netloc
                    tags_json = json.dumps(tags)
                    
                    cursor.execute('''
                        INSERT OR IGNORE INTO scam_urls 
                        (url_hash, original_url, domain, threat_type, source, tags, confidence)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (url_hash, url, domain, threat_type, source, tags_json, 0.9))
                
                conn.commit()
                logger.info(f"Added {len(default_scams)} default scam URLs")
                
        except Exception as e:
            logger.error(f"Error adding default scam URLs: {str(e)}")
    
    def check_url_in_database(self, url: str) -> Optional[Dict]:
        """Check if URL exists in local database"""
        try:
            url_hash = self._hash_url(url)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT url_hash, original_url, domain, threat_type, confidence, 
                           source, tags, first_seen, report_count
                    FROM scam_urls 
                    WHERE url_hash = ? AND is_active = 1
                ''', (url_hash,))
                
                result = cursor.fetchone()
                
                if result:
                    # Update last_seen and report_count
                    cursor.execute('''
                        UPDATE scam_urls 
                        SET last_seen = CURRENT_TIMESTAMP, report_count = report_count + 1
                        WHERE url_hash = ?
                    ''', (url_hash,))
                    
                    conn.commit()
                    
                    return {
                        'is_malicious': True,
                        'url_hash': result[0],
                        'original_url': result[1],
                        'domain': result[2],
                        'threat_type': result[3],
                        'confidence': result[4],
                        'source': result[5],
                        'tags': json.loads(result[6]) if result[6] else [],
                        'first_seen': result[7],
                        'report_count': result[8],
                        'detection_method': 'local_database'
                    }
                
                return None
                
        except Exception as e:
            logger.error(f"Database check error: {str(e)}")
            return None
    
    def add_user_report(self, url: str, description: str, user_id: str = None) -> Dict:
        """Add user report to database"""
        try:
            url_hash = self._hash_url(url)
            domain = urlparse(url).netloc
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Add to user_reports table
                cursor.execute('''
                    INSERT INTO user_reports (url_hash, original_url, description, user_id)
                    VALUES (?, ?, ?, ?)
                ''', (url_hash, url, description, user_id))
                
                # Add to scam_urls table if not exists
                cursor.execute('''
                    INSERT OR IGNORE INTO scam_urls 
                    (url_hash, original_url, domain, threat_type, source, confidence)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (url_hash, url, domain, 'user_reported', 'user_report', 0.7))
                
                # If URL already exists, update report count
                cursor.execute('''
                    UPDATE scam_urls 
                    SET report_count = report_count + 1, last_seen = CURRENT_TIMESTAMP
                    WHERE url_hash = ?
                ''', (url_hash,))
                
                conn.commit()
                
                return {
                    'success': True,
                    'message': 'Report added successfully',
                    'report_id': cursor.lastrowid,
                    'url_hash': url_hash
                }
                
        except Exception as e:
            logger.error(f"Error adding user report: {str(e)}")
            return {
                'success': False,
                'message': f'Error adding report: {str(e)}'
            }
    
    def log_detection(self, url: str, threat_level: str, confidence: float, 
                     detection_methods: List[str], is_suspicious: bool, 
                     response_time_ms: int = None):
        """Log detection result for analytics"""
        try:
            url_hash = self._hash_url(url)
            methods_json = json.dumps(detection_methods)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO detection_history 
                    (url_hash, original_url, threat_level, confidence, detection_methods, 
                     is_suspicious, response_time_ms)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (url_hash, url, threat_level, confidence, methods_json, 
                     is_suspicious, response_time_ms))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error logging detection: {str(e)}")
    
    def update_api_status(self, api_name: str, status: str, error_message: str = None, 
                         response_time_ms: int = None):
        """Update API status for monitoring"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO api_status 
                    (api_name, status, last_check, error_message, response_time_ms)
                    VALUES (?, ?, CURRENT_TIMESTAMP, ?, ?)
                ''', (api_name, status, error_message, response_time_ms))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error updating API status: {str(e)}")
    
    def get_database_stats(self) -> Dict:
        """Get database statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total scam URLs
                cursor.execute('SELECT COUNT(*) FROM scam_urls WHERE is_active = 1')
                total_scams = cursor.fetchone()[0]
                
                # URLs by source
                cursor.execute('''
                    SELECT source, COUNT(*) 
                    FROM scam_urls 
                    WHERE is_active = 1 
                    GROUP BY source
                ''')
                by_source = dict(cursor.fetchall())
                
                # Recent detections (last 24 hours)
                cursor.execute('''
                    SELECT COUNT(*) 
                    FROM detection_history 
                    WHERE timestamp > datetime('now', '-1 day')
                ''')
                recent_detections = cursor.fetchone()[0]
                
                # User reports (pending review)
                cursor.execute('''
                    SELECT COUNT(*) 
                    FROM user_reports 
                    WHERE status = 'pending'
                ''')
                pending_reports = cursor.fetchone()[0]
                
                return {
                    'total_scam_urls': total_scams,
                    'by_source': by_source,
                    'recent_detections_24h': recent_detections,
                    'pending_user_reports': pending_reports
                }
                
        except Exception as e:
            logger.error(f"Error getting database stats: {str(e)}")
            return {}
    
    def search_scams_by_domain(self, domain: str) -> List[Dict]:
        """Search for scams by domain"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT original_url, threat_type, confidence, source, 
                           first_seen, report_count
                    FROM scam_urls 
                    WHERE domain LIKE ? AND is_active = 1
                    ORDER BY report_count DESC, first_seen DESC
                ''', (f'%{domain}%',))
                
                results = []
                for row in cursor.fetchall():
                    results.append({
                        'url': row[0],
                        'threat_type': row[1],
                        'confidence': row[2],
                        'source': row[3],
                        'first_seen': row[4],
                        'report_count': row[5]
                    })
                
                return results
                
        except Exception as e:
            logger.error(f"Error searching by domain: {str(e)}")
            return []
    
    def cleanup_old_data(self, days: int = 30):
        """Clean up old detection history data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    DELETE FROM detection_history 
                    WHERE timestamp < datetime('now', '-{} days')
                '''.format(days))
                
                deleted_count = cursor.rowcount
                conn.commit()
                
                logger.info(f"Cleaned up {deleted_count} old detection records")
                
        except Exception as e:
            logger.error(f"Error cleaning up old data: {str(e)}")
    
    def _hash_url(self, url: str) -> str:
        """Create hash for URL (normalized)"""
        # Normalize URL for consistent hashing
        normalized = url.lower().strip()
        if not normalized.startswith(('http://', 'https://')):
            normalized = 'https://' + normalized
        
        return hashlib.sha256(normalized.encode()).hexdigest()
    
    def backup_database(self, backup_path: str = None):
        """Create database backup"""
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"phishguard_backup_{timestamp}.db"
        
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            logger.info(f"Database backed up to {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Backup error: {str(e)}")
            return None 
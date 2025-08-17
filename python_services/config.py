#!/usr/bin/env python3
"""
PhishGuard Configuration
"""

import os
from typing import Optional

class Config:
    """Configuration class for PhishGuard"""
    
    # URLhaus API Configuration
    URLHAUS_AUTH_KEY: Optional[str] = os.getenv('URLHAUS_AUTH_KEY')
    
    # PhishTank API Configuration (no key required)
    PHISHTANK_ENABLED: bool = True
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Detection Thresholds
    PATTERN_THRESHOLD: float = 0.3
    STRUCTURE_THRESHOLD: float = 0.6
    MYANMAR_THRESHOLD: float = 0.7
    
    # API Timeouts
    REQUEST_TIMEOUT: int = 15
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # Security
    CORS_ORIGINS: list = [
        "http://localhost:3000",  # React dev server
        "http://localhost:8000",  # FastAPI server
        "https://phishguard.mm",  # Production domain
    ]
    
    # Database (for future use)
    DATABASE_URL: Optional[str] = os.getenv('DATABASE_URL')
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        issues = []
        
        if not cls.URLHAUS_AUTH_KEY:
            issues.append("URLHAUS_AUTH_KEY not set (URLhaus API will be disabled)")
        
        if cls.RATE_LIMIT_PER_MINUTE <= 0:
            issues.append("RATE_LIMIT_PER_MINUTE must be positive")
        
        if cls.REQUEST_TIMEOUT <= 0:
            issues.append("REQUEST_TIMEOUT must be positive")
        
        if issues:
            print("⚠️  Configuration issues found:")
            for issue in issues:
                print(f"   • {issue}")
            return False
        
        return True
    
    @classmethod
    def print_config(cls):
        """Print current configuration"""
        print("🔧 PhishGuard Configuration:")
        print(f"   URLhaus Auth Key: {'✅ Set' if cls.URLHAUS_AUTH_KEY else '❌ Not set'}")
        print(f"   PhishTank Enabled: {'✅ Yes' if cls.PHISHTANK_ENABLED else '❌ No'}")
        print(f"   Rate Limit (per minute): {cls.RATE_LIMIT_PER_MINUTE}")
        print(f"   Request Timeout: {cls.REQUEST_TIMEOUT}s")
        print(f"   Log Level: {cls.LOG_LEVEL}")
        print()

# Environment variable documentation
ENV_VARS = {
    'URLHAUS_AUTH_KEY': {
        'description': 'Authentication key for URLhaus API',
        'required': False,
        'how_to_get': 'Visit https://urlhaus.abuse.ch/api/ to get a free auth key'
    },
    'LOG_LEVEL': {
        'description': 'Logging level (DEBUG, INFO, WARNING, ERROR)',
        'required': False,
        'default': 'INFO'
    },
    'DATABASE_URL': {
        'description': 'Database connection URL (for future use)',
        'required': False,
        'default': None
    }
}

def print_env_help():
    """Print environment variable help"""
    print("🌍 Environment Variables:")
    print()
    for var, info in ENV_VARS.items():
        print(f"   {var}:")
        print(f"     Description: {info['description']}")
        print(f"     Required: {'Yes' if info['required'] else 'No'}")
        if 'default' in info:
            print(f"     Default: {info['default']}")
        if 'how_to_get' in info:
            print(f"     How to get: {info['how_to_get']}")
        print() 
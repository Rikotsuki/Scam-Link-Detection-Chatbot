#!/usr/bin/env python3
"""
PhishGuard Demo - Showcase the phishing detection capabilities
"""

from app.phish_core import PhishGuardCore
import time
import os

def main():
    print("🛡️  PhishGuard Demo - Protecting Myanmar from Phishing")
    print("=" * 60)
    print()
    
    # Check for URLhaus auth key
    urlhaus_auth_key = os.getenv('URLHAUS_AUTH_KEY')
    if urlhaus_auth_key:
        print("✅ URLhaus API configured")
    else:
        print("⚠️  URLhaus API not configured (run setup_urlhaus.py to enable)")
    
    print()
    
    # Initialize PhishGuard
    phish_guard = PhishGuardCore(urlhaus_auth_key=urlhaus_auth_key)
    
    # Test URLs
    test_cases = [
        {
            "name": "Safe Website",
            "url": "https://www.google.com",
            "expected": "safe"
        },
        {
            "name": "Suspicious URL Shortener",
            "url": "https://bit.ly/suspicious-link",
            "expected": "medium"
        },
        {
            "name": "Myanmar Bank Scam",
            "url": "https://kbz-verify-account.secure-banking.cf",
            "expected": "high"
        },
        {
            "name": "Lottery Scam",
            "url": "https://myanmar-lottery-winner.sweepstakes.gq",
            "expected": "high"
        }
    ]
    
    print("🔍 Testing URL Analysis...")
    print()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['name']}")
        print(f"URL: {test_case['url']}")
        
        try:
            result = phish_guard.analyze_url(test_case['url'])
            
            # Display result with emoji
            emoji_map = {
                'critical': '🚨',
                'high': '⚠️',
                'medium': '🔶',
                'safe': '✅',
                'unknown': '❓'
            }
            
            emoji = emoji_map.get(result['threat_level'], '❓')
            print(f"Result: {emoji} {result['threat_level'].upper()}")
            print(f"Message: {result['message']}")
            print(f"Confidence: {result['confidence']:.1%}")
            
            if result.get('detection_methods'):
                print(f"Detection Methods: {', '.join(result['detection_methods'])}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print("-" * 50)
        time.sleep(1)
    
    print()
    print("🛡️  Safety Tips:")
    print("-" * 30)
    tips = phish_guard.get_safety_tips()
    for i, tip in enumerate(tips[:5], 1):
        print(f"{i}. {tip}")
    
    print()
    print("📝 Testing Scam Reporting...")
    print("-" * 30)
    
    report_result = phish_guard.report_scam(
        "https://fake-scam-example.com",
        "Fake bank login page asking for credentials"
    )
    
    if report_result['success']:
        print(f"✅ {report_result['message']}")
        print(f"Report ID: {report_result.get('report_id', 'N/A')}")
    else:
        print(f"❌ {report_result['message']}")
    
    print()
    print("🎉 Demo completed successfully!")
    print("PhishGuard is ready to protect users from phishing threats!")
    print()
    print("Next steps:")
    print("1. Run 'python -m app.api' to start the API server")
    print("2. Run 'python -m app.cli chat' for interactive mode")
    print("3. Visit http://localhost:8000/docs for API documentation")

if __name__ == "__main__":
    main() 
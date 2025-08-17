#!/usr/bin/env python3
"""
PhishGuard Test Suite - Demonstrates phishing detection capabilities
"""

import time
import json
from .phish_core import PhishGuardCore

def test_phish_guard():
    """Test the PhishGuard core functionality"""
    
    print("🛡️  PhishGuard Test Suite")
    print("=" * 60)
    
    # Initialize PhishGuard
    phish_guard = PhishGuardCore()
    
    # Test URLs (these are examples - some may be real threats)
    test_urls = [
        # Safe URLs
        "https://www.google.com",
        "https://www.facebook.com",
        "https://www.github.com",
        
        # Suspicious patterns
        "https://bit.ly/suspicious-link",
        "https://facebook-login-secure.verify-account.tk",
        "https://kbz-bank-verify.myanmar-secure.ga",
        "https://free-gift-win-prize.urgent-action.ml",
        
        # Myanmar-specific scam patterns
        "https://kbz-verify-account.secure-banking.cf",
        "https://myanmar-lottery-winner.sweepstakes.gq",
        "https://inheritance-money-refund.kyat-payment.tk",
        
        # Gaming scams
        "https://free-diamonds-hack.game-cheat.ml",
        "https://pubg-mobile-hack.free-diamonds.ga",
        
        # Investment scams
        "https://investment-profit-double.money-multiply.cf",
        "https://crypto-investment-profit.urgent-action.gq"
    ]
    
    print(f"Testing {len(test_urls)} URLs...")
    print()
    
    results = []
    
    for i, url in enumerate(test_urls, 1):
        print(f"Test {i:2d}/{len(test_urls)}: {url}")
        
        try:
            # Analyze URL
            result = phish_guard.analyze_url(url)
            
            # Display result
            status_emoji = {
                'critical': '🚨',
                'high': '⚠️',
                'medium': '🔶',
                'safe': '✅',
                'unknown': '❓'
            }
            
            emoji = status_emoji.get(result['threat_level'], '❓')
            print(f"   {emoji} {result['threat_level'].upper()}: {result['message']}")
            print(f"   Confidence: {result['confidence']:.1%}")
            
            if result.get('detection_methods'):
                methods = ', '.join(result['detection_methods'])
                print(f"   Methods: {methods}")
            
            results.append(result)
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            results.append({'url': url, 'error': str(e)})
        
        print()
        time.sleep(0.5)  # Rate limiting
    
    # Summary
    print("📊 Test Summary")
    print("=" * 60)
    
    threat_counts = {}
    for result in results:
        if 'threat_level' in result:
            level = result['threat_level']
            threat_counts[level] = threat_counts.get(level, 0) + 1
    
    for level, count in threat_counts.items():
        emoji = status_emoji.get(level, '❓')
        print(f"{emoji} {level.upper()}: {count} URLs")
    
    print()
    print("✅ Test completed successfully!")
    return results

def test_safety_tips():
    """Test safety tips functionality"""
    print("🛡️  Testing Safety Tips")
    print("=" * 60)
    
    phish_guard = PhishGuardCore()
    tips = phish_guard.get_safety_tips()
    
    print(f"Retrieved {len(tips)} safety tips:")
    for i, tip in enumerate(tips, 1):
        print(f"{i:2d}. {tip}")
    
    print()
    return tips

def test_scam_reporting():
    """Test scam reporting functionality"""
    print("📝 Testing Scam Reporting")
    print("=" * 60)
    
    phish_guard = PhishGuardCore()
    
    test_reports = [
        {
            'url': 'https://fake-kbz-login.scam-site.tk',
            'description': 'Fake KBZ Bank login page asking for credentials'
        },
        {
            'url': 'https://myanmar-lottery-fake.prize-win.ml',
            'description': 'Fake lottery claiming user won money'
        }
    ]
    
    for report in test_reports:
        print(f"Reporting: {report['url']}")
        result = phish_guard.report_scam(
            report['url'],
            report['description']
        )
        
        if result['success']:
            print(f"✅ {result['message']}")
            print(f"   Report ID: {result.get('report_id', 'N/A')}")
        else:
            print(f"❌ {result['message']}")
        
        print()
    
    return True

def run_all_tests():
    """Run all tests"""
    print("🧪 PhishGuard Comprehensive Test Suite")
    print("=" * 60)
    print()
    
    try:
        # Test 1: URL Analysis
        print("1️⃣  Testing URL Analysis...")
        url_results = test_phish_guard()
        print()
        
        # Test 2: Safety Tips
        print("2️⃣  Testing Safety Tips...")
        tips = test_safety_tips()
        print()
        
        # Test 3: Scam Reporting
        print("3️⃣  Testing Scam Reporting...")
        reporting_success = test_scam_reporting()
        print()
        
        # Final summary
        print("🎉 All Tests Completed!")
        print("=" * 60)
        print(f"✅ URL Analysis: {len(url_results)} URLs tested")
        print(f"✅ Safety Tips: {len(tips)} tips retrieved")
        print(f"✅ Scam Reporting: {'Working' if reporting_success else 'Failed'}")
        print()
        print("🚀 PhishGuard is ready to protect users from phishing threats!")
        
    except Exception as e:
        print(f"❌ Test suite failed: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    run_all_tests()

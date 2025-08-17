#!/usr/bin/env python3
"""
PhishGuard URLhaus Integration Demo
Showcases comprehensive URLhaus API capabilities
"""

import os
import time
from app.phish_core import PhishGuardCore

def main():
    print("🛡️  PhishGuard URLhaus Integration Demo")
    print("=" * 60)
    print()
    
    # Check for URLhaus auth key
    urlhaus_auth_key = os.getenv('URLHAUS_AUTH_KEY')
    if not urlhaus_auth_key or urlhaus_auth_key == 'your_auth_key_here':
        print("❌ URLhaus Auth Key not configured!")
        print("Please follow these steps:")
        print("1. Get a free auth key from: https://urlhaus.abuse.ch/api/")
        print("2. Edit the .env file and replace 'your_auth_key_here' with your actual key")
        print("3. Run this demo again")
        print()
        print("For now, showing local detection capabilities...")
        urlhaus_auth_key = None
    else:
        print("✅ URLhaus API configured")
    
    print()
    
    # Initialize PhishGuard
    phish_guard = PhishGuardCore(urlhaus_auth_key=urlhaus_auth_key)
    
    # Demo 1: URL Analysis with URLhaus
    print("🔍 Demo 1: Enhanced URL Analysis")
    print("-" * 40)
    
    test_urls = [
        "https://www.google.com",
        "https://bit.ly/suspicious-link",
        "https://kbz-verify-account.secure-banking.cf",
        "https://malware.example.com"
    ]
    
    for url in test_urls:
        print(f"\nAnalyzing: {url}")
        result = phish_guard.analyze_url(url)
        
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
            methods = ', '.join(result['detection_methods'])
            print(f"Methods: {methods}")
        
        if result.get('warnings'):
            for warning in result['warnings']:
                print(f"Warning: {warning}")
        
        time.sleep(1)
    
    if not urlhaus_auth_key:
        print("\n⚠️  URLhaus features not available without auth key")
        return
    
    # Demo 2: Recent Threats Intelligence
    print("\n\n📊 Demo 2: Recent Threats Intelligence")
    print("-" * 40)
    
    recent_urls = phish_guard.get_recent_urlhaus_urls(limit=5)
    if recent_urls.get('success'):
        print(f"Found {recent_urls.get('count', 0)} recent malware URLs:")
        for i, url_data in enumerate(recent_urls.get('urls', []), 1):
            url = url_data.get('url', 'N/A')
            threat = url_data.get('threat', 'unknown')
            status = url_data.get('url_status', 'unknown')
            tags = ', '.join(url_data.get('tags', [])[:3])  # First 3 tags
            
            status_emoji = '🔴' if status == 'online' else '⚫'
            print(f"{i}. {status_emoji} {threat.upper()}")
            print(f"   URL: {url[:60]}{'...' if len(url) > 60 else ''}")
            print(f"   Tags: {tags}")
            print()
    else:
        print(f"❌ {recent_urls.get('error', 'Failed to get recent threats')}")
    
    # Demo 3: Threat Intelligence Summary
    print("\n📈 Demo 3: Threat Intelligence Summary")
    print("-" * 40)
    
    intelligence = phish_guard.get_urlhaus_intelligence_summary()
    if intelligence.get('success'):
        summary = intelligence.get('summary', {})
        stats = intelligence.get('stats', {})
        
        print(f"📊 Statistics:")
        print(f"   Recent URLs: {stats.get('recent_urls', 0)}")
        print(f"   Recent Payloads: {stats.get('recent_payloads', 0)}")
        print(f"   Total Threats: {stats.get('total_threats', 0)}")
        print(f"   Unique Domains: {stats.get('unique_domains', 0)}")
        print()
        
        print("🎯 Top Threats:")
        for threat, count in list(summary.get('threats', {}).items())[:3]:
            print(f"   • {threat}: {count}")
        print()
        
        print("🏠 Top Malicious Domains:")
        for domain, count in list(summary.get('top_domains', {}).items())[:3]:
            print(f"   • {domain}: {count} URLs")
        print()
        
        print("🏷️  Top Malware Tags:")
        for tag, count in list(summary.get('top_tags', {}).items())[:5]:
            print(f"   • {tag}: {count}")
    else:
        print(f"❌ {intelligence.get('error', 'Failed to get intelligence')}")
    
    # Demo 4: Host Reputation Check
    print("\n\n🏠 Demo 4: Host Reputation Check")
    print("-" * 40)
    
    test_hosts = [
        "google.com",
        "suspicious-domain.tk",
        "malware.example.com"
    ]
    
    for host in test_hosts:
        print(f"\nChecking host: {host}")
        host_result = phish_guard.check_urlhaus_host(host)
        
        if host_result.get('success'):
            if host_result.get('is_malicious'):
                print(f"🚨 MALICIOUS HOST!")
                print(f"   URLs found: {host_result.get('url_count', 0)}")
                print(f"   First seen: {host_result.get('firstseen', 'N/A')}")
                
                blacklists = host_result.get('blacklists', {})
                if blacklists:
                    print(f"   Blacklist status:")
                    for bl_name, bl_status in blacklists.items():
                        print(f"     • {bl_name}: {bl_status}")
            else:
                print(f"✅ Clean host (not in URLhaus database)")
        else:
            print(f"❌ {host_result.get('error', 'Failed to check host')}")
        
        time.sleep(0.5)
    
    # Demo 5: Tag Search
    print("\n\n🏷️  Demo 5: Malware Tag Search")
    print("-" * 40)
    
    common_tags = ["emotet", "trojan", "phishing", "botnet"]
    
    for tag in common_tags[:2]:  # Test first 2 tags
        print(f"\nSearching for tag: {tag}")
        tag_result = phish_guard.search_urlhaus_tag(tag)
        
        if tag_result.get('success') and tag_result.get('url_count', 0) > 0:
            print(f"📊 Found {tag_result.get('url_count', 0)} URLs with tag '{tag}'")
            print(f"   First seen: {tag_result.get('firstseen', 'N/A')}")
            print(f"   Last seen: {tag_result.get('lastseen', 'N/A')}")
            
            # Show first few URLs
            urls = tag_result.get('urls', [])
            for i, url_data in enumerate(urls[:3], 1):
                url = url_data.get('url', 'N/A')
                status = url_data.get('url_status', 'unknown')
                status_emoji = '🔴' if status == 'online' else '⚫'
                print(f"   {i}. {status_emoji} {url[:50]}{'...' if len(url) > 50 else ''}")
        else:
            if tag_result.get('success'):
                print(f"ℹ️  No URLs found with tag '{tag}'")
            else:
                print(f"❌ {tag_result.get('error', 'Failed to search by tag')}")
        
        time.sleep(1)
    
    print("\n\n🎉 URLhaus Integration Demo Complete!")
    print("=" * 60)
    print()
    print("🚀 Available Commands:")
    print("• python -m app.cli intel summary")
    print("• python -m app.cli intel recent --limit 20")
    print("• python -m app.cli intel tag emotet")
    print("• python -m app.cli intel host suspicious-domain.com")
    print("• python -m app.api (Start API server)")
    print()
    print("📚 API Endpoints:")
    print("• GET /intelligence/recent-urls?limit=10")
    print("• GET /intelligence/recent-payloads?limit=10")
    print("• GET /intelligence/summary")
    print("• POST /intelligence/search-tag")
    print("• POST /intelligence/check-host")
    print()
    print("🔗 URLhaus API Documentation:")
    print("   https://urlhaus-api.abuse.ch/")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
PhishGuard CLI - Command Line Interface for testing phishing detection
"""

import argparse
import sys
import json
from typing import Optional
import requests
import time

from .phish_core import PhishGuardCore

class PhishGuardCLI:
    def __init__(self):
        self.phish_guard = PhishGuardCore()
        self.api_base_url = "http://localhost:8000"
    
    def analyze_url_cli(self, url: str, verbose: bool = False):
        """Analyze a URL using the CLI"""
        print(f"🔍 Analyzing URL: {url}")
        print("-" * 50)
        
        try:
            # Use local core for analysis
            result = self.phish_guard.analyze_url(url)
            
            # Display results
            print(f"📊 Analysis Results:")
            print(f"   URL: {result['url']}")
            print(f"   Threat Level: {result['threat_level'].upper()}")
            print(f"   Suspicious: {'Yes' if result['is_suspicious'] else 'No'}")
            print(f"   Confidence: {result['confidence']:.1%}")
            print(f"   Message: {result['message']}")
            
            if verbose and result.get('detection_methods'):
                print(f"\n🔧 Detection Methods:")
                for method in result['detection_methods']:
                    print(f"   • {method}")
            
            if verbose and result.get('warnings'):
                print(f"\n⚠️  Warnings:")
                for warning in result['warnings']:
                    print(f"   • {warning}")
            
            print("-" * 50)
            return result
            
        except Exception as e:
            print(f"❌ Error analyzing URL: {str(e)}")
            return None
    
    def analyze_url_api(self, url: str, verbose: bool = False):
        """Analyze a URL using the API"""
        print(f"🔍 Analyzing URL via API: {url}")
        print("-" * 50)
        
        try:
            response = requests.post(
                f"{self.api_base_url}/analyze",
                json={"url": url},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"📊 Analysis Results:")
                print(f"   URL: {result['url']}")
                print(f"   Threat Level: {result['threat_level'].upper()}")
                print(f"   Suspicious: {'Yes' if result['is_suspicious'] else 'No'}")
                print(f"   Confidence: {result['confidence']:.1%}")
                print(f"   Message: {result['message']}")
                
                if verbose and result.get('detection_methods'):
                    print(f"\n🔧 Detection Methods:")
                    for method in result['detection_methods']:
                        print(f"   • {method}")
                
                if verbose and result.get('warnings'):
                    print(f"\n⚠️  Warnings:")
                    for warning in result['warnings']:
                        print(f"   • {warning}")
                
                print("-" * 50)
                return result
            else:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network Error: {str(e)}")
            print("   Make sure the API server is running on http://localhost:8000")
            return None
    
    def get_safety_tips(self):
        """Get safety tips"""
        print("🛡️  Digital Safety Tips:")
        print("-" * 50)
        
        tips = self.phish_guard.get_safety_tips()
        for i, tip in enumerate(tips, 1):
            print(f"{i:2d}. {tip}")
        
        print("-" * 50)
    
    def report_scam(self, url: str, description: str):
        """Report a scam URL"""
        print(f"📝 Reporting scam: {url}")
        print("-" * 50)
        
        try:
            result = self.phish_guard.report_scam(url, description)
            
            if result['success']:
                print(f"✅ {result['message']}")
                print(f"   Report ID: {result.get('report_id', 'N/A')}")
            else:
                print(f"❌ {result['message']}")
            
            print("-" * 50)
            return result
            
        except Exception as e:
            print(f"❌ Error reporting scam: {str(e)}")
            return None
    
    def chat_mode(self):
        """Interactive chat mode"""
        print("🤖 PhishGuard Chat Mode")
        print("Type 'quit' to exit, 'help' for commands")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye! Stay safe online!")
                    break
                
                if user_input.lower() == 'help':
                    print("\nAvailable commands:")
                    print("  check <url> - Analyze a URL")
                    print("  tips - Get safety tips")
                    print("  report <url> <description> - Report a scam")
                    print("  intel summary - Get threat intelligence summary")
                    print("  intel recent [limit] - Get recent threats (default: 10)")
                    print("  intel tag <tag> - Search by malware tag")
                    print("  intel host <host> - Check host reputation")
                    print("  quit - Exit chat mode")
                    print()
                    continue
                
                if user_input.lower().startswith('check '):
                    url = user_input[6:].strip()
                    if url:
                        self.analyze_url_cli(url)
                    continue
                
                if user_input.lower() == 'tips':
                    self.get_safety_tips()
                    continue
                
                if user_input.lower().startswith('report '):
                    parts = user_input[7:].split(' ', 1)
                    if len(parts) >= 2:
                        url, description = parts
                        self.report_scam(url, description)
                    else:
                        print("❌ Please provide URL and description: report <url> <description>")
                    continue
                
                if user_input.lower().startswith('intel '):
                    command = user_input[6:].strip()
                    if command == 'summary':
                        self.show_intelligence_summary()
                    elif command.startswith('recent'):
                        limit = 10
                        try:
                            if ' ' in command:
                                limit = int(command.split()[1])
                        except ValueError:
                            pass
                        self.show_recent_threats(limit)
                    elif command.startswith('tag '):
                        tag = command[4:].strip()
                        if tag:
                            self.search_by_tag(tag)
                    elif command.startswith('host '):
                        host = command[5:].strip()
                        if host:
                            self.check_host(host)
                    else:
                        print("Available intel commands:")
                        print("  intel summary - Get threat intelligence summary")
                        print("  intel recent [limit] - Get recent threats")
                        print("  intel tag <tag> - Search by malware tag")
                        print("  intel host <host> - Check host reputation")
                    continue
                
                # Default chat response
                print("PhishGuard: I can help you with:")
                print("• Checking if links are safe (type 'check <url>')")
                print("• Getting safety tips (type 'tips')")
                print("• Reporting scams (type 'report <url> <description>')")
                print("• Threat intelligence (type 'intel summary')")
                print("• Type 'help' for more commands")
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye! Stay safe online!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    def show_intelligence_summary(self):
        """Show URLhaus intelligence summary"""
        print("📊 Threat Intelligence Summary")
        print("-" * 40)
        
        try:
            result = self.phish_guard.get_urlhaus_intelligence_summary()
            
            if not result.get('success'):
                print(f"❌ {result.get('error', 'Failed to get intelligence')}")
                return
            
            summary = result.get('summary', {})
            stats = result.get('stats', {})
            
            print(f"📈 Statistics:")
            print(f"   Recent URLs: {stats.get('recent_urls', 0)}")
            print(f"   Recent Payloads: {stats.get('recent_payloads', 0)}")
            print(f"   Total Threats: {stats.get('total_threats', 0)}")
            print(f"   Unique Domains: {stats.get('unique_domains', 0)}")
            print()
            
            print("🎯 Top Threats:")
            for threat, count in list(summary.get('threats', {}).items())[:5]:
                print(f"   • {threat}: {count}")
            print()
            
            print("🏠 Top Malicious Domains:")
            for domain, count in list(summary.get('top_domains', {}).items())[:5]:
                print(f"   • {domain}: {count} URLs")
            print()
            
            print("🏷️  Top Malware Tags:")
            for tag, count in list(summary.get('top_tags', {}).items())[:5]:
                print(f"   • {tag}: {count}")
            
        except Exception as e:
            print(f"❌ Error getting intelligence: {str(e)}")
        
        print("-" * 40)
    
    def show_recent_threats(self, limit: int = 10):
        """Show recent threats from URLhaus"""
        print(f"🚨 Recent Threats (Last {limit})")
        print("-" * 50)
        
        try:
            result = self.phish_guard.get_recent_urlhaus_urls(limit=limit)
            
            if not result.get('success'):
                print(f"❌ {result.get('error', 'Failed to get recent threats')}")
                return
            
            urls = result.get('urls', [])
            
            for i, url_data in enumerate(urls, 1):
                url = url_data.get('url', 'N/A')
                threat = url_data.get('threat', 'unknown')
                status = url_data.get('url_status', 'unknown')
                tags = ', '.join(url_data.get('tags', []))
                date_added = url_data.get('date_added', 'N/A')
                
                status_emoji = '🔴' if status == 'online' else '⚫'
                
                print(f"{i:2d}. {status_emoji} {threat.upper()}")
                print(f"    URL: {url[:80]}{'...' if len(url) > 80 else ''}")
                print(f"    Tags: {tags[:50]}{'...' if len(tags) > 50 else ''}")
                print(f"    Added: {date_added}")
                print()
            
        except Exception as e:
            print(f"❌ Error getting recent threats: {str(e)}")
        
        print("-" * 50)
    
    def search_by_tag(self, tag: str):
        """Search URLs by malware tag"""
        print(f"🔍 Searching for tag: {tag}")
        print("-" * 40)
        
        try:
            result = self.phish_guard.search_urlhaus_tag(tag)
            
            if not result.get('success'):
                print(f"❌ {result.get('error', 'Failed to search by tag')}")
                return
            
            if result.get('url_count', 0) == 0:
                print(f"ℹ️  No URLs found with tag '{tag}'")
                return
            
            print(f"📊 Found {result.get('url_count', 0)} URLs with tag '{tag}'")
            print(f"   First seen: {result.get('firstseen', 'N/A')}")
            print(f"   Last seen: {result.get('lastseen', 'N/A')}")
            print()
            
            urls = result.get('urls', [])
            for i, url_data in enumerate(urls[:10], 1):  # Show first 10
                url = url_data.get('url', 'N/A')
                status = url_data.get('url_status', 'unknown')
                threat = url_data.get('threat', 'unknown')
                
                status_emoji = '🔴' if status == 'online' else '⚫'
                print(f"{i:2d}. {status_emoji} {threat}: {url[:60]}{'...' if len(url) > 60 else ''}")
            
            if len(urls) > 10:
                print(f"    ... and {len(urls) - 10} more")
            
        except Exception as e:
            print(f"❌ Error searching by tag: {str(e)}")
        
        print("-" * 40)
    
    def check_host(self, host: str):
        """Check host reputation"""
        print(f"🏠 Checking host: {host}")
        print("-" * 40)
        
        try:
            result = self.phish_guard.check_urlhaus_host(host)
            
            if not result.get('success'):
                print(f"❌ {result.get('error', 'Failed to check host')}")
                return
            
            if not result.get('is_malicious'):
                print(f"✅ Host '{host}' is not known to be malicious")
                return
            
            host_info = result.get('host_info', {})
            print(f"🚨 Host '{host}' is MALICIOUS!")
            print(f"   URLs found: {result.get('url_count', 0)}")
            print(f"   First seen: {result.get('firstseen', 'N/A')}")
            
            blacklists = result.get('blacklists', {})
            if blacklists:
                print(f"   Blacklist status:")
                for bl_name, bl_status in blacklists.items():
                    print(f"     • {bl_name}: {bl_status}")
            
        except Exception as e:
            print(f"❌ Error checking host: {str(e)}")
        
        print("-" * 40)

    def show_detection_status(self):
        """Show status of all detection methods"""
        print("🔍 Detection Method Status")
        print("=" * 50)
        
        status = self.phish_guard.get_detection_status()
        
        for method, info in status.items():
            status_icon = "✅" if info['enabled'] else "❌"
            priority_icon = "🥇" if info['priority'] == 'PRIMARY' else "🔄"
            
            print(f"{status_icon} {method.upper().replace('_', ' ')}")
            print(f"   Priority: {priority_icon} {info['priority']}")
            print(f"   Status: {'Enabled' if info['enabled'] else 'Disabled'}")
            print(f"   Description: {info['description']}")
            print()
        
        print("📊 Detection Priority:")
        print("   1. 🥇 URLhaus (PRIMARY) - Most accurate malware detection")
        print("   2. 🔄 PhishTank (FALLBACK) - Community phishing database")
        print("   3. 🔄 Pattern Analysis (FALLBACK) - Local pattern matching")
        print("   4. 🔄 URL Structure (FALLBACK) - Technical analysis")
        print("   5. 🔄 Myanmar-Specific (FALLBACK) - Local scam detection")
        print()
        print("💡 Tip: Configure URLhaus API key for maximum protection!")

def main():
    parser = argparse.ArgumentParser(
        description="PhishGuard CLI - Phishing Detection Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m app.cli analyze https://example.com
  python -m app.cli analyze --api https://suspicious-link.com
  python -m app.cli tips
  python -m app.cli report "https://scam.com" "Fake bank login page"
  python -m app.cli chat
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a URL for threats')
    analyze_parser.add_argument('url', help='URL to analyze')
    analyze_parser.add_argument('--api', action='store_true', help='Use API instead of local analysis')
    analyze_parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed information')
    
    # Tips command
    subparsers.add_parser('tips', help='Get digital safety tips')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Report a scam URL')
    report_parser.add_argument('url', help='Scam URL to report')
    report_parser.add_argument('description', help='Description of the scam')
    
    # Chat command
    subparsers.add_parser('chat', help='Start interactive chat mode')
    
    # Intelligence commands
    intel_parser = subparsers.add_parser('intel', help='URLhaus threat intelligence')
    intel_subparsers = intel_parser.add_subparsers(dest='intel_command', help='Intelligence commands')
    
    intel_subparsers.add_parser('summary', help='Get threat intelligence summary')
    
    recent_parser = intel_subparsers.add_parser('recent', help='Get recent threats')
    recent_parser.add_argument('--limit', type=int, default=10, help='Number of recent threats to show')
    
    tag_parser = intel_subparsers.add_parser('tag', help='Search by malware tag')
    tag_parser.add_argument('tag_name', help='Malware tag to search for')
    
    host_parser = intel_subparsers.add_parser('host', help='Check host reputation')
    host_parser.add_argument('host_name', help='Host/domain to check')
    
    intel_subparsers.add_parser('status', help='Show detection method status')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = PhishGuardCLI()
    
    try:
        if args.command == 'analyze':
            if args.api:
                cli.analyze_url_api(args.url, args.verbose)
            else:
                cli.analyze_url_cli(args.url, args.verbose)
        
        elif args.command == 'tips':
            cli.get_safety_tips()
        
        elif args.command == 'report':
            cli.report_scam(args.url, args.description)
        
        elif args.command == 'chat':
            cli.chat_mode()
        
        elif args.command == 'intel':
            if args.intel_command == 'summary':
                cli.show_intelligence_summary()
            elif args.intel_command == 'recent':
                cli.show_recent_threats(args.limit)
            elif args.intel_command == 'tag':
                cli.search_by_tag(args.tag_name)
            elif args.intel_command == 'host':
                cli.check_host(args.host_name)
            elif args.intel_command == 'status':
                cli.show_detection_status()
            else:
                print("Please specify an intelligence command. Use --help for options.")
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye! Stay safe online!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

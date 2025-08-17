#!/usr/bin/env python3
"""
Database Initialization Script for PhishGuard
Initializes the SQLite database with default scam URLs and tests functionality
"""

import sys
import os
import time

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.phish_core import PhishGuardCore
from app.database import PhishGuardDatabase

def main():
    print("🗄️  PhishGuard Database Initialization")
    print("=" * 50)
    
    try:
        # Initialize PhishGuard core (this will create the database)
        print("📦 Initializing PhishGuard core...")
        phish_guard = PhishGuardCore()
        
        # Initialize database with default scam URLs
        print("📝 Adding default scam URLs to database...")
        success = phish_guard.initialize_database()
        
        if success:
            print("✅ Database initialized successfully!")
        else:
            print("❌ Failed to initialize database")
            return
        
        # Get database statistics
        print("\n📊 Database Statistics:")
        stats = phish_guard.get_database_stats()
        
        print(f"   Total scam URLs: {stats.get('total_scam_urls', 0)}")
        print(f"   Recent detections (24h): {stats.get('recent_detections_24h', 0)}")
        print(f"   Pending user reports: {stats.get('pending_user_reports', 0)}")
        
        if 'by_source' in stats:
            print("   URLs by source:")
            for source, count in stats['by_source'].items():
                print(f"     • {source}: {count}")
        
        # Test database functionality
        print("\n🧪 Testing Database Functionality:")
        
        # Test 1: Check a known scam URL
        test_url = "https://kbz-verify-account.secure-banking.cf"
        print(f"   Testing URL: {test_url}")
        
        start_time = time.time()
        result = phish_guard.analyze_url(test_url)
        response_time = (time.time() - start_time) * 1000
        
        print(f"   Result: {result['threat_level'].upper()}")
        print(f"   Confidence: {result['confidence']:.1%}")
        print(f"   Methods: {', '.join(result['detection_methods'])}")
        print(f"   Response time: {response_time:.1f}ms")
        
        # Test 2: Check a safe URL
        safe_url = "https://google.com"
        print(f"\n   Testing safe URL: {safe_url}")
        
        start_time = time.time()
        result = phish_guard.analyze_url(safe_url)
        response_time = (time.time() - start_time) * 1000
        
        print(f"   Result: {result['threat_level'].upper()}")
        print(f"   Confidence: {result['confidence']:.1%}")
        print(f"   Response time: {response_time:.1f}ms")
        
        # Test 3: Report a new scam
        print(f"\n   Testing scam reporting...")
        report_result = phish_guard.report_scam(
            "https://fake-scam-test.com", 
            "Test scam URL for database functionality"
        )
        
        if report_result['success']:
            print(f"   ✅ Report added successfully (ID: {report_result['report_id']})")
        else:
            print(f"   ❌ Report failed: {report_result['message']}")
        
        # Show updated stats
        print("\n📊 Updated Database Statistics:")
        stats = phish_guard.get_database_stats()
        print(f"   Total scam URLs: {stats.get('total_scam_urls', 0)}")
        print(f"   Recent detections (24h): {stats.get('recent_detections_24h', 0)}")
        
        print("\n🎉 Database initialization and testing completed!")
        print("\n💡 Next steps:")
        print("   1. Run 'python demo_urlhaus.py' to test full functionality")
        print("   2. Configure URLhaus API key for enhanced detection")
        print("   3. Start using PhishGuard for URL analysis")
        
    except Exception as e:
        print(f"❌ Error during initialization: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
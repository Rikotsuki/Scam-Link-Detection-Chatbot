#!/usr/bin/env python3
"""
Vision-Enabled PhishGuard AI Demo
Demonstrates LLaVA vision model capabilities with RAG integration
"""

import json
import logging
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import time

from vision_ollama_integration import VisionPhishGuardManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VisionDemo:
    """Demo class for showcasing vision capabilities"""
    
    def __init__(self):
        self.manager = VisionPhishGuardManager()
        self.demo_images_dir = Path("demo_images")
        self.demo_images_dir.mkdir(exist_ok=True)
    
    def create_demo_images(self):
        """Create demo images for testing"""
        logger.info("Creating demo images for testing...")
        
        # Demo 1: Suspicious login form
        login_image = Image.new('RGB', (400, 300), color='white')
        draw = draw = ImageDraw.Draw(login_image)
        
        # Draw a fake login form
        draw.rectangle([50, 50, 350, 250], outline='black', width=2)
        draw.text((150, 70), "SECURE LOGIN", fill='red', font=None)
        draw.rectangle([70, 100, 330, 130], outline='gray', width=1)
        draw.text((80, 110), "Enter your password:", fill='black', font=None)
        draw.rectangle([70, 150, 330, 180], outline='gray', width=1)
        draw.text((80, 160), "Enter credit card number:", fill='black', font=None)
        draw.rectangle([120, 200, 280, 230], fill='red', outline='black', width=1)
        draw.text((180, 210), "SUBMIT", fill='white', font=None)
        
        login_image.save(self.demo_images_dir / "suspicious_login.png")
        logger.info("✅ Created suspicious login demo image")
        
        # Demo 2: Fake security warning
        warning_image = Image.new('RGB', (500, 400), color='yellow')
        draw = ImageDraw.Draw(warning_image)
        
        # Draw warning message
        draw.rectangle([50, 50, 450, 350], fill='red', outline='black', width=3)
        draw.text((200, 100), "⚠️ SECURITY ALERT ⚠️", fill='white', font=None)
        draw.text((100, 150), "Your computer has been infected!", fill='white', font=None)
        draw.text((100, 180), "Call 1-800-FAKE-NOW immediately", fill='white', font=None)
        draw.text((100, 210), "or your data will be lost forever!", fill='white', font=None)
        draw.rectangle([150, 250, 350, 300], fill='green', outline='black', width=2)
        draw.text((200, 270), "CALL NOW", fill='white', font=None)
        
        warning_image.save(self.demo_images_dir / "fake_warning.png")
        logger.info("✅ Created fake security warning demo image")
        
        # Demo 3: Suspicious email
        email_image = Image.new('RGB', (600, 500), color='white')
        draw = ImageDraw.Draw(email_image)
        
        # Draw email content
        draw.rectangle([50, 50, 550, 450], outline='black', width=2)
        draw.text((70, 80), "From: support@microsft.com", fill='blue', font=None)
        draw.text((70, 110), "Subject: URGENT: Your account has been suspended", fill='red', font=None)
        draw.text((70, 150), "Dear valued customer,", fill='black', font=None)
        draw.text((70, 180), "We have detected suspicious activity on your account.", fill='black', font=None)
        draw.text((70, 210), "Click the link below to verify your identity:", fill='black', font=None)
        draw.text((70, 240), "http://microsft-verify.com/secure", fill='blue', font=None)
        draw.text((70, 270), "This link will expire in 24 hours.", fill='red', font=None)
        draw.rectangle([200, 320, 400, 370], fill='blue', outline='black', width=2)
        draw.text((250, 340), "VERIFY NOW", fill='white', font=None)
        
        email_image.save(self.demo_images_dir / "suspicious_email.png")
        logger.info("✅ Created suspicious email demo image")
    
    def demo_url_analysis(self):
        """Demo URL analysis with RAG enhancement"""
        logger.info("🔗 Demo: URL Analysis with RAG Enhancement")
        logger.info("=" * 50)
        
        test_urls = [
            "https://paypal-secure-verify.com/login",
            "https://www.google.com",
            "https://amaz0n-prime.com/account",
            "https://github.com"
        ]
        
        for url in test_urls:
            logger.info(f"\nAnalyzing URL: {url}")
            try:
                result = self.manager.phishguard_ai.analyze_url_with_context(url)
                
                print(f"\n📊 Analysis for: {url}")
                print(f"Risk Level: {'🔴 HIGH' if 'suspicious' in result['analysis'].lower() else '🟢 LOW'}")
                print(f"Analysis: {result['analysis'][:200]}...")
                print(f"Context Used: {len(result.get('context_used', []))} knowledge entries")
                
            except Exception as e:
                logger.error(f"Error analyzing URL {url}: {e}")
    
    def demo_image_analysis(self):
        """Demo image analysis for phishing detection"""
        logger.info("\n🖼️ Demo: Image Analysis for Phishing Detection")
        logger.info("=" * 50)
        
        demo_images = [
            "suspicious_login.png",
            "fake_warning.png", 
            "suspicious_email.png"
        ]
        
        for image_name in demo_images:
            image_path = self.demo_images_dir / image_name
            if image_path.exists():
                logger.info(f"\nAnalyzing image: {image_name}")
                try:
                    result = self.manager.phishguard_ai.analyze_image_for_phishing(image_path)
                    
                    print(f"\n🖼️ Analysis for: {image_name}")
                    print(f"Analysis Type: {result.get('analysis_type', 'N/A')}")
                    print(f"Analysis: {result['analysis'][:300]}...")
                    print(f"Context Used: {len(result.get('context_used', []))} knowledge entries")
                    
                except Exception as e:
                    logger.error(f"Error analyzing image {image_name}: {e}")
            else:
                logger.warning(f"Demo image not found: {image_path}")
    
    def demo_screenshot_analysis(self):
        """Demo screenshot analysis"""
        logger.info("\n📸 Demo: Screenshot Analysis")
        logger.info("=" * 50)
        
        # Use the suspicious login image as a screenshot
        screenshot_path = self.demo_images_dir / "suspicious_login.png"
        if screenshot_path.exists():
            logger.info("Analyzing screenshot for phishing indicators...")
            try:
                result = self.manager.phishguard_ai.analyze_screenshot(screenshot_path)
                
                print(f"\n📸 Screenshot Analysis:")
                print(f"Analysis Type: {result.get('analysis_type', 'N/A')}")
                print(f"Analysis: {result['analysis'][:300]}...")
                
            except Exception as e:
                logger.error(f"Error analyzing screenshot: {e}")
    
    def demo_combined_analysis(self):
        """Demo combined URL and image analysis"""
        logger.info("\n🔗🖼️ Demo: Combined URL and Image Analysis")
        logger.info("=" * 50)
        
        test_url = "https://paypal-secure-verify.com/login"
        test_image = self.demo_images_dir / "suspicious_login.png"
        
        if test_image.exists():
            logger.info("Performing combined analysis...")
            try:
                result = self.manager.phishguard_ai.combined_analysis(
                    url=test_url,
                    image_path=test_image
                )
                
                print(f"\n🔗🖼️ Combined Analysis Results:")
                print(f"Analysis Type: {result.get('analysis_type', 'N/A')}")
                
                if 'url_analysis' in result:
                    print(f"URL Analysis: {result['url_analysis']['analysis'][:150]}...")
                
                if 'image_analysis' in result:
                    print(f"Image Analysis: {result['image_analysis']['analysis'][:150]}...")
                
                if 'combined_assessment' in result:
                    print(f"Combined Assessment: {result['combined_assessment'][:200]}...")
                
            except Exception as e:
                logger.error(f"Error in combined analysis: {e}")
    
    def demo_haru_vision_help(self):
        """Demo Haru's vision-enabled help"""
        logger.info("\n🤝 Demo: Haru's Vision-Enabled Help")
        logger.info("=" * 50)
        
        # Use the fake warning image
        warning_image = self.demo_images_dir / "fake_warning.png"
        if warning_image.exists():
            logger.info("Testing Haru's help with suspicious screenshot...")
            try:
                result = self.manager.haru.help_with_screenshot(
                    warning_image,
                    "I got this popup warning and I'm scared. What should I do?"
                )
                
                print(f"\n🤝 Haru's Help Response:")
                print(f"Situation: {result['situation']}")
                print(f"Analysis: {result['analysis'][:300]}...")
                print(f"Recovery Context: {len(result.get('recovery_context', []))} guidance items")
                
            except Exception as e:
                logger.error(f"Error getting Haru's help: {e}")
    
    def demo_rag_system(self):
        """Demo RAG system capabilities"""
        logger.info("\n🧠 Demo: RAG System Capabilities")
        logger.info("=" * 50)
        
        # Test adding custom knowledge
        logger.info("Adding custom phishing knowledge to RAG system...")
        custom_knowledge = [
            "Phishing emails often use urgent language to create panic",
            "Fake login pages may have slightly misspelled URLs",
            "Legitimate companies never ask for passwords via email",
            "Suspicious popups often claim your computer is infected"
        ]
        
        for knowledge in custom_knowledge:
            success = self.manager.rag_system.add_knowledge(
                knowledge,
                {"type": "custom_knowledge", "source": "demo"}
            )
            if success:
                logger.info(f"✅ Added: {knowledge[:50]}...")
        
        # Test retrieval
        logger.info("\nTesting knowledge retrieval...")
        queries = [
            "phishing email indicators",
            "fake login pages",
            "suspicious popups"
        ]
        
        for query in queries:
            context = self.manager.rag_system.retrieve_relevant_context(query)
            print(f"\n🔍 Query: {query}")
            print(f"Retrieved {len(context)} relevant items:")
            for i, item in enumerate(context[:2], 1):
                print(f"  {i}. {item[:80]}...")
    
    def run_full_demo(self):
        """Run the complete vision demo"""
        logger.info("🚀 Starting Vision-Enabled PhishGuard AI Demo")
        logger.info("=" * 60)
        
        # Setup vision system
        logger.info("Setting up vision system...")
        if not self.manager.setup_vision_system():
            logger.error("Failed to setup vision system")
            return
        
        # Create demo images
        self.create_demo_images()
        
        # Run all demos
        demos = [
            self.demo_rag_system,
            self.demo_url_analysis,
            self.demo_image_analysis,
            self.demo_screenshot_analysis,
            self.demo_combined_analysis,
            self.demo_haru_vision_help
        ]
        
        for demo in demos:
            try:
                demo()
                time.sleep(2)  # Brief pause between demos
            except Exception as e:
                logger.error(f"Demo failed: {e}")
        
        logger.info("\n🎉 Vision Demo Completed!")
        logger.info("=" * 60)
        logger.info("📝 Key Features Demonstrated:")
        logger.info("   ✅ LLaVA Vision Model Integration")
        logger.info("   ✅ RAG-Enhanced Context Retrieval")
        logger.info("   ✅ Image Analysis for Phishing Detection")
        logger.info("   ✅ Screenshot Analysis")
        logger.info("   ✅ Combined URL + Image Analysis")
        logger.info("   ✅ Vision-Enabled Help System")
        logger.info("\n🔧 Next Steps:")
        logger.info("   1. Test with your own images and URLs")
        logger.info("   2. Customize the RAG knowledge base")
        logger.info("   3. Integrate with your existing systems")

def main():
    """Main function"""
    demo = VisionDemo()
    demo.run_full_demo()

if __name__ == "__main__":
    main() 
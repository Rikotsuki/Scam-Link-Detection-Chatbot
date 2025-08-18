#!/usr/bin/env python3
"""
Anime PhishGuard AI Demo
Demonstrates AI-chan and Haru with Japanese voice synthesis and vision capabilities
"""

import json
import logging
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import time
import asyncio

from anime_vision_ollama_integration import AnimePhishGuardManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AnimeDemo:
    """Demo class for showcasing anime character capabilities"""
    
    def __init__(self):
        self.manager = AnimePhishGuardManager()
        self.demo_images_dir = Path("demo_images")
        self.demo_images_dir.mkdir(exist_ok=True)
        
        # Character information
        self.ai_chan_info = {
            "name": "AI-chan",
            "personality": "Cheerful anime girl phishing detector",
            "catchphrase": "危険です！",  # "It is dangerous!"
            "role": "Cybersecurity specialist"
        }
        
        self.haru_info = {
            "name": "Haru",
            "personality": "Lazy but caring anime boy",
            "catchphrase": "めんどくさいな...",  # "What a pain in the ass..."
            "role": "Recovery and education specialist"
        }
    
    def create_anime_demo_images(self):
        """Create anime-style demo images for testing"""
        logger.info("🎨 Creating anime-style demo images...")
        
        # Demo 1: Fake anime game login (common phishing target)
        game_login = Image.new('RGB', (500, 400), color='#FFB6C1')  # Light pink
        draw = ImageDraw.Draw(game_login)
        
        # Draw anime-style fake game login
        draw.rectangle([50, 50, 450, 350], fill='#FF69B4', outline='#FF1493', width=3)
        draw.text((180, 80), "♪ ANIME GAME LOGIN ♪", fill='white', font=None)
        draw.text((100, 120), "Get 1000 FREE GEMS!", fill='yellow', font=None)
        draw.rectangle([80, 160, 420, 190], outline='white', width=2)
        draw.text((90, 170), "Enter your account password:", fill='white', font=None)
        draw.rectangle([80, 210, 420, 240], outline='white', width=2)
        draw.text((90, 220), "Enter your credit card:", fill='white', font=None)
        draw.rectangle([180, 270, 320, 310], fill='red', outline='white', width=2)
        draw.text((220, 285), "CLAIM NOW!", fill='white', font=None)
        
        game_login.save(self.demo_images_dir / "fake_anime_game.png")
        logger.info("✅ Created fake anime game login image")
        
        # Demo 2: Suspicious anime character popup
        popup_warning = Image.new('RGB', (600, 500), color='#FF6347')  # Tomato red
        draw = ImageDraw.Draw(popup_warning)
        
        # Draw suspicious popup with anime styling
        draw.rectangle([50, 50, 550, 450], fill='#DC143C', outline='black', width=4)
        draw.text((200, 100), "⚠️ URGENT WAIFU ALERT ⚠️", fill='white', font=None)
        draw.text((150, 150), "Your anime collection is in danger!", fill='white', font=None)
        draw.text((120, 180), "Click here to protect your waifus NOW!", fill='yellow', font=None)
        draw.text((100, 210), "Limited time: Only 5 minutes remaining!", fill='white', font=None)
        draw.rectangle([200, 280, 400, 330], fill='green', outline='black', width=3)
        draw.text((250, 300), "PROTECT NOW", fill='white', font=None)
        draw.text((180, 360), "Brought to you by AnimeProtect.exe", fill='#FFB6C1', font=None)
        
        popup_warning.save(self.demo_images_dir / "anime_popup_scam.png")
        logger.info("✅ Created anime popup scam image")
        
        # Demo 3: Fake anime merchandise store
        merch_store = Image.new('RGB', (700, 600), color='white')
        draw = ImageDraw.Draw(merch_store)
        
        # Draw fake anime store
        draw.rectangle([50, 50, 650, 550], outline='#FF69B4', width=3)
        draw.text((250, 80), "ANIME STORE SALE!", fill='#FF1493', font=None)
        draw.text((100, 120), "Limited Edition Figures - 90% OFF!", fill='red', font=None)
        draw.text((100, 160), "From: anime-store-oficial.com", fill='blue', font=None)
        draw.text((100, 200), "Pay with Bitcoin for extra 50% discount!", fill='green', font=None)
        draw.text((100, 240), "Send payment to: 1FakeAnimeAddress123", fill='black', font=None)
        draw.rectangle([250, 350, 450, 400], fill='orange', outline='black', width=2)
        draw.text((300, 370), "BUY NOW!", fill='white', font=None)
        draw.text((150, 480), "⚠️ Warning: This site is NOT secure", fill='red', font=None)
        
        merch_store.save(self.demo_images_dir / "fake_anime_store.png")
        logger.info("✅ Created fake anime store image")
    
    def demo_ai_chan_greetings(self):
        """Demo AI-chan's cheerful greetings and personality"""
        logger.info("🌸 Demo: AI-chan's Cheerful Personality")
        logger.info("=" * 50)
        
        try:
            # Get AI-chan's greeting
            greeting = self.manager.ai_chan.get_cheerful_greeting()
            
            print(f"\n🌸 {greeting['character']} appears!")
            print(f"💬 {greeting['greeting']}")
            print(f"🎭 Personality: {greeting['personality']}")
            
            if greeting.get('voice_file'):
                print(f"🔊 Voice file generated: {greeting['voice_file']}")
                print("   (AI-chan's cheerful voice saying her greeting)")
            
            return greeting
            
        except Exception as e:
            logger.error(f"Error in AI-chan greeting demo: {e}")
            return None
    
    def demo_haru_greetings(self):
        """Demo Haru's lazy but caring personality"""
        logger.info("\n😴 Demo: Haru's Lazy but Caring Personality")
        logger.info("=" * 50)
        
        try:
            # Get Haru's greeting
            greeting = self.manager.haru.get_lazy_greeting()
            
            print(f"\n😴 {greeting['character']} reluctantly appears...")
            print(f"💬 {greeting['greeting']}")
            print(f"🎭 Personality: {greeting['personality']}")
            
            if greeting.get('voice_file'):
                print(f"🔊 Voice file generated: {greeting['voice_file']}")
                print("   (Haru's lazy voice with a slight sigh)")
            
            return greeting
            
        except Exception as e:
            logger.error(f"Error in Haru greeting demo: {e}")
            return None
    
    def demo_ai_chan_phishing_detection(self):
        """Demo AI-chan detecting phishing with voice warnings"""
        logger.info("\n🔍 Demo: AI-chan's Phishing Detection with Voice Warnings")
        logger.info("=" * 50)
        
        demo_images = [
            ("fake_anime_game.png", "Fake anime game login form"),
            ("anime_popup_scam.png", "Suspicious anime popup warning"),
            ("fake_anime_store.png", "Fake anime merchandise store")
        ]
        
        results = []
        
        for image_name, description in demo_images:
            image_path = self.demo_images_dir / image_name
            if image_path.exists():
                logger.info(f"\n🖼️ AI-chan analyzing: {description}")
                try:
                    # AI-chan analyzes the image
                    result = self.manager.ai_chan.analyze_with_voice_warning(image_path=image_path)
                    
                    print(f"\n🌸 AI-chan's Analysis of {description}:")
                    
                    if 'image_analysis' in result:
                        analysis = result['image_analysis']
                        print(f"💭 Analysis: {analysis['analysis'][:200]}...")
                        print(f"🎭 Character: {analysis['character']}")
                        
                        if analysis.get('voice_file'):
                            print(f"🔊 Danger Warning Voice: {analysis['voice_file']}")
                            print("   🎌 AI-chan says: '危険です！' (It is dangerous!)")
                    
                    if result.get('danger_detected'):
                        print("🚨 DANGER DETECTED! AI-chan generated voice warning!")
                    
                    results.append(result)
                    time.sleep(2)  # Brief pause between analyses
                    
                except Exception as e:
                    logger.error(f"Error analyzing {image_name}: {e}")
            else:
                logger.warning(f"Demo image not found: {image_path}")
        
        return results
    
    def demo_ai_chan_url_analysis(self):
        """Demo AI-chan analyzing suspicious URLs"""
        logger.info("\n🔗 Demo: AI-chan's URL Analysis")
        logger.info("=" * 50)
        
        suspicious_urls = [
            "https://anime-game-free-gems.com/login",
            "https://waifu-protector-download.exe",
            "https://anime-store-oficial.com/bitcoin-sale",
            "https://free-anime-episodes.net/download-now"
        ]
        
        results = []
        
        for url in suspicious_urls:
            logger.info(f"\n🔗 AI-chan analyzing URL: {url}")
            try:
                result = self.manager.ai_chan.analyze_with_voice_warning(url=url)
                
                print(f"\n🌸 AI-chan's URL Analysis:")
                print(f"🔗 URL: {url}")
                
                if 'url_analysis' in result:
                    analysis = result['url_analysis']
                    print(f"💭 Analysis: {analysis['response'][:200]}...")
                    print(f"🎭 Character: {analysis['character']}")
                
                results.append(result)
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error analyzing URL {url}: {e}")
        
        return results
    
    def demo_haru_recovery_help(self):
        """Demo Haru helping with recovery scenarios"""
        logger.info("\n🤝 Demo: Haru's Recovery Assistance (with increasing laziness)")
        logger.info("=" * 50)
        
        recovery_scenarios = [
            ("I clicked on a suspicious anime game link", "fake_anime_game.png"),
            ("I downloaded something called 'WaifuProtector.exe'", "anime_popup_scam.png"),
            ("I gave my credit card to a fake anime store", "fake_anime_store.png"),
            ("Can you help me check if this website is safe?", None),
            ("What should I do if I think I've been scammed?", None),
            ("How can I protect myself from anime-related scams?", None)  # This should trigger lazy response
        ]
        
        results = []
        
        for scenario, image_file in recovery_scenarios:
            logger.info(f"\n🤝 User asks Haru: {scenario}")
            
            try:
                image_path = None
                if image_file:
                    image_path = self.demo_images_dir / image_file
                    if not image_path.exists():
                        image_path = None
                
                result = self.manager.haru.help_with_lazy_attitude(scenario, image_path)
                
                print(f"\n😴 Haru's Response:")
                print(f"📝 Situation: {result['situation']}")
                
                if 'help_response' in result:
                    response = result['help_response']
                    print(f"💭 Help: {response['response'][:200]}...")
                    print(f"🎭 Character: {response['character']}")
                
                if 'lazy_response' in result:
                    print(f"🔊 Lazy Voice Response: {result['lazy_response']}")
                    print("   🎌 Haru says: 'めんどくさいな...' (What a pain in the ass...)")
                    print(f"💤 {result.get('message', '')}")
                
                results.append(result)
                time.sleep(2)  # Pause between scenarios
                
            except Exception as e:
                logger.error(f"Error in Haru recovery demo: {e}")
        
        return results
    
    def demo_character_interactions(self):
        """Demo interactions between AI-chan and Haru"""
        logger.info("\n🎭 Demo: AI-chan and Haru Character Interactions")
        logger.info("=" * 50)
        
        print("\n🌸 AI-chan: こんにちは！AI-chanです♪ Let's detect some phishing!")
        print("😴 Haru: はぁ...Haruだよ。何か用？ (sigh... I'm Haru. What do you want?)")
        print("\n🌸 AI-chan: We need to help users stay safe online! ♪")
        print("😴 Haru: めんどくさいけど...まあ、大丈夫だよ。(It's a pain but... well, it'll be fine.)")
        print("\n🌸 AI-chan: Let's work together to protect everyone! (◕‿◕)♡")
        print("😴 Haru: はぁ...わかったよ。(sigh... I understand.)")
        
        # Show their different approaches
        print("\n" + "=" * 50)
        print("🎭 CHARACTER COMPARISON:")
        print("=" * 50)
        
        print(f"🌸 {self.ai_chan_info['name']}:")
        print(f"   • Personality: {self.ai_chan_info['personality']}")
        print(f"   • Role: {self.ai_chan_info['role']}")
        print(f"   • Catchphrase: {self.ai_chan_info['catchphrase']}")
        print(f"   • Response to danger: Enthusiastic warnings with voice alerts")
        
        print(f"\n😴 {self.haru_info['name']}:")
        print(f"   • Personality: {self.haru_info['personality']}")
        print(f"   • Role: {self.haru_info['role']}")
        print(f"   • Catchphrase: {self.haru_info['catchphrase']}")
        print(f"   • Response to questions: Gets lazy but still helps")
    
    def run_full_anime_demo(self):
        """Run the complete anime demo"""
        logger.info("🎌 Starting Anime PhishGuard AI Demo")
        logger.info("=" * 60)
        
        # Setup anime system
        logger.info("Setting up anime system...")
        if not self.manager.setup_anime_system():
            logger.error("Failed to setup anime system")
            return
        
        # Create demo images
        self.create_anime_demo_images()
        
        # Run character introductions
        ai_greeting = self.demo_ai_chan_greetings()
        haru_greeting = self.demo_haru_greetings()
        
        # Show character interactions
        self.demo_character_interactions()
        
        # Demo AI-chan's phishing detection
        ai_detection_results = self.demo_ai_chan_phishing_detection()
        
        # Demo AI-chan's URL analysis
        url_analysis_results = self.demo_ai_chan_url_analysis()
        
        # Demo Haru's recovery assistance
        haru_help_results = self.demo_haru_recovery_help()
        
        # Summary
        logger.info("\n🎉 Anime Demo Completed!")
        logger.info("=" * 60)
        logger.info("📝 Key Features Demonstrated:")
        logger.info("   🌸 AI-chan: Cheerful anime girl phishing detector")
        logger.info("   😴 Haru: Lazy but caring anime boy recovery assistant")
        logger.info("   🎌 Japanese voice synthesis for both characters")
        logger.info("   🔊 Voice warnings: '危険です！' for danger detection")
        logger.info("   💤 Lazy responses: 'めんどくさいな...' for too many questions")
        logger.info("   🖼️ Vision analysis with llama3.2-vision:11b")
        logger.info("   🧠 RAG-enhanced context for better responses")
        
        logger.info("\n🎮 Generated Files:")
        voice_files = list(Path(".").glob("*.wav"))
        for voice_file in voice_files:
            logger.info(f"   🔊 {voice_file}")
        
        logger.info("\n🔧 Next Steps:")
        logger.info("   1. Listen to the generated voice files")
        logger.info("   2. Test with your own suspicious images/URLs")
        logger.info("   3. Customize the anime character personalities")
        logger.info("   4. Integrate into your own applications")
        
        return {
            'ai_greeting': ai_greeting,
            'haru_greeting': haru_greeting,
            'detection_results': ai_detection_results,
            'url_results': url_analysis_results,
            'recovery_results': haru_help_results
        }

def main():
    """Main function"""
    demo = AnimeDemo()
    results = demo.run_full_anime_demo()
    
    # Save demo results
    if results:
        with open("anime_demo_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        logger.info("💾 Demo results saved to anime_demo_results.json")

if __name__ == "__main__":
    main() 
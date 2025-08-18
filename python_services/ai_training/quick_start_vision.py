#!/usr/bin/env python3
"""
Quick Start Script for Vision-Enabled PhishGuard AI
Easy setup and testing of the LLaVA vision system with RAG integration
"""

import sys
import os
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        logger.error("❌ Python 3.8 or higher is required")
        return False
    logger.info(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_ollama_installation():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"✅ Ollama installed: {result.stdout.strip()}")
            return True
        else:
            logger.error("❌ Ollama not found in PATH")
            return False
    except FileNotFoundError:
        logger.error("❌ Ollama not installed")
        return False

def install_dependencies():
    """Install required Python dependencies"""
    logger.info("📦 Installing Python dependencies...")
    
    requirements_file = Path("requirements_vision.txt")
    if not requirements_file.exists():
        logger.error("❌ requirements_vision.txt not found")
        return False
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements_vision.txt'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("✅ Dependencies installed successfully")
            return True
        else:
            logger.error(f"❌ Failed to install dependencies: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"❌ Error installing dependencies: {e}")
        return False

def setup_vision_system():
    """Setup the vision system"""
    logger.info("🚀 Setting up vision system...")
    
    try:
        from setup_vision_ollama import VisionOllamaSetup
        setup = VisionOllamaSetup()
        return setup.setup_environment()
    except ImportError as e:
        logger.error(f"❌ Error importing setup module: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Error setting up vision system: {e}")
        return False

def test_vision_system():
    """Test the vision system"""
    logger.info("🧪 Testing vision system...")
    
    try:
        from vision_ollama_integration import VisionPhishGuardManager
        manager = VisionPhishGuardManager()
        test_results = manager.test_system()
        
        all_passed = all(test_results.values())
        if all_passed:
            logger.info("✅ All vision system tests passed!")
        else:
            logger.warning("⚠️ Some tests failed:")
            for test, result in test_results.items():
                status = "✅" if result else "❌"
                logger.info(f"  {status} {test}")
        
        return all_passed
    except Exception as e:
        logger.error(f"❌ Error testing vision system: {e}")
        return False

def run_demo():
    """Run the vision demo"""
    logger.info("🎮 Running vision demo...")
    
    try:
        from vision_demo import VisionDemo
        demo = VisionDemo()
        demo.run_full_demo()
        return True
    except Exception as e:
        logger.error(f"❌ Error running demo: {e}")
        return False

def create_example_usage():
    """Create example usage script"""
    logger.info("📝 Creating example usage script...")
    
    example_code = '''#!/usr/bin/env python3
"""
Example Usage of Vision-Enabled PhishGuard AI
"""

from vision_ollama_integration import VisionPhishGuardManager

def main():
    # Initialize the vision system
    manager = VisionPhishGuardManager()
    manager.setup_vision_system()
    
    # Example 1: Analyze a suspicious URL
    print("🔗 Analyzing suspicious URL...")
    result = manager.phishguard_ai.analyze_url_with_context(
        "https://paypal-secure-verify.com/login"
    )
    print(f"Analysis: {result['analysis'][:200]}...")
    
    # Example 2: Analyze an image (replace with your image path)
    print("\\n🖼️ Analyzing image...")
    # result = manager.phishguard_ai.analyze_image_for_phishing("your_image.png")
    # print(f"Analysis: {result['analysis'][:200]}...")
    
    # Example 3: Get help with a screenshot
    print("\\n🤝 Getting help...")
    # result = manager.haru.help_with_screenshot(
    #     "screenshot.png", 
    #     "I got this popup warning. What should I do?"
    # )
    # print(f"Help: {result['analysis'][:200]}...")
    
    print("\\n✅ Example completed! Check the results above.")

if __name__ == "__main__":
    main()
'''
    
    with open("example_usage.py", "w") as f:
        f.write(example_code)
    
    logger.info("✅ Created example_usage.py")

def main():
    """Main quick start function"""
    logger.info("🚀 Vision-Enabled PhishGuard AI Quick Start")
    logger.info("=" * 50)
    
    # Step 1: Check Python version
    if not check_python_version():
        return False
    
    # Step 2: Check Ollama installation
    if not check_ollama_installation():
        logger.error("Please install Ollama from https://ollama.ai")
        return False
    
    # Step 3: Install dependencies
    if not install_dependencies():
        return False
    
    # Step 4: Setup vision system
    if not setup_vision_system():
        return False
    
    # Step 5: Test system
    if not test_vision_system():
        logger.warning("⚠️ Some tests failed, but continuing...")
    
    # Step 6: Create example usage
    create_example_usage()
    
    # Step 7: Ask if user wants to run demo
    print("\n" + "=" * 50)
    print("🎉 Vision system setup completed!")
    print("\n📝 Next steps:")
    print("   1. Run: python example_usage.py")
    print("   2. Run: python vision_demo.py (for full demo)")
    print("   3. Test with your own images and URLs")
    
    demo_choice = input("\n🤔 Would you like to run the full demo now? (y/n): ").lower().strip()
    if demo_choice in ['y', 'yes']:
        run_demo()
    
    print("\n🎯 You're all set! The vision-enabled PhishGuard AI is ready to use.")
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("\n👋 Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1) 
#!/usr/bin/env python3
"""
Quick Environment Setup Script
Creates the necessary .env files for the Enhanced Anime AI System
"""

import os
from pathlib import Path

def create_env_file(file_path: Path, content: str):
    """Create an environment file with the given content"""
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"✅ Created: {file_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to create {file_path}: {e}")
        return False

def main():
    print("🔧 Setting up environment files for Enhanced Anime AI System...")
    print("=" * 60)
    
    # Get the current directory (python_services)
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    
    # JWT Secret (you can regenerate this if needed)
    jwt_secret = "bgOSiM/GjwBbKb+H3TMMXN/yMlvbNZtxuzAk3ndEkTo="
    
    # Frontend .env.local
    frontend_env = f"""# Required Environment Variables
JWT_SECRET="{jwt_secret}"
NEXT_PUBLIC_BASE_URL="http://localhost:3000"

# Optional Environment Variables (for enhanced features)
# URLHAUS_AUTH_KEY="your-urlhaus-api-key-here"
# NEXT_PUBLIC_TURNSTILE_SITE_KEY="your-turnstile-site-key"
# TURNSTILE_SECRET_KEY="your-turnstile-secret-key"
"""
    
    # Backend .env
    backend_env = f"""# Required Environment Variables
JWT_SECRET="{jwt_secret}"
PYTHON_SERVICE_URL="http://localhost:8000"

# Optional Environment Variables
# URLHAUS_AUTH_KEY="your-urlhaus-api-key-here"
"""
    
    # Python services .env
    python_env = """# Optional: URLhaus API Key for enhanced threat detection
# Get your free API key from: https://urlhaus.abuse.ch/api/
URLHAUS_AUTH_KEY="your-urlhaus-api-key-here"

# Note: The system will work without URLhaus, but with enhanced features if provided
"""
    
    # Create the files
    files_created = 0
    
    # Frontend .env.local
    frontend_path = project_root / "frontend" / ".env.local"
    if create_env_file(frontend_path, frontend_env):
        files_created += 1
    
    # Backend .env
    backend_path = project_root / "backend" / ".env"
    if create_env_file(backend_path, backend_env):
        files_created += 1
    
    # Python services .env
    python_path = current_dir / ".env"
    if create_env_file(python_path, python_env):
        files_created += 1
    
    print("=" * 60)
    print(f"🎉 Environment setup complete! Created {files_created}/3 files.")
    print("")
    print("📝 Next steps:")
    print("1. Optional: Get a free URLhaus API key from https://urlhaus.abuse.ch/api/")
    print("2. Edit the .env files to add your URLhaus key if desired")
    print("3. Run: python start_enhanced_system.py")
    print("")
    print("🔑 Demo Login Credentials:")
    print("   User: user@example.com / password123")
    print("   Admin: admin@example.com / admin123")
    print("")
    print("🌐 System will be available at:")
    print("   Login: http://localhost:3000/login")
    print("   Dashboard: http://localhost:3000/anime")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Test script to verify Gemini API connection and model
"""
import os
import sys
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from edutrack.api.gemini_handler import GeminiHandler

def test_gemini_connection():
    """Test Gemini API connection"""
    print("=" * 60)
    print("🧪 Testing Gemini API Connection")
    print("=" * 60)
    print()
    
    # Test with Gemini 2.5 Pro
    print("📡 Initializing Gemini 2.5 Pro...")
    handler = GeminiHandler(model_name='gemini-2.5-pro')
    
    if not handler.model:
        print("❌ Error: Gemini API key not configured!")
        print("Please check your .env file.")
        return False
    
    print(f"✅ Model initialized: {handler.model_name}")
    print()
    
    # Test simple query
    print("🔍 Testing with a simple query...")
    test_prompt = """
    Analyze this simple Python code and provide a brief review:
    
    def greet(name):
        return f"Hello, {name}!"
    
    result = greet("World")
    print(result)
    
    Provide a brief summary (2-3 sentences) of the code quality.
    """
    
    try:
        response = handler.model.generate_content(test_prompt)
        print("✅ API Response received!")
        print()
        print("📝 Response:")
        print("-" * 60)
        print(response.text)
        print("-" * 60)
        print()
        print("✅ Gemini API is working correctly!")
        print()
        
        # Show available models info
        print("📊 Model Information:")
        print(f"   Model: {handler.model_name}")
        print(f"   Status: Active and responding")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error during API call: {e}")
        print()
        print("💡 Troubleshooting:")
        print("   1. Check your API key in .env file")
        print("   2. Verify your API key at: https://makersuite.google.com/app/apikey")
        print("   3. Ensure you have API quota available")
        return False

if __name__ == "__main__":
    success = test_gemini_connection()
    sys.exit(0 if success else 1)

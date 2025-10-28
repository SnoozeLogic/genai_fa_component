#!/usr/bin/env python3
"""
List available Gemini models
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)

print("=" * 70)
print("📋 Available Gemini Models")
print("=" * 70)
print()

try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Description: {model.description}")
            print(f"   Methods: {', '.join(model.supported_generation_methods)}")
            print()
except Exception as e:
    print(f"❌ Error: {e}")

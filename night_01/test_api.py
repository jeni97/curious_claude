#!/usr/bin/env python3
"""Quick API connection test"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openai import OpenAI
from config.api_config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, MODEL

print("Testing API connection...")
print(f"Base URL: {DEEPSEEK_BASE_URL}")
print(f"Model: {MODEL}\n")

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL
)

try:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": "Say 'API working' if you can read this."}
        ],
        max_tokens=50
    )
    
    print("✅ API Response:")
    print(response.choices[0].message.content)
    print("\n✅ API connection successful!")
    
except Exception as e:
    print(f"❌ API connection failed: {e}")
    print("\nCheck:")
    print("- API key is correct")
    print("- Base URL is correct")
    print("- Model name is correct")

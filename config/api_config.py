"""API Configuration"""

import os

# DeepSeek API
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "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")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# Model settings
MODEL = "deepseek-reasoner"
MAX_TOKENS = 8000

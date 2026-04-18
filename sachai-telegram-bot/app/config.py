import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    SACH_AI_BACKEND_URL = os.getenv("SACH_AI_BACKEND_URL", "http://127.0.0.1:8000")
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "60"))

# Validate essential config early
if not Config.TELEGRAM_BOT_TOKEN or Config.TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
    print("CRITICAL ERROR: TELEGRAM_BOT_TOKEN is not set in .env")
    sys.exit(1)

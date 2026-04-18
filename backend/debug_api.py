import logging
logging.basicConfig(level=logging.ERROR)
from app.services.gemini_service import get_settings
import google.genai as genai

settings = get_settings()
print("API KEY:", settings.gemini_api_key)
client = genai.Client(api_key=settings.gemini_api_key)
try:
    client.models.generate_content(model='gemini-1.5-flash', contents='hello')
    print('SUCCESS')
except Exception as e:
    print('ERROR:', str(e))

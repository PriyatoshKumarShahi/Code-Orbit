import logging
logging.basicConfig(level=logging.ERROR)
from app.services.gemini_service import get_settings
import google.genai as genai

settings = get_settings()
print('API KEY:', settings.gemini_api_key[:10] + '...')
print('MODEL:', settings.gemini_model)
client = genai.Client(api_key=settings.gemini_api_key)
try:
    res = client.models.generate_content(model='gemini-2.5-flash', contents='hello')
    print('SUCCESS:', res.text)
except Exception as e:
    print('ERROR:', type(e).__name__, str(e))

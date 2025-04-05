import google.generativeai as genai
import os

try:
    api_key = os.environ.get('GOOGLE_API_KEY', '')
    print(f'API key exists: {bool(api_key)}')
    
    if not api_key:
        print('API key is not set in environment variables')
    else:
        genai.configure(api_key=api_key)
        for m in genai.list_models():
            print(m.name)
except Exception as e:
    print(f'API Error: {str(e)}')

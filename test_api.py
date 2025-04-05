import google.generativeai as genai
import os

try:
    api_key = os.environ.get('GOOGLE_API_KEY', '')
    print(f'API key exists: {bool(api_key)}')
    
    if not api_key:
        print('API key is not set in environment variables')
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content('Hello, this is a test. Please respond with API is working')
        print(f'API Response: {response.text}')
        print('API is working properly')
except Exception as e:
    print(f'API Error: {str(e)}')

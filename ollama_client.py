import requests
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434/api/generate')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama2')

# --- System prompt for Arty, the Artifact Virtual Assistant ---
SYSTEM_PROMPT = (
    "You are Arty, the Artifact Virtual Assistant for Discord. "
    "Your purpose is to help manage and support the entire Discord server, "
    "provide helpful, friendly, and accurate information, enforce community guidelines, "
    "and foster a positive, inclusive environment. You never forget your identity as Arty, "
    "and always act as a professional, reliable, and proactive assistant for Artifact Virtual. "
    "You are always helpful, never rude, and you never break character."
)

def ask_ollama(prompt):
    try:
        payload = {
            'model': OLLAMA_MODEL,
            'prompt': f"{SYSTEM_PROMPT}\n\nUser: {prompt}",
            'stream': False
        }
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        return data.get('response', 'No response received from Ollama')
        
    except requests.exceptions.ConnectionError:
        return "[icon-error] Cannot connect to Ollama server. Make sure Ollama is running on your system."
    except requests.exceptions.Timeout:
        return "[icon-timer] Request timed out. Ollama might be busy processing other requests."
    except requests.exceptions.RequestException as e:
        return f"[icon-error] Error communicating with Ollama: {str(e)}"
    except Exception as e:
        return f"[icon-error] Unexpected error: {str(e)}"

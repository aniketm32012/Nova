import os
import shutil
import urllib.request
import sys
import json

MODEL_NAME = "qwen2.5:1.5b"
OLLAMA_API_URL = "http://localhost:11434/api/tags"

def check_selenium():
    try:
        import selenium
        return True
    except ImportError:
        return False

def check_edge_tts():
    try:
        import edge_tts
        return True
    except ImportError:
        return False

def check_chrome():
    # 1. Check if chrome command is in system PATH
    if shutil.which("chrome") or shutil.which("chrome.exe"):
        return True

    # 2. Check standard Windows installation paths
    default_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    ]

    for path in default_paths:
        if os.path.exists(path):
            return True

    return False

def check_ollama():
    # 1. Check if 'ollama' executable exists in PATH
    if shutil.which("ollama") or shutil.which("ollama.exe"):
        return True

    # 2. Check standard installation directories on Windows
    default_paths = [
        os.path.expanduser(r"~\AppData\Local\Programs\Ollama\ollama.exe"),
        r"C:\Program Files\Ollama\ollama.exe"
    ]

    for path in default_paths:
        if os.path.exists(path):
            return True

    return False

def check_ollama_service():
    # Ping the local Ollama API server endpoint (default port 11434)
    try:
        url = "http://localhost:11434/api/tags"
        with urllib.request.urlopen(url, timeout=2) as response:
            return response.status == 200
    except Exception:
        return False

def check_python_version():
    # Returns True if Python is 3.12.0 or higher
    return sys.version_info >= (3, 12)


def check_qwen_model():
    try:
        req = urllib.request.Request(OLLAMA_API_URL)
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                models = [model.get("name") for model in data.get("models", [])]

                # Verify exact or prefixed match (e.g., qwen2.5:1.5b or qwen2.5:1.5b-instruct)
                for installed_model in models:
                    if installed_model.startswith(MODEL_NAME):
                        return True

                return False
    except urllib.error.URLError:
        return False
    except Exception as e:
        return False

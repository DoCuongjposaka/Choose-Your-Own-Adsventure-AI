#!/usr/bin/env python3
"""Test import trực tiếp"""

import sys
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Python path: {sys.path[:3]}")

try:
    import google.generativeai as genai
    print(f"✅ Google GenerativeAI: {genai.__version__}")
except ImportError as e:
    print(f"❌ Google GenerativeAI import error: {e}")
    print(f"Error type: {type(e)}")

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    print("✅ LangChain Google GenAI imported successfully")
except ImportError as e:
    print(f"❌ LangChain Google GenAI import error: {e}")
    print(f"Error type: {type(e)}")

try:
    import langchain_google_genai
    # Kiểm tra xem có __version__ attribute không
    if hasattr(langchain_google_genai, '__version__'):
        print(f"✅ LangChain Google GenAI version: {langchain_google_genai.__version__}")
    else:
        print("✅ LangChain Google GenAI imported successfully (version info not available)")
except ImportError as e:
    print(f"❌ LangChain Google GenAI version error: {e}")
    print(f"Error type: {type(e)}")
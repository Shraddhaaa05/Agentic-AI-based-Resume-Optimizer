# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # FREE MODEL THAT WORKS FOR EVERYONE:
    MODEL_NAME = "gemini-2.0-flash"  # This is the free model
    
    TEMPERATURE = 0.1
    MAX_TOKENS = 2000
    
    # File processing limits
    MAX_PDF_PAGES = 4
    MAX_TEXT_LENGTH = 4000
    
    
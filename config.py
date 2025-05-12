import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    CRYPTO_API_KEY = os.getenv("CRYPTO_API_KEY")
    MOVIES_API_KEY = os.getenv("MOVIES_API_KEY")
    AGRI_API_KEY = os.getenv("AGRI_API_KEY")

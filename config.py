import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # API configuration dictionary
    API_CONFIG = {
        "news_api": {
            "base_url": "https://example.com/news/",
            "headers": {
                "Authorization": f"Bearer {os.getenv('API_KEY_NEWS')}"
            },
            "params": {}
        },
        "weather_api": {
            "base_url": "https://example.com/weather/",
            "params": {
                "apikey": os.getenv("API_KEY_WEATHER")
            }
        },
        "crypto_api": {
            "base_url": "https://example.com/crypto/",
            "params": {
                "key": os.getenv("API_KEY_CRYPTO")
            }
        },
        "movies_api": {
            "base_url": "https://example.com/movies/",
            "params": {
                "apikey": os.getenv("API_KEY_MOVIES")
            }
        },
        "agri_api": {
            "base_url": "https://example.com/agriculture/",
            "params": {
                "key": os.getenv("API_KEY_AGRI")
            }
        },
        "sports_api": {
            "base_url": "https://example.com/sports/",
            "params": {
                "apikey": os.getenv("API_KEY_SPORTS")
            }
        },
        "stocks_api": {
            "base_url": "https://example.com/stocks/",
            "params": {
                "apikey": os.getenv("API_KEY_STOCKS")
            }
        },
        "finance_api": {
            "base_url": "https://example.com/finance/",
            "params": {
                "key": os.getenv("API_KEY_FINANCE")
            }
        },
        "health_api": {
            "base_url": "https://example.com/health/",
            "params": {
                "token": os.getenv("API_KEY_HEALTH")
            }
        },
        "education_api": {
            "base_url": "https://example.com/education/",
            "params": {
                "apikey": os.getenv("API_KEY_EDUCATION")
            }
        },
        "travel_api": {
            "base_url": "https://example.com/travel/",
            "params": {
                "apikey": os.getenv("API_KEY_TRAVEL")
            }
        },
        "books_api": {
            "base_url": "https://example.com/books/",
            "params": {
                "apikey": os.getenv("API_KEY_BOOKS")
            }
        },
        "music_api": {
            "base_url": "https://example.com/music/",
            "params": {
                "apikey": os.getenv("API_KEY_MUSIC")
            }
        },
        "traffic_api": {
            "base_url": "https://example.com/traffic/",
            "params": {
                "apikey": os.getenv("API_KEY_TRAFFIC")
            }
        },
        "shopping_api": {
            "base_url": "https://example.com/shopping/",
            "params": {
                "apikey": os.getenv("API_KEY_SHOPPING")
            }
        },
        "jobs_api": {
            "base_url": "https://example.com/jobs/",
            "params": {
                "apikey": os.getenv("API_KEY_JOBS")
            }
        },
        "events_api": {
            "base_url": "https://example.com/events/",
            "params": {
                "apikey": os.getenv("API_KEY_EVENTS")
            }
        },
        "trends_api": {
            "base_url": "https://example.com/trends/",
            "params": {
                "apikey": os.getenv("API_KEY_TRENDS")
            }
        },
        "transport_api": {
            "base_url": "https://example.com/transport/",
            "params": {
                "apikey": os.getenv("API_KEY_TRANSPORT")
            }
        },
        # Models Configuration
        "summarizer_api_key": {
            "base_url": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3",  # Summarizer Model
            "headers": {
                "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"  # For Summarizer
            },
            "params": {}
        },
        "reasoning_api_key": {
            "base_url": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3",  # Reasoning Model
            "headers": {
                "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY1')}"  # For Reasoning
            },
            "params": {}
        },
        "fallback_api_key": {
            "base_url": "https://api-inference.huggingface.co/models/google/flan-t5-large",  # Fallback Model
            "headers": {
                "Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY2')}"  # For Fallback
            },
            "params": {}
        }
    }

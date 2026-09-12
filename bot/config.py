import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

    WEATHER_CHANNEL_ID = int(os.getenv("WEATHER_CHANNEL_ID"))
    FORECAST_CHANNEL_ID = int(os.getenv("FORECAST_CHANNEL_ID"))
    ALERTS_CHANNEL_ID = int(os.getenv("ALERTS_CHANNEL_ID"))

    DEFAULT_CITY = "Wroclaw"
    LANG = "en"

settings = Settings()

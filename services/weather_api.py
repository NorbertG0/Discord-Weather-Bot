import requests

from bot.config import settings

class WeatherAPI:
    BASE_URL = "https://api.weatherapi.com/v1"

    def __init__(self):
        self.api_key = settings.WEATHER_API_KEY

    def _get(self, endpoint, params):
        params["key"] = self.api_key

        url = f"{self.BASE_URL}/{endpoint}"

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            return response.json(), None

        except requests.exceptions.Timeout:
            return None, "The server did not respond in time"

        except requests.exceptions.RequestException as error:
            print(f"Error fetching weather data: {error}")
            return None, "Error fetching weather data"

    def get_current_weather(self, city, lang):

        return self._get(
            "current.json",
            {
                "q": city,
                "aqi": "yes",
                "lang": lang,
            }
        )

    def get_forecast(self, city, days, lang="en", alerts="no", aqi="no"):

        return self._get(
            "forecast.json",
            {
                "q": city,
                "days": days,
                "lang": lang,
                "alerts": alerts,
                "aqi": aqi,
            }
        )

    def get_forecast_longterm(self, city, days="3", lang="en", alerts="yes", aqi="no"):

        return self._get(
            "forecast.json",
            {
                "q": city,
                "days": days,
                "lang": lang,
                "alerts": alerts,
                "aqi": aqi,
            }
        )

    def get_data_for_plot(self, city, days="1", alerts="no", aqi="no"):

        return self._get(
            "forecast.json",
            {
                "q": city,
                "days": days,
                "alerts": alerts,
                "aqi": aqi,
            }
        )
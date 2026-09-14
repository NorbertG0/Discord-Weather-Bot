from services.weather_api import WeatherAPI


class WeatherService:

    def __init__(self):
        self.api = WeatherAPI()

    def get_current_weather(self, city, lang="en"):

        data, error = self.api.get_current_weather(city, lang)

        if error:
            return None, error

        location = data["location"]
        current = data["current"]

        air_quality = current.get("air_quality", {})

        weather = {
            "city": location["name"],
            "country": location["country"],
            "last_updated": current["last_updated"],

            "temperature_c": current["temp_c"],
            "temperature_f": current["temp_f"],
            "is_day": "Night" if current["is_day"] == 0 else "Day",

            "wind_kph": current["wind_kph"],
            "pressure": current["pressure_mb"],
            "humidity": current["humidity"],

            "condition": current["condition"]["text"],
            "icon": current["condition"]["icon"],

            "co": air_quality.get("co"),
            "no2": air_quality.get("no2"),
            "o3": air_quality.get("o3"),
            "so2": air_quality.get("so2"),
            "pm2_5": air_quality.get("pm2_5"),
            "pm10": air_quality.get("pm10"),
        }

        return weather, None
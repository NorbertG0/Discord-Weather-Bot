import plotly.graph_objects as px
import io

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

    def get_forecast_today(self, city, lang="en", alerts="no", aqi="no"):

        data, error = self.api.get_forecast(city, lang, alerts, aqi)

        if error:
            return None, error

        location = data["location"]
        current = data["current"]
        forecast = data["forecast"]["forecastday"][0]["day"]

        weather = {
            "city": location["name"],
            "country": location["country"],
            "last_update": current["last_updated"],

            "maxtemp_c": forecast['maxtemp_c'],
            "maxtemp_f": forecast['maxtemp_f'],
            "mintemp_c": forecast['mintemp_c'],
            "mintemp_f": forecast['mintemp_f'],
            "avgtemp_c": forecast['avgtemp_c'],
            "avgtemp_f": forecast['avgtemp_f'],
            "maxwind_kph": forecast['maxwind_kph'],
            "totalprecip_mm": forecast['totalprecip_mm'],
            "totalsnow_cm": forecast['totalsnow_cm'],
            "avgvis_km": forecast['avgvis_km'],
            "avghumidity": forecast['avghumidity'],
            "daily_chance_of_rain": forecast['daily_chance_of_rain'],
            "daily_chance_of_snow": forecast['daily_chance_of_snow'],
            "uv": forecast['uv'],

            "text": forecast["condition"]["text"],
            "icon": forecast["condition"]["icon"],
        }

        return weather, None

    def get_forecast_longterm(self, city, days="3", lang="en", alerts="yes", aqi="no"):

        data, error = self.api.get_forecast_longterm(city, days, lang, alerts, aqi)

        if error:
            return None, error

        location = data["location"]
        current = data["current"]
        forecast = data["forecast"]["forecastday"]

        max_temp_day = {x['date'] : x['day']['maxtemp_c'] for x in forecast}
        text = {x['date'] : x['day']['condition']['text'] for x in forecast}

        weather = {
            "city": location["name"],
            "country": location["country"],

            "last_update": current["last_updated"],
            "max_temp_day": max_temp_day,
            "text": text,
        }

        return weather, None

    def create_plot(self, city, days="1", alerts="no", aqi="no"):

        data, error = self.api.get_data_for_plot(city, days, alerts, aqi)

        if error:
            return None, error

        forecast = data["forecast"]["forecastday"][0]["hour"]

        time = [x["time"] for x in forecast]
        temp = [x["temp_c"] for x in forecast]

        data = {"Hour": time, "Temp": temp}

        fig = px.line(data, x="Hour", y="Temp", title="Today's forecast graph")
        fig.show()
        buf = io.BytesIO()
        fig.write_image(buf, format="png")
        buf.seek(0)

        return buf, None
# ![discord](https://i.imgur.com/hvGaBRD.png) Discord Weather Bot
## Table of Contents
- [About](#-about)
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
  
## 🚀 About
A simple Discord bot written in Python that uses [WeatherAPI.com](https://www.weatherapi.com/) to provide weather-related data.
The bot can:

* Display current weather data for any city.
* Display weather forecasts for today or next three days.
* Send weather alerts for specific locations.
* Provide detailed air quality information for a selected city.
* Allow users to change the default city being tracked.
* Let users change the language of the weather data.

## ⚙️ Features

* **Current Weather**: Displays current weather details (temperature, humidity, wind speed, pressure and quality of air informations).
  <p align="center">
  <img src="https://i.imgur.com/WkNF8i7.png" />
  </p>
* **Weather Forecast**: Shows weather forecast for today or next three days.
  <p align="center">
  <img src="https://i.imgur.com/5RMxh4F.png" />
  </p>
* **Forecast Graph**: Creates a graph based on the weather forecast.
  <p align="center">
  <img src="https://i.imgur.com/kOhvH1o.png" />
  </p>
* **Weather Alerts**: Sends notifications about important weather events and alerts for selected city.
  <p align="center">
  <img src="https://i.imgur.com/PcgnnXz.png" />
  </p>
* **Air Quality Information**: Provides detailed air quality data such as AQI (Air Quality Index) for a city.
  <p align="center">
  <img src="https://i.imgur.com/hCqyuj4.png" />
  </p>
* **Default City Change**: Administrator can set or change the default city that the bot tracks.
  <p align="center">
  <img src="https://i.imgur.com/oKMSJrY.png" />
  </p>
* **Language Change**: Administrator can change the language of the weather data.
  <p align="center">
  <img src="https://i.imgur.com/yIIJamB.png" />
  </p>
* **Command Error Handling**: The bot detects and handles invalid commands or missing arguments.
  <p align="center">
  <img src="https://i.imgur.com/pe0ksxp.png" />
  </p>
  <p align="center">
  <img src="https://i.imgur.com/8tZK4SP.png" />
  </p>

## 🛠️ Installation

* Create an account on [WeatherAPI.com](https://www.weatherapi.com/)
* Get your API Key [Your API Key](https://www.weatherapi.com/my/)
  <p align="center">
  <img src="https://i.imgur.com/HzgaZgp.png" />
  </p>
* Create a  `.env` file and fill it out based on the example
  ```env
    DISCORD_TOKEN=your_discord_token
    WEATHER_API_KEY=your_weather_api_key
    WEATHER_CHANNEL_ID=your_weather_channel_id
    FORECAST_CHANNEL_ID=your_forecast_channel_id
    ALERTS_CHANNEL_ID=your_alert_channel_id
   ```
* Install Python packages
  ```sh
  pip install -r requirements.txt
   ```
  Packages documentation
  + [requests](https://pypi.org/project/requests/)
  + [discord.py](https://pypi.org/project/discord.py/)
  + [python-dotenv](https://pypi.org/project/python-dotenv/)
  + [plotly](https://pypi.org/project/plotly/)
  
## ✨ Usage
### Commands

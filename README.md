# ![discord](https://i.imgur.com/hvGaBRD.png) Discord Weather Bot
## Table of Contents
- [About](#-about)
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
  
## 🚀 About
<p align="justify">
This is a simple Discord bot written in Python that provides real-time weather information using WeatherAPI.com. The bot allows users to request weather data for any location—including current conditions, forecasts, temperature, humidity, wind speed, and more—and integrates seamlessly with Discord to enable interaction via text commands. Weather details are fetched from WeatherAPI.com and delivered in an easy-to-read format.

This project is my first major undertaking using Python. Through its development, I learned how API connections work, how to process and utilize received data, and how to handle JSON responses. Additionally, I gained valuable experience working with external libraries, structuring a Python project, creating GitHub repositories, and writing effective README documentation.
</p>

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

## 🛠️ Installation / Getting started

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
* Open the terminal and install Python packages
  ```sh
  pip install -r requirements.txt
   ```
  Packages documentation
  + [requests](https://pypi.org/project/requests/)
  + [discord.py](https://pypi.org/project/discord.py/)
  + [python-dotenv](https://pypi.org/project/python-dotenv/)
  + [plotly](https://pypi.org/project/plotly/)

* Execute the program
  ```sh
  python main.py
  ```
  
## ✨ Usage
### Commands

# ![discord](https://i.imgur.com/hvGaBRD.png) Discord Weather Bot
## Table of Contents
- [About](#-about)
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
  
## 🚀 About
<p align="justify">
This is a simple Discord bot written in Python that provides real-time weather information using WeatherAPI.com. Users can request weather data for any location, including current conditions, forecasts, temperature, humidity, wind speed, and more. The bot integrates seamlessly with Discord, allowing interaction through text commands. Weather details are fetched from WeatherAPI.com and presented in a clear, easy-to-read format.
</p>

## ⚙ Features

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

## 🛠 Installation
* Create and configure your bot on [Discord Developer Portal](https://discord.com/developers/applications)
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
  + To get your Discord token, click "Reset".
    <p align="center">
    <img src="https://i.imgur.com/qfStkrM.png" />
    </p>

  + You need to turn on developer mode in settings to see channels id's (right click on channel).
  
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
  If you have completed all the steps correctly, you should get this result in the console.
  <p align="center">
  <img src="https://i.imgur.com/Q15wQKq.png" />
  </p>
  The bot is now ready to work.
  
## ✨ Usage
### Commands
After running the program, type  `!commands` to see all available commands.

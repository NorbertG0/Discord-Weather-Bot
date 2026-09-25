# ![discord](https://i.imgur.com/hvGaBRD.png) Discord Weather Bot

## 🚀 About
<p align="justify">
Discord bot that provides weather information directly through Discord commands. The bot uses WeatherAPI.com to retrieve up-to-date weather data and presents it in a clear, easy-to-read format using Discord embeds.
</p>

## ⚙ Features

* **Current Weather**: Displays current weather details (temperature, humidity, wind speed, pressure and quality of air informations).
  <p align="center">
    <img width="49%" alt="image" src="https://github.com/user-attachments/assets/e9482833-32df-490c-aa50-0bbf2abeb923" />
    <img width="49%" alt="image" src="https://github.com/user-attachments/assets/630f6602-bc89-4cc4-a679-2e3f2e9fc6e9" />
  </p>
* **Weather Forecast**: Shows weather forecast for today or next three days.
  <p align="center">
   <img width="49%" alt="image" src="https://github.com/user-attachments/assets/719177a0-8e40-4a98-ae16-eb5187c55a48" />
      <img width="44%" alt="image" src="https://github.com/user-attachments/assets/6cde15e2-e88f-4d64-85ed-18837dde1e58" />
  </p>
* **Forecast Graph**: Creates a graph based on the weather forecast.
  <p align="center">
  <img width="44%" src="https://i.imgur.com/kOhvH1o.png" />
    <img width="45%" alt="image" src="https://github.com/user-attachments/assets/8f7af4bc-08c2-4984-8a96-b40fffdcf4a5" />
  </p>
* **Weather Alerts**: Sends notifications about important weather events and alerts for selected city.
  <p align="center">
  <img src="https://i.imgur.com/PcgnnXz.png" />
  </p>
* **Air Quality Information**: Provides detailed air quality data such as AQI (Air Quality Index) for a city.
  <p align="center">
  <img width="47%" src="https://i.imgur.com/hCqyuj4.png" />
    <img width="45%" alt="image" src="https://github.com/user-attachments/assets/474d49a8-d277-453b-bb0e-515d25434da3" />
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

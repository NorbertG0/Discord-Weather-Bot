from discord.ext import commands, tasks
import discord
import requests
import os
from dotenv import load_dotenv
import plotly.express as px
import io

# Dotenv data
load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')
weather_api_key = os.getenv('WEATHER_API_KEY')
weather_channel_id = int(os.getenv('WEATHER_CHANNEL_ID'))
forecast_channel_id = int(os.getenv('FORECAST_CHANNEL_ID'))
alerts_channel_id = int(os.getenv('ALERTS_CHANNEL_ID'))

# Discord intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents) #

# Global variables
default_city = 'Wroclaw' # Default city for task loop
buf = None # For plot
lang = 'en' # Default language

def get_current_weather_data(city):
    url = f'https://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}&aqi=yes&lang={lang}'

    # API response
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        response = response.json()
    except requests.exceptions.Timeout:
        print("The server did not respond in time")
        return None, 'The server did not respond in time'
    except requests.exceptions.RequestException as error:
        print(f'Error fetching weather data: {error}')
        return None, 'Error fetching weather data'

    # Data
    location = response['location']
    city_name = location['name']
    country = location['country']

    current = response['current']
    last_update = current['last_updated']
    temp_c = current['temp_c']
    temp_f = current['temp_f']
    is_day = current['is_day']
    wind_kph = current['wind_kph']
    pressure = current['pressure_mb']
    humidity = current['humidity']

    condition = current['condition']
    text = condition['text']
    icon = condition['icon']

    aiq = current['air_quality']
    co = aiq['co']
    no2 = aiq['no2']
    o3 = aiq['o3']
    so2 = aiq['so2']
    pm2_5 = aiq['pm2_5']
    pm10 = aiq['pm10']

    is_day = 'Night' if is_day == 0 else 'Day'

    return city_name, country, last_update, temp_c, temp_f, is_day, wind_kph, pressure, humidity, \
           text, icon, co, no2, o3, so2, pm2_5, pm10

def get_forecast_today_data(city):
    url = f'https://api.weatherapi.com/v1/forecast.json?q={city}&days=1&lang={lang}&alerts=disable&aqi=disable&key={weather_api_key}'

    # API response
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        response = response.json()
    except requests.exceptions.Timeout:
        print("The server did not respond in time")
        return None, 'The server did not respond in time'
    except requests.exceptions.RequestException as error:
        print(f'Error fetching weather data: {error}')
        return None, 'Error fetching weather data'

    # Data
    location = response['location']
    city = location['name']
    country = location['country']

    current = response['current']
    last_update = current['last_updated']

    forecast = response['forecast']['forecastday'][0]['day']
    maxtemp_c = forecast['maxtemp_c']
    maxtemp_f = forecast['maxtemp_f']
    mintemp_c = forecast['mintemp_c']
    mintemp_f = forecast['mintemp_f']
    avgtemp_c = forecast['avgtemp_c']
    avgtemp_f = forecast['avgtemp_f']
    maxwind_kph = forecast['maxwind_kph']
    totalprecip_mm = forecast['totalprecip_mm']
    totalsnow_cm = forecast['totalsnow_cm']
    avgvis_km = forecast['avgvis_km']
    avghumidity = forecast['avghumidity']
    daily_chance_of_rain = forecast['daily_chance_of_rain']
    daily_chance_of_snow = forecast['daily_chance_of_snow']
    uv = forecast['uv']

    condition = forecast['condition']
    text = condition['text']
    icon = condition['icon']

    return city, country, maxtemp_c, maxtemp_f, mintemp_c, mintemp_f, avgtemp_f, avgtemp_c,\
           maxwind_kph, totalsnow_cm, totalprecip_mm, avgvis_km, avghumidity, daily_chance_of_rain,\
           daily_chance_of_snow, uv, text, icon, last_update

def get_data_for_plot(city):
    global buf
    url = f'http://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q={city}&days=1&aqi=no&alerts=no'

    # API response
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        response = response.json()
    except requests.exceptions.Timeout:
        print("The server did not respond in time")
        return None, 'The server did not respond in time'
    except requests.exceptions.RequestException as error:
        print(f'Error fetching weather data: {error}')
        return None, 'Error fetching weather data'

    forecast = response['forecast']['forecastday'][0]['hour']

    time = [x['time'] for x in forecast]
    temp = [x['temp_c'] for x in forecast]

    data = {'Hour': time, 'Temperature': temp}

    # Creating plot
    fig = px.line(data, x='Hour', y='Temperature', title="Today's forecast graph")
    buf = io.BytesIO()
    fig.write_image(buf, format='png')
    buf.seek(0)
    return

def get_forecast_longterm_data(city):
    url = f'https://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q={city}&days=3&aqi=no&alerts=yes&lang={lang}' # <- API gives only 3 days forecast (limit?)

    # API response
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        response = response.json()
    except requests.exceptions.Timeout:
        print("The server did not respond in time")
        return None, 'The server did not respond in time'
    except requests.exceptions.RequestException as error:
        print(f'Error fetching weather data: {error}')
        return None, 'Error fetching weather data'

    # Data
    location = response['location']
    name = location['name']
    country = location['country']
    current = response['current']
    last_updated = current['last_updated']

    forecast = response['forecast']['forecastday']

    data = {x['date'] : x['day']['maxtemp_c'] for x in forecast}# {date : max_temp}
    text = {x['date'] : x['day']['condition']['text'] for x in forecast}# {date : weather_status}

    alerts = response['alerts']['alert']

    return name, country, last_updated, data, text, alerts

def validate_city_name(arg, command):
    if not arg:
        return f'⚠️ You must provide a city name! Use: `!{command} city_name` ⚠️'
    if arg.replace(' ', '').isalpha() == False:
        return '⚠️ The city name can only contain letters! ⚠️'
    if len(arg) > 30:
        return '⚠️ The city name is too long! Please provide a shorter name. ⚠️'
    return None

# Tasks loops
@tasks.loop(hours=24)# Automatically sending weather of the day (cooldown = 24h)
async def daily_weather():
    # Checking if channel exist
    channel = bot.get_channel(forecast_channel_id)
    if channel:
        weather = get_forecast_today_data(default_city)

        # Creating discord embed
        embed = discord.Embed(title=f'{weather[0]} ({weather[1]})  ~{weather[7]} ℃ ({weather[6]} °F)', description='', color=0x346eeb)
        embed.set_thumbnail(url='https:' + str(weather[17]))
        embed.add_field(name='――――――――――――――――――――――――――――――――', value='', inline=False)
        embed.add_field(name=str(weather[16]), value='', inline=False)
        embed.add_field(name=f'🌡️ 🔻 {str(weather[4])} ℃    🌡️ 🔺 {str(weather[2])} ℃   |   🌡️ 🔻 {str(weather[5])} °F    🌡️ 🔺 {str(weather[3])} °F',value='', inline=False)
        embed.add_field(name=f'💨 {str(weather[8])} km/h     ❄️ {str(weather[9])} cm ({str(weather[14])}%)     🌧️ {str(weather[10])} mm ({str(weather[13])}%)', value='', inline=False)
        embed.add_field(name=f'👁️ {str(weather[11])} km      💧 {str(weather[12])} %       ☀️ {str(weather[15])}', value='', inline=False)
        embed.add_field(name='――――――――――――――――――――――――――――――――', value='', inline=False)
        embed.set_footer(text='last update - ' + str(weather[18]))
        await channel.send(f"@here Today's forecast for {default_city}.")
        await channel.send(embed=embed)

@tasks.loop(hours=24)
async def alert():

    # Checking if channel exist
    channel = bot.get_channel(alerts_channel_id)
    if channel:
        alerts = get_forecast_longterm_data(default_city)[5]

        # Checking if there are any alerts for city
        if alerts == []:
            await channel.send(f'✅ There are no alerts for {default_city}. ✅')
            return
        for alert in alerts:

            # Creating discord embed
            embed = discord.Embed(title=f'⚠️ ‼️ Warning! ({alert["event"]}) ‼️ ⚠️ ', description=f'**{alert["headline"]}** {alert["areas"]} \n{alert["note"]}', color=0xfc0303)
            embed.add_field(name=f'**{alert["effective"]}  -  {alert["expires"]}**', value='', inline=False)
            embed.add_field(name=f'{alert["instruction"]}', value='', inline=False)
            await channel.send("@everyone ‼️ **ALERT FOR YOUR CITY** ‼️")
            await channel.send(embed=embed)

# Commands
@bot.command(name='weather')
@commands.cooldown(1, 5, commands.BucketType.user) # Command cooldown 1 command per 5 per 1 user
async def weather(ctx, *, arg=None):
    channel = bot.get_channel(weather_channel_id)

    # Validate city name
    error_msg = validate_city_name(arg, 'weather')
    if error_msg:
        await ctx.channel.send(error_msg)
        return

    # Checking if channel exist
    if channel:
        weather = get_current_weather_data(arg) # Getting current weather data

        #Creating discord embed
        embed = discord.Embed(title=f'{weather[0]} ({weather[1]}) | {weather[5]}', description='', color=0x346eeb)
        embed.set_thumbnail(url='https:' + str(weather[10]))
        embed.add_field(name='――――――――――――――――――――――――――――――――', value='', inline=False)
        embed.add_field(name=str(weather[9]), value='', inline=False)
        embed.add_field(name=f'🌡️ {str(weather[3])} ℃    🌡️ {str(weather[4])} °F    💨 {str(weather[6])} km/h    ⏱ ️{str(weather[7])} HPa      💧 {str(weather[8])} %', value='', inline=False)
        embed.add_field(name='――――――――――――――――――――――――――――――――', value='', inline=False)
        embed.add_field(name='Quality of air', value='', inline=False)
        embed.add_field(name=f'CO - {str(weather[11])} mg/m³      NO₂ - {str(weather[12])} µg/m³      PM₂ ̦₅ - {str(weather[15])} µg/m³', value='', inline=False)
        embed.add_field(name=f'O₃ - {str(weather[13])} µg/m³      SO₂ - {str(weather[14])} µg/m³      PM₁₀ - {str(weather[16])} µg/m³', value='', inline=False)
        embed.add_field(name='――――――――――――――――――――――――――――――――', value='', inline=False)
        embed.set_footer(text='last update - ' + str(weather[2]))
        await ctx.channel.send(embed=embed)

@bot.command(name='setcity') 
@commands.cooldown(1, 5, commands.BucketType.user) # Command cooldown 1 command per 5 per 1 user
@commands.has_permissions(administrator=True) # Permisson to use this command
async def set_city(ctx, *, arg=None):
    global default_city

    # Validate city name
    error_msg = validate_city_name(arg, 'setcity')
    if error_msg:
        await ctx.channel.send(error_msg)
        return

    default_city = arg # Set new default city (global var)
    await ctx.channel.send(f'✅ Succesfully changed city! Current city - {default_city} ✅')

@bot.command(name='setlang')
@commands.cooldown(1, 5, commands.BucketType.user) # Command cooldown 1 command per 5 per 1 user
@commands.has_permissions(administrator=True) # Permisson to use this command
async def set_lang(ctx, arg):
    global lang

    # Validate coutry code
    if len(arg) != 2:
        await ctx.channel.send('⚠️ The country code must be exactly 2 characters long! ⚠️')
        return
    if arg.isalpha() == False:
        await ctx.channel.send('⚠️ The coutry code can only contain letters! ⚠️')
        return
    if arg == None:
        await ctx.channel.send(f'⚠️ You must provide a country code! Use: `!setlang coutry code` ⚠️')
        return

    lang = arg # Set new default language (global var)
    await ctx.channel.send(f'✅ Succesfully changed language! Current language - {lang} ✅')

@bot.command(name='commands')
@commands.cooldown(1, 5, commands.BucketType.user) # Command cooldown 1 command per 5 per 1 user
async def show_commands(ctx):

    # Creating discord embed
    embed = discord.Embed(title='All available commands', description='', color=0x346eeb)
    embed.add_field(name='`!commands` - Shows all available commands.', value='', inline=False)
    embed.add_field(name='`!weather city_name` - Displays the current weather for the specified city.', value='', inline=False)
    embed.add_field(name='`!setcity city_name` - Sets a new default city for forecasts.', value='', inline=False)
    embed.add_field(name='`!setlang country_code` - Sets a new default language for short info.', value='', inline=False)
    embed.add_field(name='`!plot city_name` - Creates a temperature graph for the specified city.', value='', inline=False)
    embed.add_field(name='`!forecast city_name` - Shows a 3-day forecast for the specified city.', value='', inline=False)
    embed.add_field(name="`!forecasttoday city_name` - Shows today's forecast for the specified city.", value='', inline=False)
    embed.add_field(name='`!temperature city_name` - Displays the current temperature for the city.', value='', inline=False)
    embed.add_field(name='`!wind city_name` - Shows the current wind speed in the specified city.', value='', inline=False)
    embed.add_field(name='`!humidity city_name` - Displays the current humidity level in the city.', value='', inline=False)
    embed.add_field(name='`!pressure city_name` - Shows the current atmospheric pressure in the city.', value='', inline=False)
    embed.add_field(name='`!aqi city_name` - Shows the current air quality in the city.', value='', inline=False)
    await ctx.channel.send(embed=embed)

@bot.command(name='plot')
@commands.cooldown(1, 5, commands.BucketType.user) # Command cooldown 1 command per 5 per 1 user
async def plot(ctx, *, arg=None):

    # Validate city name
    error_msg = validate_city_name(arg, 'plot')
    if error_msg:
        await ctx.channel.send(error_msg)
        return

    get_data_for_plot(arg) # Creating plot for city
    file = discord.File(buf, filename='plot.png') # Getting file

    # Creating embed
    embed = discord.Embed(title=f'📊 Temperature graph ({arg})', color=0x346eeb)
    embed.set_image(url='attachment://plot.png')
    await ctx.send(embed=embed, file=file)

@bot.command(name='forecasttoday')
@commands.cooldown(1, 5, commands.BucketType.user) # Command cooldown 1 command per 5 per 1 user
async def forecast_today(ctx, *, arg=None):

    # Validate city name
    error_msg = validate_city_name(arg, 'forecasttoday')
    if error_msg:
        await ctx.channel.send(error_msg)
        return
    weather = get_forecast_today_data(arg) # Getting forecast data

    #Creating embed
    embed = discord.Embed(title=f'{weather[0]} ({weather[1]})  ~{weather[7]} ℃ ({weather[6]} °F)', description='',color=0x346eeb)
    embed.set_thumbnail(url='https:' + str(weather[17]))
    embed.add_field(name='――――――――――――――――――――――――――――――――', value='', inline=False)
    embed.add_field(name=str(weather[16]), value='', inline=False)
    embed.add_field(name=f'🌡️ 🔻 {str(weather[4])} ℃    🌡️ 🔺 {str(weather[2])} ℃   |   🌡️ 🔻 {str(weather[5])} °F    🌡️ 🔺 {str(weather[3])} °F', value='', inline=False)
    embed.add_field(name=f'💨 {str(weather[8])} km/h     ❄️ {str(weather[9])} cm ({str(weather[14])}%)     🌧️ {str(weather[10])} mm ({str(weather[13])}%)', value='', inline=False)
    embed.add_field(name=f'👁️ {str(weather[11])} km      💧 {str(weather[12])} %       ☀️ {str(weather[15])}', value='', inline=False)
    embed.add_field(name='――――――――――――――――――――――――――――――――', value='', inline=False)
    embed.set_footer(text='last update - ' + str(weather[18]))
    await ctx.channel.send(embed=embed)

@bot.command(name='temperature')
@commands.cooldown(1, 5, commands.BucketType.user) # Command cooldown 1 command per 5 per 1 user
async def temperature(ctx, *, arg=None):

    # Validate city name
    error_msg = validate_city_name(arg, 'temperature')
    if error_msg:
        await ctx.channel.send(error_msg)
        return

    weather = get_current_weather_data(arg) # Getting current weather data

    # Creating discord embed
    embed = discord.Embed(title=f'{weather[0]} ({weather[1]})', description=f'🌡️ {weather[3]}℃  ({weather[4]} °F)', color=0x346eeb)
    embed.set_thumbnail(url='https:' + str(weather[10]))
    embed.set_footer(text='last update - ' + str(weather[2]))
    await ctx.channel.send(embed=embed)

@bot.command(name='wind')
@commands.cooldown(1, 5, commands.BucketType.user) # Command cooldown 1 command per 5 per 1 user
async def wind(ctx, *, arg=None):

    #Validate city name
    error_msg = validate_city_name(arg, 'wind')
    if error_msg:
        await ctx.channel.send(error_msg)
        return

    weather = get_current_weather_data(arg) # Getting current weather data

    # Creating discord embed
    embed = discord.Embed(title=f'{weather[0]} ({weather[1]})', description=f'💨 {weather[6]} km/h', color=0x346eeb)
    embed.set_thumbnail(url='https:' + str(weather[10]))
    embed.set_footer(text='last update - ' + str(weather[2]))
    await ctx.channel.send(embed=embed)

@bot.command(name='humidity')
@commands.cooldown(1, 5, commands.BucketType.user) # Command cooldown 1 command per 5 per 1 user
async def humidity(ctx, *, arg=None):

    # Validate city name
    error_msg = validate_city_name(arg, 'humidity')
    if error_msg:
        await ctx.channel.send(error_msg)
        return

    weather = get_current_weather_data(arg) # Getting current weather data

    # Creating discord embed
    embed = discord.Embed(title=f'{weather[0]} ({weather[1]})', description=f'💧 {str(weather[8])} %', color=0x346eeb)
    embed.set_thumbnail(url='https:' + str(weather[10]))
    embed.set_footer(text='last update - ' + str(weather[2]))
    await ctx.channel.send(embed=embed)

@bot.command(name='pressure')
@commands.cooldown(1, 5, commands.BucketType.user) # Command cooldown 1 command per 5 per 1 user
async def pressure(ctx, *, arg=None):

    #Validate city name
    error_msg = validate_city_name(arg, 'pressure')
    if error_msg:
        await ctx.channel.send(error_msg)
        return

    weather = get_current_weather_data(arg) # Getting current weather data

    # Creating discord embed
    embed = discord.Embed(title=f'{weather[0]} ({weather[1]})', description=f'⏱ ️{str(weather[7])} HPa', color=0x346eeb)
    embed.set_thumbnail(url='https:' + str(weather[10]))
    embed.set_footer(text='last update - ' + str(weather[2]))
    await ctx.channel.send(embed=embed)

@bot.command(name='forecast')
@commands.cooldown(1, 5, commands.BucketType.user) # Command cooldown 1 command per 5 per 1 user
async def forecast(ctx, *, arg=None):

    # Validate city name
    error_msg = validate_city_name(arg, 'forecast')
    if error_msg:
        await ctx.channel.send(error_msg)
        return

    weather = get_forecast_longterm_data(arg) # Getting forecast data

    # Creating discord embed
    embed = discord.Embed(title=f'{weather[0]} ({weather[1]})  3-day forecast', description='', color=0x346eeb)
    for date, temp in weather[3].items():
        status = weather[4].get(date, 'No data')
        embed.add_field(name=f'📅  {str(date)}   -   🌡️  {str(temp)} ℃     ({status})', value='', inline=False)
    embed.set_footer(text='last update - ' + str(weather[2]))
    await ctx.channel.send(embed=embed)

@bot.command(name='aqi')
@commands.cooldown(1, 5, commands.BucketType.user) # Command cooldown 1 command per 5 per 1 user
async def air_quality(ctx, *, arg=None):

    # Validate city name
    error_msg = validate_city_name(arg, 'aqi')
    if error_msg:
        await ctx.channel.send(error_msg)
        return

    weather = get_current_weather_data(arg) # Getting current weather data

    # Creating discord embed
    embed = discord.Embed(title=f'{weather[0]} ({weather[1]})', description='', color=0x346eeb)
    embed.add_field(name='Quality of air', value='', inline=False)
    embed.add_field(name=f'CO - {str(weather[11])} mg/m³      NO₂ - {str(weather[12])} µg/m³      PM₂ ̦₅ - {str(weather[15])} µg/m³', value='', inline=False)
    embed.add_field(name=f'O₃ - {str(weather[13])} µg/m³      SO₂ - {str(weather[14])} µg/m³      PM₁₀ - {str(weather[16])} µg/m³', value='', inline=False)
    embed.set_footer(text='last update - ' + str(weather[2]))
    await ctx.channel.send(embed=embed)

# Events
@bot.event
async def on_command_error(ctx, error):

    # Sending a warning if command doesnt exist
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('⚠️ Unknown command! Type `!commands` to see the available commands. ⚠️')

@bot.event
async def on_ready():
    print(f'Successfully logged in ({bot.user})')
    daily_weather.start() # Running task loop
    print('Successfully started daily weather task loop')
    alert.start() # Running task loop
    print('Successfully started alert task loop')

# Running bot
bot.run(discord_token)
import discord
from discord.ext import commands, tasks

from bot.config import settings
from services.weather_service import WeatherService

class Tasks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.weather_service = WeatherService()

        self.daily_weather.start()
        self.alert.start()

    def cog_unload(self):
        self.daily_weather.cancel()
        self.alert.cancel()

    @tasks.loop(hours=24)
    async def daily_weather(self):
        channel = await self.bot.fetch_channel(settings.FORECAST_CHANNEL_ID)

        if channel is None:
            print("Daily weather task channel not found")
            return

        weather, error = self.weather_service.get_forecast_today(
            settings.DEFAULT_CITY,
            settings.LANG,
            "no",
            "no"
        )

        if error:
            print(f"Daily weather error: {error}")
            return

        embed = discord.Embed(
            title=(
                f'{weather["city"]} '
                f'({weather["country"]})  '
                f'~{weather["avgtemp_c"]} ℃ '
                f'({weather["avgtemp_f"]} °F)'
            ),
            description='',
            color=0x346eeb
        )

        embed.set_thumbnail(url='https:' + str(weather["icon"]))
        embed.add_field(name='――――――――――――――――――――――――――――――――', value='', inline=False)
        embed.add_field(name=str(weather["text"]), value='', inline=False)

        embed.add_field(
            name=(
                f'🌡️ 🔻 {weather["mintemp_c"]} ℃    '
                f'🌡️ 🔺 {weather["maxtemp_c"]} ℃   |   '
                f'🌡️ 🔻 {weather["mintemp_f"]} °F    '
                f'🌡️ 🔺 {weather["maxtemp_f"]} °F'
            ),
            value='',
            inline=False
        )

        embed.add_field(
            name=(
                f'💨 {weather["maxwind_kph"]} km/h     '
                f'❄️ {weather["totalsnow_cm"]} cm '
                f'({weather["daily_chance_of_snow"]}%)     '
                f'🌧️ {weather["totalprecip_mm"]} mm '
                f'({weather["daily_chance_of_rain"]}%)'
            ),
            value='',
            inline=False
        )

        embed.add_field(
            name=(
                f'👁️ {weather["avgvis_km"]} km      '
                f'💧 {weather["avghumidity"]} %       '
                f'☀️ {weather["uv"]}'
            ),
            value='',
            inline=False
        )

        embed.add_field(name='――――――――――――――――――――――――――――――――', value='', inline=False)
        embed.set_footer(text='last update - ' + str(weather["last_updated"]))

        await channel.send(f"@here Today's forecast for {settings.DEFAULT_CITY}.")
        await channel.send(embed=embed)

    @tasks.loop(hours=24)
    async def alert(self):
        channel = await self.bot.fetch_channel(settings.ALERTS_CHANNEL_ID)

        if channel is None:
            print("Alert task channel not found")
            return

        data, error = self.weather_service.get_forecast_longterm(
            settings.DEFAULT_CITY,
            "3",
            settings.LANG,
            "yes",
            "no"
        )

        if error:
            print(f"Alert error: {error}")
            return

        alerts = data["alerts"]

        if not alerts:
            await channel.send(f"There are no alerts for {settings.DEFAULT_CITY}.")
            return

        for alert in alerts:
            embed = discord.Embed(
                title=f'⚠️ ‼️ Warning! ({alert["event"]}) ‼️ ⚠️ ',
                description=(
                    f'**{alert["headline"]}** '
                    f'{alert["areas"]} \n'
                    f'{alert["note"]}'
                ),
                color=0xfc0303
            )

            embed.add_field(
                name=(
                    f'**{alert["effective"]}  -  '
                     f'{alert["expires"]}**'
                ),
                value='',
                inline=False
            )

            embed.add_field(name="Instructions", value=f'{alert["instruction"]}', inline=False)

            await channel.send("@everyone ‼️ **ALERT FOR YOUR CITY** ‼️")
            await channel.send(embed=embed)

    @daily_weather.before_loop
    async def before_daily_weather(self):
        await self.bot.wait_until_ready()

    @alert.before_loop
    async def before_alert(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Tasks(bot))
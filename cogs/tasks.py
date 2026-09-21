import discord
from discord.ext import commands, tasks
import logging

from bot.config import settings
from services.weather_service import WeatherService


logger = logging.getLogger(__name__)


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
        logger.info(
            "daily_weather (task) | Task started | city=%s | channel_id=%s",
            settings.DEFAULT_CITY, settings.FORECAST_CHANNEL_ID
        )

        try:
            channel = await self.bot.fetch_channel(settings.FORECAST_CHANNEL_ID)

        except discord.NotFound:
            logger.error(
                "daily_weather (task) | Task failed - channel not found | channel_id=%s",
                settings.FORECAST_CHANNEL_ID
            )

        except discord.Forbidden:
            logger.error(
                "daily_weather (task) | Task failed - missing permissions | channel_id=%s",
                settings.FORECAST_CHANNEL_ID
            )

        except discord.HTTPException:
            logger.exception(
                "daily_weather (task) | Task failed - failed to fetch channel | channel_id=%s",
                settings.FORECAST_CHANNEL_ID
            )

        weather, error = self.weather_service.get_forecast_today(
            settings.DEFAULT_CITY,
            settings.LANG,
            "no",
            "no"
        )

        if error:
            logger.warning(
                "daily_weather (task) | Forecast data error | city=%s | error=%s",
                settings.DEFAULT_CITY,
                error
            )
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

        try:
            await channel.send(f"@here Today's forecast for {settings.DEFAULT_CITY}.")
            await channel.send(embed=embed)

        except discord.Forbidden:
            logger.error(
                "daily_weather (task) | Missing permissions to send message | channel_id=%s",
                settings.FORECAST_CHANNEL_ID
            )
            return

        except discord.HTTPException:
            logger.exception(
                "daily_weather (task) | Failed to send forecast | city=%s",
                settings.DEFAULT_CITY
            )
            return

        logger.info(
            "daily_weather (task) | Forecast send successfully | city=%s | channel_id=%s",
            settings.DEFAULT_CITY,
            settings.FORECAST_CHANNEL_ID
        )

    @tasks.loop(hours=24)
    async def alert(self):
        logger.info(
            "alert (task) | Task started | city=%s | channel_id=%s",
            settings.DEFAULT_CITY, settings.ALERTS_CHANNEL_ID
        )

        try:
            channel = await self.bot.fetch_channel(settings.ALERTS_CHANNEL_ID)

        except discord.NotFound:
            logger.error(
                "alert (task) | Task failed - channel not found | channel_id=%s",
                settings.ALERTS_CHANNEL_ID
            )

        except discord.Forbidden:
            logger.error(
                "alert (task) | Task failed - missing permissions | channel_id=%s",
                settings.ALERTS_CHANNEL_ID
            )

        except discord.HTTPException:
            logger.exception(
                "alert (task) | Task failed - failed to fetch channel | channel_id=%s",
                settings.ALERTS_CHANNEL_ID
            )

        data, error = self.weather_service.get_forecast_longterm(
            settings.DEFAULT_CITY,
            "3",
            settings.LANG,
            "yes",
            "no"
        )

        if error:
            logger.warning(
                "alert (task) | Forecast data error | city=%s | error=%s",
                settings.DEFAULT_CITY,
                error
            )
            return

        alerts = data["alerts"]

        if not alerts:
            logger.info(
                "alert (task) | Alert not found | city=%s | channel_id=%s",
                settings.DEFAULT_CITY,
                settings.ALERTS_CHANNEL_ID
            )
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

            try:
                await channel.send("@everyone ‼️ **ALERT FOR YOUR CITY** ‼️")
                await channel.send(embed=embed)

            except discord.Forbidden:
                logger.error(
                    "alert (task) | Missing permissions to send message | channel_id=%s",
                    settings.ALERTS_CHANNEL_ID
                )
                return

            except discord.HTTPException:
                logger.exception(
                    "alert (task) | Failed to send forecast | city=%s",
                    settings.DEFAULT_CITY
                )
                return

            logger.info(
                "alert (task) | Alert send successfully | city=%s | channel_id=%s",
                settings.DEFAULT_CITY,
                settings.ALERTS_CHANNEL_ID
            )

    @daily_weather.before_loop
    async def before_daily_weather(self):
        await self.bot.wait_until_ready()

    @alert.before_loop
    async def before_alert(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Tasks(bot))
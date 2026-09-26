import discord
import logging

from discord.ext import commands

from bot.config import settings
from services.weather_service import WeatherService
from utils.validators import validate_city_name


logger = logging.getLogger(__name__)


class Weather(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.weather_service = WeatherService()

    @commands.command(name="weather")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def weather(self, ctx, *, city_name=None):
        error_msg = validate_city_name(city_name, "weather")

        if error_msg:
            logger.warning(
                "!weather | Validation error | user=%s | city=%s",
                ctx.author,
                city_name
            )
            await ctx.send(error_msg)
            return

        channel = self.bot.get_channel(settings.WEATHER_CHANNEL_ID)

        if channel is None:
            logger.error(
                "!weather | Channel not found | channel_if=%s",
                settings.WEATHER_CHANNEL_ID
            )
            await ctx.send("Weather channel not found.")
            return

        weather, error = self.weather_service.get_current_weather(city_name, settings.LANG)

        if error:
            logger.warning(
                "!weather | Weather data error | user=%s | city=%s | error=%s",
                ctx.author,
                city_name,
                error
            )
            await ctx.send("⚠️ Unable to retrieve weather data right now. Please try again later.")
            return

        logger.info(
            "!weather | Weather retrieved | user=%s | city=%s",
            ctx.author,
            city_name
        )

        embed = discord.Embed(
            title=(
                f'{weather["city"]} '
                f'({weather["country"]}) | '
                f'{weather["is_day"]}'
            ),
            color=0x346eeb
        )

        embed.set_thumbnail(url="https:" + weather["icon"])

        embed.add_field(
            name=weather["condition"],
            value="",
            inline=False
        )

        embed.add_field(
            name=(
                f'🌡️ {weather["temperature_c"]} ℃    '
                f'🌡️ {weather["temperature_f"]} °F    '
                f'💨 {weather["wind_kph"]} km/h    '
                f'⏱️ {weather["pressure"]} hPa    '
                f'💧 {weather["humidity"]} %'
            ),
            value="",
            inline=False
        )

        embed.add_field(name=" ", value="", inline=False)
        embed.add_field(name='Quality of air', value='', inline=False)

        embed.add_field(
            name=(
                f'CO - {weather["co"]} mg/m³      '
                f'NO₂ - {weather["no2"]} µg/m³      '
                f'PM₂ ̦₅ - {weather["pm2_5"]} µg/m³'
            ),
            value='',
            inline=False
        )

        embed.add_field(
            name=(
                f'O₃ - {weather["o3"]} µg/m³           '
                f'SO₂ - {weather["so2"]} µg/m³        '
                f'PM₁₀ - {weather["pm10"]} µg/m³'
            ),
            value='',
            inline=False
        )

        embed.add_field(name=" ", value="", inline=False)
        embed.set_footer(text=f'last update - {weather["last_updated"]}')

        await ctx.send(embed=embed)

        logger.info(
            "!weather | Weather send | user=%s | city=%s",
            ctx.author,
            city_name
        )

    @commands.command(name="tempchart")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def temperature_chart(self, ctx, *, city_name=None):
        error_msg = validate_city_name(city_name, "tempchart")

        if error_msg:
            logger.warning(
                "!tempchart | Validation error | user=%s | city=%s",
                ctx.author,
                city_name
            )
            await ctx.channel.send(error_msg)
            return

        plot_data, error = self.weather_service.create_temperature_chart(city_name, days="1", alerts="no", aqi="no")

        if error:
            logger.warning(
                "!tempchart | Weather data error | user=%s | city=%s | error=%s",
                ctx.author,
                city_name,
                error
            )
            await ctx.send("⚠️ Unable to retrieve weather data right now. Please try again later.")
            return

        try:
            file = discord.File(plot_data, filename="plot.png")

            embed = discord.Embed(title=f'📊 Temperature graph ({city_name})', color=0x346eeb)
            embed.set_image(url='attachment://plot.png')

        except Exception:
            logger.exception(
                "!tempchart | Plot creation error | city=%s",
                city_name
            )
            await ctx.send("⚠️ Failed to create temperature graph.")
            return

        await ctx.send(embed=embed, file=file)

        logger.info(
            "!tempchart | Weather plot send | user=%s | city=%s",
            ctx.author,
            city_name
        )

    @commands.command(name="temperature")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def temperature(self, ctx, *, city_name=None):
        error_msg = validate_city_name(city_name, "temperature")

        if error_msg:
            logger.warning(
                "!temperature | Validation error | user=%s | city=%s",
                ctx.author,
                city_name
            )
            await ctx.channel.send(error_msg)
            return

        weather, error = self.weather_service.get_current_weather(city_name, settings.LANG)

        logger.info(
            "!temperature | Temperature data retrieved | user=%s | city=%s",
            ctx.author,
            city_name
        )

        embed = discord.Embed(
            title=(
                f'{weather["city"]} '
                f'({weather["country"]})'
            ),
            description=(
                f'🌡️ {weather["temperature_c"]}℃  '
                f'({weather["temperature_f"]} °F)'
            ),
            color=0x346eeb
        )

        embed.set_thumbnail(url='https:' + str(weather["icon"]))
        embed.set_footer(text='last update - ' + str(weather["last_updated"]))

        await ctx.channel.send(embed=embed)

        logger.info(
            "!temperature | Temperature send | user=%s | city=%s",
            ctx.author,
            city_name
        )

    @commands.command(name="wind")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wind(self, ctx, *, city_name=None):
        error_msg = validate_city_name(city_name, "wind")

        if error_msg:
            logger.warning(
                "!wind | Validation error | user=%s | city=%s",
                ctx.author,
                city_name
            )
            await ctx.channel.send(error_msg)
            return

        weather, error = self.weather_service.get_current_weather(city_name, settings.LANG)

        logger.info(
            "!wind | Wind data retrieved | user=%s | city=%s",
            ctx.author,
            city_name
        )

        embed = discord.Embed(
            title=(
                f'{weather["city"]} '
                f'({weather["country"]})'
            ),
            description=f'💨 {weather["wind_kph"]} km/h',
            color=0x346eeb
        )

        embed.set_thumbnail(url='https:' + str(weather["icon"]))
        embed.set_footer(text='last update - ' + str(weather["last_updated"]))

        await ctx.channel.send(embed=embed)

        logger.info(
            "!wind | Wind data send | user=%s | city=%s",
            ctx.author,
            city_name
        )

    @commands.command(name="humidity")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def humidity(self, ctx, *, city_name=None):
        error_msg = validate_city_name(city_name, "humidity")

        if error_msg:
            logger.warning(
                "!humidity | Validation error | user=%s | city=%s",
                ctx.author,
                city_name
            )
            await ctx.channel.send(error_msg)
            return

        weather, error = self.weather_service.get_current_weather(city_name, settings.LANG)

        logger.info(
            "!humidity | Humidity data retrieved | user=%s | city=%s",
            ctx.author,
            city_name
        )

        embed = discord.Embed(
            title=(
                f'{weather["city"]} '
                f'({weather["country"]})'
            ),
            description=f'💧 {str(weather["humidity"])} %',
            color=0x346eeb
        )

        embed.set_thumbnail(url='https:' + str(weather["icon"]))
        embed.set_footer(text='last update - ' + str(weather["last_updated"]))

        await ctx.channel.send(embed=embed)

        logger.info(
            "!humidity | Humidity data send | user=%s | city=%s",
            ctx.author,
            city_name
        )

    @commands.command(name="pressure")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pressure(self, ctx, *, city_name=None):
        error_msg = validate_city_name(city_name, "pressure")

        if error_msg:
            logger.warning(
                "!pressure | Validation error | user=%s | city=%s",
                ctx.author,
                city_name
            )
            await ctx.channel.send(error_msg)
            return

        weather, error = self.weather_service.get_current_weather(city_name, settings.LANG)

        logger.info(
            "!pressure | Pressure data retrieved | user=%s | city=%s",
            ctx.author,
            city_name
        )

        embed = discord.Embed(
            title=(
                f'{weather["city"]} '
                f'({weather["country"]})'
            ),
            description=f'⏱ ️{str(weather["pressure"])} HPa',
            color=0x346eeb
        )

        embed.set_thumbnail(url='https:' + str(weather["icon"]))
        embed.set_footer(text='last update - ' + str(weather["last_updated"]))

        await ctx.channel.send(embed=embed)
        logger.info(
            "!pressure | Pressure data send | user=%s | city=%s",
            ctx.author,
            city_name
        )

    @commands.command(name="aqi")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def air_quality(self, ctx, *, city_name=None):
        error_msg = validate_city_name(city_name, "air_quality")

        if error_msg:
            logger.warning(
                "!aqi | Validation error | user=%s | city=%s",
                ctx.author,
                city_name
            )
            await ctx.channel.send(error_msg)
            return

        weather, error = self.weather_service.get_current_weather(city_name, settings.LANG)

        logger.info(
            "!aqi | Air quality data retrieved | user=%s | city=%s",
            ctx.author,
            city_name
        )

        embed = discord.Embed(
            title=(
                f'{weather["city"]} '
                f'({weather["country"]})'
            ),
            description='',
            color=0x346eeb
        )

        embed.add_field(name='Quality of air', value='', inline=False)

        embed.add_field(
            name=(
                f'CO - {weather["co"]} mg/m³      '
                f'NO₂ - {weather["no2"]} µg/m³      '
                f'PM₂ ̦₅ - {weather["pm2_5"]} µg/m³'
            ),
            value='',
            inline=False
        )

        embed.add_field(
            name=(
                f'O₃ - {weather["o3"]} µg/m³      '
                f'SO₂ - {weather["so2"]} µg/m³      '
                f'PM₁₀ - {weather["pm10"]} µg/m³'
            ),
            value='',
            inline=False
        )

        embed.set_footer(text='last update - ' + str(weather["last_updated"]))

        await ctx.channel.send(embed=embed)

        logger.info(
            "!aqi | Air quality data send | user=%s | city=%s",
            ctx.author,
            city_name
        )


async def setup(bot):
    await bot.add_cog(Weather(bot))
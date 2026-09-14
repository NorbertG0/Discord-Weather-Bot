import discord

from discord.ext import commands

from bot.config import settings
from services.weather_service import WeatherService
from utils.validators import validate_city_name


class Weather(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.weather_service = WeatherService()

    @commands.command(name="weather")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def weather(self, ctx, *, arg=None):
        error_msg = validate_city_name(arg, "weather")

        if error_msg:
            await ctx.send(error_msg)
            return

        channel = self.bot.get_channel(settings.WEATHER_CHANNEL_ID)

        if channel is None:
            await ctx.send("Weather channel not found.")
            return

        weather, error = self.weather_service.get_current_weather(arg, settings.LANG)

        if error:
            await ctx.send(f"⚠️ {error}")
            return

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

        embed.set_footer(text=f'last update - {weather["last_updated"]}')

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Weather(bot))
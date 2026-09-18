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
    async def weather(self, ctx, *, city_name=None):
        error_msg = validate_city_name(city_name, "weather")

        if error_msg:
            await ctx.send(error_msg)
            return

        channel = self.bot.get_channel(settings.WEATHER_CHANNEL_ID)

        if channel is None:
            await ctx.send("Weather channel not found.")
            return

        weather, error = self.weather_service.get_current_weather(city_name, settings.LANG)

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

    @commands.command(name="plot")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def plot(self, ctx, *, city_name=None):
        error_msg = validate_city_name(city_name, "plot")

        if error_msg:
            await ctx.channel.send(error_msg)
            return

        plot, error = self.weather_service.create_plot(city_name, days="1", alerts="no", aqi="no")

        if error:
            await ctx.send(f"⚠️ {error}")
            return

        file = discord.File(plot, filename="plot.png")

        embed = discord.Embed(title=f'📊 Temperature graph ({city_name})', color=0x346eeb)
        embed.set_image(url='attachment://plot.png')

        await ctx.send(embed=embed, file=file)

    @commands.command(name="temperature")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def temperature(self, ctx, *, city_name=None):
        error_msg = validate_city_name(city_name, "temperature")

        if error_msg:
            await ctx.channel.send(error_msg)
            return

        weather, error = self.weather_service.get_current_weather(city_name, settings.LANG)

        embed = discord.Embed(
            title=f'{weather["city"]} ({weather["country"]})',
            description=f'🌡️ {weather["temperature_c"]}℃  ({weather["temperature_f"]} °F)',
            color=0x346eeb
        )

        embed.set_thumbnail(url='https:' + str(weather["icon"]))
        embed.set_footer(text='last update - ' + str(weather["last_updated"]))

        await ctx.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Weather(bot))
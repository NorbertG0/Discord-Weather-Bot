import discord
from discord.ext import commands

from bot.config import settings
from services.weather_service import WeatherService
from utils.validators import validate_city_name

class Forecast(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.weather_service = WeatherService()

    @commands.command(name='forecasttoday')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def forecasttoday(self, ctx, *, city_name=None):
        error_msg = validate_city_name(city_name, "forecasttoday")

        if error_msg:
            await ctx.channel.send(error_msg)
            return

        forecast, error = self.weather_service.get_forecast_today(
            city_name,
            settings.LANG,
            "no",
            "no"
        )

        if error:
            await ctx.channel.send(f"⚠️ {error}")
            return

        embed = discord.Embed(
            title=(f'{forecast["city"]} '
                  f'({forecast["country"]})  '
                  f'~{forecast["avgtemp_c"]} ℃ '
                  f'({forecast["avgtemp_f"]} °F)'
            ),
            description='',
            color=0x346eeb,
        )

        embed.set_thumbnail(url='https:' + str(forecast["icon"]))
        embed.add_field(name='――――――――――――――――――――――――――――――――', value='', inline=False)
        embed.add_field(name=str(forecast["text"]), value='', inline=False)
        embed.add_field(
            name=(f'🌡️ 🔻 {forecast["mintemp_c"]} ℃'
                 f'    🌡️ 🔺 {forecast["maxtemp_c"]} ℃   |   '
                 f'🌡️ 🔻 {forecast["mintemp_f"]} °F    '
                 f'🌡️ 🔺 {forecast["maxtemp_f"]} °F'
            ),
            value='',
            inline=False,
        )

        embed.add_field(
            name=(f'💨 {forecast["maxwind_kph"]} km/h     '
                  f'❄️ {forecast["totalsnow_cm"]} cm '
                  f'({forecast["daily_chance_of_snow"]}%)     '
                  f'🌧️ {forecast["totalprecip_mm"]} mm '
                  f'({forecast["daily_chance_of_rain"]}%)'
            ),
            value='',
            inline=False,
        )

        embed.add_field(
            name=(f'👁️ {forecast["avgvis_km"]} km      '
                  f'💧 {forecast["avghumidity"]} %       '
                  f'☀️ {forecast["uv"]}'
            ),
            value='',
            inline=False,
        )

        embed.add_field(name='――――――――――――――――――――――――――――――――', value='', inline=False)
        embed.set_footer(text='last update - ' + str(forecast["last_updated"]))

        await ctx.send(embed=embed)

    @commands.command(name='forecast')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def forecast(self, ctx, *, city_name=None):
        error_msg = validate_city_name(city_name, "forecast")

        if error_msg:
            await ctx.channel.send(error_msg)
            return

        forecast, error = self.weather_service.get_forecast_longterm(
            city_name,
            "3",
            settings.LANG,
            "yes",
            "no"
        )

        if error:
            await ctx.channel.send(error_msg)

        embed = discord.Embed(
            title=(f'{forecast["city"]} '
                  f'({forecast["country"]})  3-day forecast'
            ),
            description='',
            color=0x346eeb,
        )

        for date, temp in forecast["max_temp_day"].items():
            status = forecast["text"].get(date, 'No data')
            embed.add_field(
                name=(f'📅  {date}   -   '
                     f'🌡️  {temp} ℃     '
                     f'({status})'
                ),
                value='',
                inline=False,
            )

        embed.set_footer(text='last update - ' + str(forecast["last_update"]))

        await ctx.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Forecast(bot))





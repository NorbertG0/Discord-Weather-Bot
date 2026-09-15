import discord
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='commands')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def show_commands(self, ctx):
        embed = discord.Embed(title='All available commands', description='', color=0x346eeb)
        embed.add_field(name='`!commands` - Shows all available commands.', value='', inline=False)
        embed.add_field(
            name='`!weather city_name` - Displays the current weather for the specified city.',
            value='',
            inline=False,
        )

        embed.add_field(
            name='`!setcity city_name` - Sets a new default city for forecasts.',
            value='',
            inline=False,
        )

        embed.add_field(
                name='`!setlang country_code` - Sets a new default language for short info.',
                value='',
                inline=False
        )

        embed.add_field(
            name='`!plot city_name` - Creates a temperature graph for the specified city.',
            value='',
            inline=False,
        )

        embed.add_field(
            name='`!forecast city_name` - Shows a 3-day forecast for the specified city.',
            value='',
            inline=False,
        )

        embed.add_field(
            name="`!forecasttoday city_name` - Shows today's forecast for the specified city.",
            value='',
            inline=False,
        )

        embed.add_field(
            name='`!temperature city_name` - Displays the current temperature for the city.',
            value='',
            inline=False,
        )

        embed.add_field(
            name='`!wind city_name` - Shows the current wind speed in the specified city.',
            value='',
            inline=False,
        )

        embed.add_field(
            name='`!humidity city_name` - Displays the current humidity level in the city.',
            value='',
            inline=False,
        )

        embed.add_field(
            name='`!pressure city_name` - Shows the current atmospheric pressure in the city.',
            value='',
            inline=False,
        )

        embed.add_field(
            name='`!aqi city_name` - Shows the current air quality in the city.',
            value='',
            inline=False,
        )

        await ctx.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Commands(bot))
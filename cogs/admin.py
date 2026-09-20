from discord.ext import commands
import logging

from bot.config import settings
from utils.validators import validate_city_name


logger = logging.getLogger(__name__)


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setcity")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def set_city(self, ctx, *, city_name=None):
        error_msg = validate_city_name(city_name, "setcity")

        if error_msg:
            logger.warning("!setcity | Invalid !setcity attempt | user=%s",ctx.author)
            await ctx.send(error_msg)
            return

        old_city_name = settings.DEFAULT_CITY
        settings.DEFAULT_CITY = city_name

        logger.info(
            "!setcity | Default city changed | user=%s | old=%s | new=%s",
            ctx.author,
            old_city_name,
            city_name
        )

        await ctx.send(f"✅ Default city changed to **{city_name}**.")

    @commands.command(name="setlang")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def setlang(self, ctx, language=None):

        if language is None:
            logger.warning("!setlang | Invalid !setlang attempt | user=%s", ctx.author)
            await ctx.send("❌ Usage: `!setlang country code` example: `!setlang en`")
            return

        language = language.lower()

        old_language = settings.LANG
        settings.LANG = language

        logger.info(
            f"!setlang | Default language changed | user=%s | old=%s | new=%s",
            ctx.author,
            old_language,
            language
        )

        await ctx.send(f"✅ Language changed to **{language}**.")


async def setup(bot):
    await bot.add_cog(Admin(bot))
import asyncio

from bot.client import create_bot
from bot.config import settings
from utils.logger import setup_logger

async def main():
    setup_logger()

    bot = create_bot()

    async with bot:
        await bot.load_extension("cogs.weather")
        await bot.load_extension("cogs.forecast")
        await bot.load_extension("cogs.admin")
        await bot.load_extension("cogs.info")
        await bot.load_extension("cogs.tasks")
        await bot.start(settings.DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
import asyncio

from bot.client import create_bot
from bot.config import settings

async def main():
    bot = create_bot()

    async with bot:
        await bot.load_extension("cogs.weather")
        await bot.load_extension("cogs.forecast")
        await bot.start(settings.DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
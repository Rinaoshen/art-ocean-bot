import os
import asyncio
import logging
from bot.bot import ArtOceanBot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    if not BOT_TOKEN:
        logger.error("Set TELEGRAM_BOT_TOKEN environment variable!")
        return

    art_bot = ArtOceanBot(BOT_TOKEN)

    # Запуск бота и параллельный запуск проверки новых возможностей
    async def run_bot():
        await art_bot.application.run_polling()

    async def run_checker():
        await art_bot.periodic_check(interval_seconds=3600)  # Каждые 60 минут

    await asyncio.gather(run_bot(), run_checker())

if __name__ == '__main__':
    asyncio.run(main())

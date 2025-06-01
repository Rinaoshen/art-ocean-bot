import asyncio
import os
from bot.bot import ArtOceanBot

async def main():
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    if not telegram_token:
        raise ValueError("TELEGRAM_TOKEN не найден в переменных окружения")

    art_bot = ArtOceanBot(telegram_token)

    # Отправка новых возможностей при запуске
    await art_bot.send_new_opportunities()

    # Запуск бота
    await art_bot.application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

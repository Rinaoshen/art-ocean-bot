import os
import logging
from telegram.ext import Application, CommandHandler
from bot import ArtOceanBot  # Импорт основного класса бота из bot.py

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен твоего бота
BOT_TOKEN = '8151684930:AAG8u2Gg3oPmOA7sl5-XamwWt57tMyIcLLI'

def main():
    # Создаем экземпляр бота
    art_bot = ArtOceanBot(BOT_TOKEN)

    logger.info("🚀🌊 Запуск Art Ocean Bot...")
    # Запускаем бота в режиме опроса (polling)
    art_bot.application.run_polling()

if __name__ == '__main__':
    main()

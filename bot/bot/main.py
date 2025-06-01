import os
import logging
from telegram import Bot
from telegram.ext import Application, CommandHandler
from bot.handlers import register_handlers
from bot.storage import load_data, save_data

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class ArtOceanBot:
    def __init__(self, telegram_token: str):
        self.bot = Bot(token=telegram_token)
        self.application = Application.builder().token(telegram_token).build()
        self.subscribers, self.seen_opportunities = load_data()
        register_handlers(self)

    def run(self):
        logger.info("🚀🌊 Starting Art Ocean Bot...")
        self.application.run_polling()

def main():
    token = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
    if token == 'YOUR_BOT_TOKEN_HERE':
        logger.error("Please set TELEGRAM_BOT_TOKEN environment variable")
        return
    bot = ArtOceanBot(token)
    bot.run()

if __name__ == '__main__':
    main()

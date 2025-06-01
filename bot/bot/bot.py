import os
import json
import logging
from telegram import Bot
from telegram.ext import Application, CommandHandler
from bot.opportunity import Opportunity
from parsers.artconnect import parse_artconnect

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class ArtOceanBot:
    def __init__(self, telegram_token: str):
        self.bot = Bot(token=telegram_token)
        self.application = Application.builder().token(telegram_token).build()
        self.subscribers = set()
        self.seen_opportunities = set()
        self.load_data()

        # Обработчики команд
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("subscribe", self.subscribe_command))
        self.application.add_handler(CommandHandler("unsubscribe", self.unsubscribe_command))
        self.application.add_handler(CommandHandler("status", self.status_command))

    def load_data(self):
        """Загрузка сохраненных данных"""
        try:
            with open('data/subscribers.json', 'r') as f:
                self.subscribers = set(json.load(f))
        except FileNotFoundError:
            self.subscribers = set()

        try:
            with open('data/seen_opportunities.json', 'r') as f:
                self.seen_opportunities = set(json.load(f))
        except FileNotFoundError:
            self.seen_opportunities = set()

    def save_data(self):
        """Сохранение данных"""
        os.makedirs("data", exist_ok=True)
        with open('data/subscribers.json', 'w') as f:
            json.dump(list(self.subscribers), f)

        with open('data/seen_opportunities.json', 'w') as f:
            json.dump(list(self.seen_opportunities), f)

    async def start_command(self, update, context):
        welcome_text = """
🎨🌊 **Добро пожаловать в Art Ocean Bot!**

Я нахожу для вас актуальные арт-возможности:
• 💰 Гранты
• 🏠 Резиденции  
• 📢 Open Call'ы
• 🏆 Конкурсы
• 🎨 Выставки

📬 Нажмите /subscribe, чтобы получать их первыми!
        """
        await update.message.reply_text(welcome_text, parse_mode='Markdown')

    async def help_command(self, update, context):
        help_text = """
🤖 **Помощь по Art Ocean Bot**

/subscribe — подписаться на рассылку  
/unsubscribe — отписаться  
/status — ваш статус  
/start — начать  
/help — справка

Я присылаю возможности для художников из проверенных источников.
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def subscribe_command(self, update, context):
        user_id = update.effective_user.id
        self.subscribers.add(user_id)
        self.save_data()
        await update.message.reply_text("✅ Вы подписаны!", parse_mode='Markdown')

    async def unsubscribe_command(self, update, context):
        user_id = update.effective_user.id
        self.subscribers.discard(user_id)
        self.save_data()
        await update.message.reply_text("❌ Вы отписаны.", parse_mode='Markdown')

    async def status_command(self, update, context):
        user_id = update.effective_user.id
        status = "✅ Подписан" if user_id in self.subscribers else "❌ Не подписан"
        total = len(self.subscribers)
        await update.message.reply_text(
            f"📊 Статус: {status}\n👥 Подписчиков: {total}\n🔍 Найдено возможностей: {len(self.seen_opportunities)}",
            parse_mode='Markdown'
        )

    async def send_new_opportunities(self):
        """Парсинг и рассылка новых возможностей"""
        opportunities = await parse_artconnect()
        new_opps = [opp for opp in opportunities if opp.url not in self.seen_opportunities]

        for opp in new_opps:
            message = opp.to_telegram_message()
            for user_id in self.subscribers:
                try:
                    await self.bot.send_message(chat_id=user_id, text=message, parse_mode='Markdown')
                except Exception as e:
                    logger.error(f"Ошибка при отправке пользователю {user_id}: {e}")
            self.seen_opportunities.add(opp.url)

        if new_opps:
            self.save_data()

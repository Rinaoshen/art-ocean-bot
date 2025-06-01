import logging
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from .subscribers import load_subscribers, save_subscribers
from .opportunity import Opportunity
from .scraper import parse_example_site, hash_opportunity
import asyncio

logger = logging.getLogger(__name__)

class ArtOceanBot:
    def __init__(self, telegram_token: str):
        self.bot = Bot(token=telegram_token)
        self.application = Application.builder().token(telegram_token).build()
        self.subscribers = load_subscribers()
        self.seen_opportunities = set()

        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("subscribe", self.subscribe_command))
        self.application.add_handler(CommandHandler("unsubscribe", self.unsubscribe_command))
        self.application.add_handler(CommandHandler("status", self.status_command))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        welcome_text = (
            "🎨🌊 **Добро пожаловать в Art Ocean Bot!**\n\n"
            "Я океан возможностей для художников! Автоматически мониторю сайты и нахожу новые возможности:\n"
            "• 💰 Гранты\n• 🏠 Арт-резиденции\n• 📢 Open Call'ы\n• 🏆 Конкурсы\n• 🎨 Выставки\n\n"
            "**Команды:**\n"
            "/subscribe - подписаться на уведомления\n"
            "/unsubscribe - отписаться\n"
            "/status - проверить статус подписки\n"
            "/help - помощь\n\n"
            "🌊 Нажмите /subscribe чтобы погрузиться в океан арт-возможностей!"
        )
        await update.message.reply_text(welcome_text, parse_mode='Markdown')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = (
            "🤖🌊 **Справка по Art Ocean Bot**\n\n"
            "**Что я умею:**\n"
            "• Мониторю 15+ сайтов с арт-возможностями\n"
            "• Отправляю уведомления о новых открытых заявках\n"
            "• Фильтрую дубликаты\n"
            "• Работаю 24/7 как океанские волны\n\n"
            "**Источники:**\n"
            "• ArtConnect, ArtRabbit, ArtForum\n"
            "• e-flux, Artist-Opportunities.org\n"
            "• Крупные галереи (Tate, Gagosian, etc.)\n"
            "• И многие другие\n\n"
            "**Команды:**\n"
            "/start - начать работу\n"
            "/subscribe - подписаться\n"
            "/unsubscribe - отписаться\n"
            "/status - статус подписки\n\n"
            "🌊 Океан возможностей ждет вас!"
        )
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def subscribe_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        self.subscribers.add(user_id)
        save_subscribers(self.subscribers)
        await update.message.reply_text(
            "✅🌊 Вы подписались на Art Ocean Bot!\nТеперь я буду присылать вам все новые арт-возможности из океана творчества.",
            parse_mode='Markdown'
        )

    async def unsubscribe_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        self.subscribers.discard(user_id)
        save_subscribers(self.subscribers)
        await update.message.reply_text(
            "❌ Вы отписались от уведомлений.\nИспользуйте /subscribe чтобы подписаться снова.",
            parse_mode='Markdown'
        )

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        is_subscribed = user_id in self.subscribers
        status = "✅ Подписан" if is_subscribed else "❌ Не подписан"
        total_subscribers = len(self.subscribers)
        await update.message.reply_text(
            f"📊 **Ваш статус:** {status}\n"
            f"👥 **Всего подписчиков:** {total_subscribers}\n"
            f"🔍 **Найдено возможностей:** {len(self.seen_opportunities)}",
            parse_mode='Markdown'
        )

    async def send_new_opportunities(self):
        opportunities = await parse_example_site()
        new_opps = []
        for opp in opportunities:
            opp_hash = hash_opportunity(opp)
            if opp_hash not in self.seen_opportunities:
                self.seen_opportunities.add(opp_hash)
                new_opps.append(opp)

        for opp in new_opps:
            message = opp.to_telegram_message()
            for user_id in self.subscribers:
                try:
                    await self.bot.send_message(chat_id=user_id, text=message, parse_mode='Markdown', disable_web_page_preview=False)
                except Exception as e:
                    logger.error(f"Failed to send message to {user_id}: {e}")

    async def periodic_check(self, interval_seconds=3600):
        while True:
            logger.info("Checking for new opportunities...")
            await self.send_new_opportunities()
            await asyncio.sleep(interval_seconds)

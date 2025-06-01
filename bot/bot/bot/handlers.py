from telegram import Update
from telegram.ext import ContextTypes
from bot.storage import Storage

storage = Storage()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎨 Добро пожаловать в Art Ocean Bot!\n\n"
        "Я бот, который помогает художникам находить:\n"
        "• Гранты 💰\n"
        "• Арт-резиденции 🏠\n"
        "• Open Call'ы 📢\n"
        "• Конкурсы 🏆\n\n"
        "Команды:\n"
        "/subscribe - подписаться\n"
        "/unsubscribe - отписаться\n"
        "/status - статус подписки\n"
        "/help - справка"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛟 Справка:\n\n"
        "/subscribe — подписка на рассылку\n"
        "/unsubscribe — отписка от рассылки\n"
        "/status — проверка подписки\n"
        "/start — приветственное сообщение\n"
        "/help — помощь"
    )

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    storage.subscribers.add(user_id)
    storage.save()
    await update.message.reply_text("✅ Вы подписались на рассылку!")

async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    storage.subscribers.discard(user_id)
    storage.save()
    await update.message.reply_text("❌ Вы отписались от рассылки.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in storage.subscribers:
        text = "✅ Вы подписаны на рассылку."
    else:
        text = "❌ Вы не подписаны."
    await update.message.reply_text(text)

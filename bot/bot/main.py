# bot/main.py

import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler
from bot.handlers import start, help_command, subscribe, unsubscribe, status

TOKEN = "8151684930:AAG8u2Gg3oPmOA7sl5-XamwWt57tMyIcLLI"

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Регистрируем обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe))
    app.add_handler(CommandHandler("status", status))

    print("Бот запущен...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

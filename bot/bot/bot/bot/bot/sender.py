import logging
from telegram import Bot
from bot.models import Opportunity
from bot.subscribers import load_subscribers

logger = logging.getLogger(__name__)

async def send_opportunity(bot: Bot, opportunity: Opportunity):
    message = opportunity.to_telegram_message()
    subscribers = load_subscribers()

    if not subscribers:
        logger.info("Нет подписчиков для рассылки.")
        return

    for user_id in subscribers:
        try:
            await bot.send_message(chat_id=user_id, text=message, parse_mode='Markdown', disable_web_page_preview=True)
            logger.info(f"Отправлено пользователю {user_id}")
        except Exception as e:
            logger.error(f"Ошибка при отправке пользователю {user_id}: {e}")

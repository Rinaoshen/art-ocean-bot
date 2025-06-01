import asyncio
import logging
from bot.utils import fetch_all_opportunities, load_seen_opportunities, save_seen_opportunities
from bot.subscribers import load_subscribers
from bot.formatting import format_opportunity
from telegram import Bot

logger = logging.getLogger(__name__)

async def notify_new_opportunities(bot: Bot):
    logger.info("🔍 Запуск проверки новых возможностей...")
    
    subscribers = load_subscribers()
    seen_ids = load_seen_opportunities()
    new_opportunities = await fetch_all_opportunities()

    fresh = []
    for opp in new_opportunities:
        if opp["id"] not in seen_ids:
            seen_ids.add(opp["id"])
            fresh.append(opp)

    if not fresh:
        logger.info("📭 Новых возможностей не найдено.")
        return

    save_seen_opportunities(seen_ids)
    logger.info(f"📬 Найдено новых возможностей: {len(fresh)}")

    for user_id in subscribers:
        for opp in fresh:
            try:
                msg = format_opportunity(opp)
                await bot.send_message(chat_id=user_id, text=msg, parse_mode="Markdown", disable_web_page_preview=False)
            except Exception as e:
                logger.warning(f"❌ Не удалось отправить сообщение {user_id}: {e}")

from dataclasses import dataclass

@dataclass
class Opportunity:
    title: str
    description: str
    deadline: str
    source: str
    url: str
    category: str  # grant, residency, open_call, competition, exhibition
    location: str = ""
    fee: str = ""

    def to_telegram_message(self) -> str:
        category_emoji = {
            'grant': '💰',
            'residency': '🏠',
            'open_call': '📢',
            'competition': '🏆',
            'exhibition': '🎨'
        }
        emoji = category_emoji.get(self.category, '📋')
        message = f"{emoji} **{self.title}**\n\n"
        message += f"📅 **Дедлайн:** {self.deadline}\n"
        if self.location:
            message += f"🌍 **Локация:** {self.location}\n"
        if self.fee:
            message += f"💵 **Взнос:** {self.fee}\n"
        desc_preview = self.description[:300]
        if len(self.description) > 300:
            desc_preview += "..."
        message += f"📝 **Описание:** {desc_preview}\n\n"
        message += f"🔗 [Подробнее]({self.url})\n"
        message += f"📊 **Источник:** {self.source}"
        return message

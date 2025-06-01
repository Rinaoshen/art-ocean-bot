import aiohttp
from bs4 import BeautifulSoup
from bot.opportunity import Opportunity

async def parse_artconnect() -> list[Opportunity]:
    url = "https://www.artconnect.com/opportunities/opencalls?types=OPEN_CALL"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()

    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.find_all('a', class_='OpportunityCard_link__g2_3o')

    results = []
    for card in cards:
        title_tag = card.find('h2')
        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        link = "https://www.artconnect.com" + card['href']
        deadline_tag = card.find('span', class_='OpportunityCard_deadline__cG3yM')
        deadline = deadline_tag.get_text(strip=True) if deadline_tag else "Не указано"

        results.append(Opportunity(
            title=title,
            description="",
            deadline=deadline,
            source="ArtConnect",
            url=link,
            category="open_call"
        ))

    return results

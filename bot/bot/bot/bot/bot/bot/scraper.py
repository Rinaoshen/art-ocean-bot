import aiohttp
from bs4 import BeautifulSoup
from typing import List
from .opportunity import Opportunity
import hashlib
import logging

logger = logging.getLogger(__name__)

async def fetch_html(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.warning(f"Failed to fetch {url} with status {response.status}")
                    return ""
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return ""

def hash_opportunity(opportunity: Opportunity) -> str:
    unique_str = opportunity.title + opportunity.url
    return hashlib.sha256(unique_str.encode('utf-8')).hexdigest()

async def parse_example_site() -> List[Opportunity]:
    # Пример парсинга гипотетического сайта
    url = "https://example.com/art-opportunities"
    html = await fetch_html(url)
    if not html:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    opportunities = []

    for item in soup.select('.opportunity-item'):
        title = item.select_one('.title').get_text(strip=True)
        description = item.select_one('.description').get_text(strip=True)
        deadline = item.select_one('.deadline').get_text(strip=True)
        link = item.select_one('a')['href']
        source = "Example Site"
        category = "open_call"  # Логика определения категории зависит от сайта
        location = item.select_one('.location').get_text(strip=True) if item.select_one('.location') else ""
        fee = item.select_one('.fee').get_text(strip=True) if item.select_one('.fee') else ""

        opp = Opportunity(
            title=title,
            description=description,
            deadline=deadline,
            source=source,
            url=link,
            category=category,
            location=location,
            fee=fee
        )
        opportunities.append(opp)

    return opportunities

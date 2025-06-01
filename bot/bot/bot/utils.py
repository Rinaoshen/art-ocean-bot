import hashlib
from dataclasses import asdict
from typing import List, Set

from .models import Opportunity


def hash_opportunity(opportunity: Opportunity) -> str:
    """
    Создаёт уникальный хеш для возможности на основе её основных полей.
    """
    data = f"{opportunity.title}|{opportunity.deadline}|{opportunity.url}"
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def filter_new_opportunities(opportunities: List[Opportunity], seen_hashes: Set[str]) -> List[Opportunity]:
    """
    Фильтрует новые возможности, исключая уже известные по хешу.
    """
    return [
        opp for opp in opportunities
        if hash_opportunity(opp) not in seen_hashes
    ]

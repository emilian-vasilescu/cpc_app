import random
import asyncio

import requests as requests

from Models.card import Card
from app import db


class CollectionService:
    COLLECTION_COUNT = 5
    RANDOM_NAME_API = 'https://random-data-api.com/api/v2/users'
    RANDOM_SKILL_LEVEL_API = 'https://www.random.org/integers/?num=1&min=10&max=100&col=1&base=10&format=plain'
    loop = asyncio.get_event_loop()

    def __init__(self, user):
        self.user = user

    def generate_collection(self):
        self.loop.run_until_complete(self.create_cards())

    async def create_cards(self):
        for i in range(self.COLLECTION_COUNT):
            name = await self.get_name()
            skill_level = await self.get_skill_level()
            card = Card(
                name=name,
                age=random.randint(18, 40),
                skill_level=skill_level,
                market_value=Card.INITIAL_MARKET_VALUE
            )
            self.user.cards.append(card)
            db.session.commit()

    async def get_name(self):
        response = await self.loop.run_in_executor(None, requests.get, self.RANDOM_NAME_API)
        if response.ok:
            data = response.json()
            return data['first_name'] + ' ' + data['last_name']
        else:
            return 'Baseball Player'

    async def get_skill_level(self):
        response = await self.loop.run_in_executor(None, requests.get, self.RANDOM_SKILL_LEVEL_API)
        if response.ok:
            skill_level = int(response.text.strip())
        else:
            skill_level = random.randint(10, 70)
        return skill_level

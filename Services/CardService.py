from Models.Card import Card


class CardService:
    _card = None
    _data = None

    def create_card(self):

        skill_level, name, market_value, age = self.data.get('skill_level'), self.data.get('name'), self.data.get(
            'market_value'), self.data.get('age')

        if not all([skill_level, name, market_value, age]):
            raise Exception('At least one of skill_level, name, market_value or age is mandatory.')

        self.card = Card(
            skill_level=skill_level,
            name=name,
            market_value=market_value,
            age=age
        )

    def update_card(self):
        if not self.card:
            raise Exception('Card does not exist')

        skill_level, name, market_value, age = self.data.get('skill_level'), self.data.get('name'), self.data.get(
            'market_value'), self.data.get('age')

        if not any([skill_level, name, market_value, age]):
            return {'message': 'At least one of skill_level, name, market_value or age is mandatory.'}, 400

        # @todo Validate data
        if skill_level:
            self.card.skill_level = skill_level
        if name:
            self.card.name = name
        if market_value:
            self.card.market_value = market_value
        if age:
            self.card.age = age

    @property
    def card(self):
        return self._card

    @card.setter
    def card(self, card):
        self._card = card

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

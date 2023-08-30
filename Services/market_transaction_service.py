from datetime import datetime

from Exceptions.exceptions import ValidationFieldsException, AccessDeniedException, NotFoundException
from MachineLearning.machine_learning import CardMarketValueGenerator
from Models.card import Card
from Models.market_transaction import MarketTransaction
from Models.user import User


class MarketTransactionService:
    _user = None
    _card = None
    _data = None
    _transaction = None

    def create_transaction(self, current_user):
        card_id, seller_id, asked_value = self.data.get('card_id'), self.data.get('seller_id'), self.data.get(
            'asked_value')

        if not all([card_id, seller_id, asked_value]):
            raise ValidationFieldsException('card_id, seller_id and asked_value are mandatory.')

        if current_user.role != User.ADMIN and current_user.id != seller_id:
            raise AccessDeniedException('Only admins can add other user cards on market')

        self.user = User.query \
            .filter_by(id=seller_id) \
            .first()

        self.card = Card.query \
            .filter_by(id=card_id) \
            .first()

        self.transaction = MarketTransaction.query \
            .filter_by(card_id=card_id, seller_id=seller_id, status=MarketTransaction.ON_SELL) \
            .first()

        if self.transaction:
            raise ValidationFieldsException('This card is already posted on market by this user!')

        if not self.user:
            raise NotFoundException('User does not exist!')

        if not self.card:
            raise NotFoundException('Card does not exist!')

        if not any([c.id == self.card.id for c in self.user.cards]):
            raise NotFoundException('User does not have the card!')

        self.transaction = MarketTransaction(
            asked_value=asked_value,
            market_value=self.card.market_value,
            seller_id=self.user.id,
            card_id=self.card.id
        )

    def edit_transaction(self, current_user):
        buyer_id = self.data.get('buyer_id')

        if not buyer_id:
            raise ValidationFieldsException('buyer_id is mandatory.')

        if current_user.role != User.ADMIN and current_user.id != buyer_id:
            raise AccessDeniedException('Only admins do purchases in the name of other users')

        self.user = User.query \
            .filter_by(id=buyer_id) \
            .first()

        if not self.transaction:
            raise NotFoundException('This transaction does not exists on market')

        if self.transaction.status != MarketTransaction.ON_SELL:
            raise ValidationFieldsException('This transaction is not on sell on market')

        if not self.user:
            raise NotFoundException('Buyer does not exist!')

        if self.user.budget < self.transaction.asked_value:
            raise ValidationFieldsException('User does not have enough money!')

        self.card = Card.query \
            .filter_by(id=self.transaction.card_id) \
            .first()

        if not self.card:
            raise NotFoundException('Card does not exist!')

        if any([c.id == self.card.id for c in self.user.cards]):
            raise ValidationFieldsException('User already have this card!')

        seller = User.query \
            .filter_by(id=self.transaction.seller_id) \
            .first()

        if not seller:
            raise NotFoundException('Seller does not exist!')

        self.transaction.buyer_id = self.user.id
        self.transaction.status = MarketTransaction.SOLD
        self.transaction.modified_at = datetime.now()

        self.user.budget = self.user.budget - self.transaction.asked_value
        seller.budget = seller.budget + self.transaction.asked_value

        self.user.cards.append(self.card)
        seller.cards.remove(self.card)

        generator = CardMarketValueGenerator()
        previous_transactions = MarketTransaction.query.filter_by(card_id=self.card.id,
                                                                  status=MarketTransaction.SOLD).count()
        self.card.market_value = generator.predict(self.card.age, self.card.skill_level, previous_transactions)

    def delete_transaction(self, current_user):

        if not self.transaction:
            raise NotFoundException('This transaction does not exists on market')

        if current_user.role != User.ADMIN and current_user.id != self.transaction.seller_id:
            raise AccessDeniedException('Only admins can cancel other market transactions')

        if self.transaction.status != MarketTransaction.ON_SELL:
            raise ValidationFieldsException('Only on sell transactions can be canceled')

        self.transaction.status = MarketTransaction.CANCELED

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def transaction(self):
        return self._transaction

    @transaction.setter
    def transaction(self, transaction):
        self._transaction = transaction

    @property
    def card(self):
        return self._card

    @card.setter
    def card(self, card):
        self._card = card

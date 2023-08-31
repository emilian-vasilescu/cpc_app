import random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sqlalchemy import select
from Models.market_transaction_train import MarketTransactionTrain
from app import db, app
import joblib


class CardMarketValueGenerator:
    model = None
    card_data = None
    model_file_name = "card_market_value_model.joblib"

    def __init__(self):
        self.get_cards_data()
        self.init_model()

    def init_model(self):
        try:
            self.model = joblib.load(self.model_file_name)
        except Exception as e:
            self.generate_model()

    def predict(self, age, skill_level, previous_transactions):
        prediction = self.model.predict([[age, skill_level, previous_transactions]])
        return prediction[0]

    def save_model(self):
        if self.model is not None:
            joblib.dump(self.model, self.model_file_name)

    def generate_model(self):
        self.model = linear_model.LinearRegression()
        # X is the input_data
        input_data = self.card_data.drop(columns=["market_value"])
        # Y is the output_data or the predicted data
        output_data = self.card_data["market_value"]

        input_data_train, input_data_test, output_data_train, output_data_test = train_test_split(input_data.values,
                                                                                                  output_data.values,
                                                                                                  test_size=0.2)
        self.model.fit(input_data_train, output_data_train)
        predictions = self.model.predict(input_data_test)

        score = self.model.score(input_data_test, output_data_test)

        if score > 0.75:
            self.save_model()
        else:
            self.generate_model()

    def get_cards_data(self):
        try:
            if MarketTransactionTrain.query.count() == 0:
                self.generate_train_data()
        except Exception as e:
            print(str(e))
            self.generate_train_data()

        statement = select(MarketTransactionTrain.market_value, MarketTransactionTrain.age,
                           MarketTransactionTrain.skill_level, MarketTransactionTrain.previous_transactions)
        connection = db.engine.connect()
        self.card_data = pd.read_sql_query(statement, connection)
        connection.close()
        return self.card_data

    def adjust_market_value_to_transaction_count(self, market_value, previous_transactions):
        if previous_transactions == 0:
            return market_value
        elif previous_transactions == 1:
            return market_value * random.randint(102, 115) / 100
        else:
            return market_value * random.randint(110, 122) / 100

    def generate_train_data(self):
        # init train table
        try:
            MarketTransactionTrain.__table__.drop(db.engine)
        except Exception as e:
            print(str(e))

        db.create_all()

        for i in range(100):
            age = random.randint(18, 40)
            skill_level = random.randint(10, 100)
            previous_transactions = random.randint(0, 2)

            if age < 30 and skill_level > 80:
                market_value = random.randint(450, 1000)
                asked_value = round(market_value * random.randint(122, 160) / 100)
            elif age < 30 and skill_level > 60 or age > 30 and skill_level > 80:
                market_value = random.randint(300, 600)
                asked_value = round(market_value * random.randint(120, 150) / 100)
            elif age < 30 and skill_level > 40 or age > 30 and skill_level > 60:
                market_value = random.randint(225, 400)
                asked_value = round(market_value * random.randint(118, 140) / 100)
            elif age < 30 and skill_level > 20 or age > 30 and skill_level > 40:
                market_value = random.randint(150, 250)
                asked_value = round(market_value * random.randint(115, 130) / 100)
            else:
                market_value = random.randint(100, 200)
                asked_value = round(market_value * random.randint(105, 125) / 100)

            market_value = round(self.adjust_market_value_to_transaction_count(market_value, previous_transactions))
            transaction = MarketTransactionTrain(
                asked_value=asked_value,
                market_value=market_value,
                age=age,
                skill_level=skill_level,
                previous_transactions=previous_transactions
            )
            db.session.add(transaction)
            db.session.commit()


with app.app_context():
    generator = CardMarketValueGenerator()
    # generator.generate_train_data()
    # generator.init_model()

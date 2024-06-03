from datetime import datetime
from . import db
import random
from sqlalchemy.exc import IntegrityError


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.BigInteger)
    username = db.Column(db.String)
    name = db.Column(db.String)
    phone = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    wallets = db.relationship('Wallet', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'


class Currency(db.Model):
    __tablename__ = 'currency'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    code = db.Column(db.String)
    symbol = db.Column(db.String)

    wallets = db.relationship('Wallet', backref='basic_currency', lazy=True)
    incomes = db.relationship('Income', backref='currency', lazy=True)
    expenses = db.relationship('Expense', backref='currency', lazy=True)
    transactions = db.relationship('Transaction', backref='currency', lazy=True)

    def __repr__(self):
        return f'<Currency {self.code}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'symbol': self.symbol
        }


class Wallet(db.Model):
    __tablename__ = 'wallet'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    basic_currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
    amount = db.Column(db.Float)
    number = db.Column(db.Integer, unique=True)  # Corrected the field name to match the column definition

    incomes = db.relationship('Income', backref='wallet', lazy=True)
    expenses = db.relationship('Expense', backref='wallet', lazy=True)
    transactions_from = db.relationship('Transaction', foreign_keys='Transaction.wallet_from_id', backref='wallet_from', lazy=True)
    transactions_to = db.relationship('Transaction', foreign_keys='Transaction.wallet_to_id', backref='wallet_to', lazy=True)

    def __repr__(self):
        return f'<Wallet {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'user_id': self.user_id,
            'basic_currency_id': self.basic_currency_id,
            'number': self.number,
            'amount': self.amount
        }


@db.event.listens_for(Wallet, 'before_insert')
def generate_six_digit_number(mapper, connection, target):
    if not target.number:  # Corrected to match the field name
        while True:
            target.number = random.randint(100000, 999999)
            existing_wallet = Wallet.query.filter_by(number=target.number).first()  # Corrected to match the field name
            if existing_wallet is None:
                break


class Income(db.Model):
    __tablename__ = 'incomes'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    amount = db.Column(db.Float)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'))

    def __repr__(self):
        return f'<Income {self.amount}>'


class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    amount = db.Column(db.Float)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'))

    def __repr__(self):
        return f'<Expense {self.amount}>'


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    amount = db.Column(db.Float)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
    wallet_from_id = db.Column(db.Integer, db.ForeignKey('wallet.id'))
    wallet_to_id = db.Column(db.Integer, db.ForeignKey('wallet.id'))

    def __repr__(self):
        return f'<Transaction {self.amount}>'


def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

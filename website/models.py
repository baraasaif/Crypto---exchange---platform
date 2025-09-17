from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

class User(db.Model, UserMixin):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150),unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    wallet = db.relationship('Wallet', backref='user', uselist=False)

class Wallet(db.Model):
    #__tablename__ = 'wallets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    public_key = db.Column(db.String(128), unique=True, nullable=False)
    private_key = db.Column(db.String(128), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    sent_transactions = db.relationship('Transaction', foreign_keys='Transaction.sender_wallet_id', backref='sender_wallet', lazy=True)
    received_transactions = db.relationship('Transaction', foreign_keys='Transaction.receiver_wallet_id', backref='receiver_wallet', lazy=True)

class Transaction(db.Model):
    #__tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    sender_wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'), nullable=False)
    receiver_wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime(timezone = True), default=func.now())
    transaction_hash = db.Column(db.String(128), unique=True, nullable=False)
    block = db.relationship('Block', backref='transaction', uselist=False)

class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    block_number = db.Column(db.Integer, nullable=False, unique=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    previous_hash = db.Column(db.String(128), nullable=False)
    current_hash = db.Column(db.String(128), nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    proof = db.Column(db.Integer, nullable=False)
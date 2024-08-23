from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Chore(db.Model):
    __tablename__ = 'chores'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_completed = db.Column(db.Date)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    chore_id = db.Column(db.Integer, db.ForeignKey('chores.id', ondelete='CASCADE'))
    date = db.Column(db.Date, default=date.today, nullable=False)
    description = db.Column(db.String, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'spending'

    chore = db.relationship('Chore', backref=db.backref('transactions', cascade='all, delete'))
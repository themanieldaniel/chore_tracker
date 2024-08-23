from flask import Blueprint, request, jsonify
from models import db, Chore, Transaction
from datetime import date

chores_bp = Blueprint('chores', __name__, url_prefix='/chores')
transactions_bp = Blueprint('transactions', __name__, url_prefix='/transactions')

# Routes for Chores
@chores_bp.route('/', methods=['GET'])
def get_chores():
    chores = Chore.query.all()
    return jsonify([chore_to_dict(chore) for chore in chores])

@chores_bp.route('/', methods=['POST'])
def create_chore():
    data = request.json
    new_chore = Chore(description=data['description'], amount=data['amount'])
    db.session.add(new_chore)
    db.session.commit()
    return jsonify(chore_to_dict(new_chore)), 201

@chores_bp.route('/<int:chore_id>', methods=['PUT'])
def update_chore(chore_id):
    chore = Chore.query.get_or_404(chore_id)
    data = request.json
    chore.description = data.get('description', chore.description)
    chore.amount = data.get('amount', chore.amount)
    db.session.commit()
    return jsonify(chore_to_dict(chore))

@chores_bp.route('/<int:chore_id>', methods=['DELETE'])
def delete_chore(chore_id):
    chore = Chore.query.get_or_404(chore_id)
    db.session.delete(chore)
    db.session.commit()
    return '', 204

# Routes for Transactions
@transactions_bp.route('/', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([transaction_to_dict(transaction) for transaction in transactions])

@transactions_bp.route('/', methods=['POST'])
def create_transaction():
    data = request.json
    new_transaction = Transaction(
        chore_id=data.get('chore_id'),
        description=data.get('description'),
        amount=data.get('amount'),
        type=data.get('type')
    )
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify(transaction_to_dict(new_transaction)), 201

@transactions_bp.route('/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    data = request.json
    transaction.description = data.get('description', transaction.description)
    transaction.amount = data.get('amount', transaction.amount)
    transaction.type = data.get('type', transaction.type)
    db.session.commit()
    return jsonify(transaction_to_dict(transaction))

@transactions_bp.route('/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    db.session.delete(transaction)
    db.session.commit()
    return '', 204

# Helper functions to convert model instances to dict
def chore_to_dict(chore):
    return {
        'id': chore.id,
        'description': chore.description,
        'amount': str(chore.amount),
        'completed': chore.completed,
        'date_completed': chore.date_completed
    }

def transaction_to_dict(transaction):
    return {
        'id': transaction.id,
        'chore_id': transaction.chore_id,
        'date': str(transaction.date),
        'description': transaction.description,
        'amount': str(transaction.amount),
        'type': transaction.type
    }
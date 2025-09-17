import hashlib
import os
from .models import Wallet

def create_wallet(user):
    private_key = os.urandom(32).hex()
    public_key = hashlib.sha256(private_key.encode()).hexdigest()
    return Wallet(user=user, public_key=public_key, private_key=private_key, balance=10000)

def generate_transaction_hash():
    return hashlib.sha256(os.urandom(32)).hexdigest()

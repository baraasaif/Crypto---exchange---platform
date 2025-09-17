import hashlib
import json
from time import time
from uuid import uuid4
from sqlalchemy import func
from .models import Block
from . import db

def calculate_hash(block_number, transaction, previous_hash, timestamp,proof):
    """
    حساب الـ hash الخاص بالكتلة بناءً على بياناتها.
    """
    Challenge = "0000"
    print(transaction['sender'])
    data = f"{block_number}{transaction['sender']}{transaction['sender_public_key']}{transaction['receiver_public_key']}{transaction['amount']}{previous_hash}{timestamp}{proof}"
    hash_value = hashlib.sha256(data.encode()).hexdigest()
    while  hash_value[:len(Challenge)] != Challenge:
        proof += 1
        data = f"{block_number}{transaction['sender']}{transaction['sender_public_key']}{transaction['receiver_public_key']}{transaction['amount']}{previous_hash}{timestamp}{proof}"
        hash_value = hashlib.sha256(data.encode()).hexdigest()
    return hash_value, proof

def create_block(transaction):
    """
    إنشاء كتلة جديدة وربطها بمعاملة.
    """
    # الحصول على رقم الكتلة التالي
    last_block = Block.query.order_by(Block.block_number.desc()).first()
       # الحصول على الطابع الزمني الحالي
    timestamp = func.now()
    block_number = last_block.block_number + 1 if last_block else 1
    
    if block_number == 1:
        previous_hash,proof = calculate_hash(0, transaction, "101", func.now(),0)
    else:
        previous_hash = last_block.current_hash
    current_hash,proof = calculate_hash(block_number, transaction, previous_hash, func.now(),0)

 
    # حساب الـ hash الحالي
    # current_hash,proof = calculate_hash(block_number, transaction, previous_hash, timestamp,0)

    # إنشاء الكتلة
    new_block = {
            'block_number': block_number,
            'sender': transaction['sender'],
            'sender_public_key': transaction['sender_public_key'],
            'receiver_public_key': transaction['receiver_public_key'],
            'amount': transaction['amount'],
            'previous_hash': previous_hash,
            'current_hash': current_hash,
            'timestamp': func.now(),
            'proof': proof 
        }
        # إرجاع الكتلة الجديدة
    return new_block

def is_chain_valid():
    """
    التحقق من صحة سلسلة الكتل:
    - التأكد من أن hash الكتل متسلسل بشكل صحيح.
    - التأكد من أن الكتل مرتبة حسب block_number.
    """
    # جلب جميع الكتل مرتبة حسب block_number
    blocks = Block.query.order_by(Block.block_number).all()

    # إذا كانت السلسلة تحتوي على أقل من كتلتين، فهي صالحة تلقائيًا
    if len(blocks) < 2:
        return True

    for i in range(1, len(blocks)):
        current_block = blocks[i]
        previous_block = blocks[i - 1]

        # 1. التحقق من أن رقم الكتلة الحالي أكبر بمقدار 1 من الكتلة السابقة
        if current_block.block_number != previous_block.block_number + 1:
            print(f"خطأ: الكتلة رقم {current_block.block_number} غير مرتبة بشكل صحيح.")
            return False

        # 2. التحقق من أن الـ hash السابق يطابق الـ hash الخاص بالكتلة السابقة
        if current_block.previous_hash != previous_block.current_hash:
            print(f"خطأ: hash السابق للكتلة رقم {current_block.block_number} لا يطابق hash الكتلة السابقة.")
            return False

        # 3. التحقق من صحة الـ hash الحالي للكتلة
        recalculated_hash = calculate_hash(
            current_block.block_number,
            current_block.sender,
            current_block.sender_public_key,
            current_block.receiver_public_key,
            current_block.amount,
            current_block.previous_hash,
            current_block.timestamp,
            current_block.proof
        )
        if current_block.current_hash != recalculated_hash:
            print(f"خطأ: hash الكتلة رقم {current_block.block_number} غير صالح.")
            return False

    # إذا اجتازت السلسلة جميع الاختبارات، فهي صالحة
    return True
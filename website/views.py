from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Wallet, User, Transaction, Block
from .wallet import generate_transaction_hash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .blockchain import create_block, is_chain_valid

views = Blueprint('views',__name__)

@views.route('/',methods=['GET','POST'])
#@login_required
def index():
    ## Blockchain Home
    transactions = Transaction.query.filter_by(sender_wallet_id=current_user.wallet.id).all()
    blocks = Block.query.filter_by().all()
    return render_template('index.html',user=current_user,blocks=blocks)

@views.route('/users_pk',methods=['GET','POST'])
#@login_required
def users_pk():
    ## Blockchain Home
    users = User.query.all()
    return render_template('users_pk.html',users=users)

@views.route('/user_info')
def user_info():
    transactions = Transaction.query.filter_by(sender_wallet_id=current_user.wallet.id).all()
    return render_template('user_info.html',user=current_user,transactions=transactions)


@views.route('/transaction', methods=['GET', 'POST'])
def create_transaction():
    if request.method == 'POST':
        sender_wallet = current_user.wallet  # مثال: إرسال من أول محفظة فقط
        receiver_public_key = request.form['receiver_public_key']
        amount = float(request.form['amount'])
        # تحقق من وجود المحفظة المستقبلة عبر المفتاح العام
        receiver_wallet = Wallet.query.filter_by(public_key=receiver_public_key).first()
        
        if not receiver_wallet or sender_wallet.balance < amount:
            flash('فشلت المناقلة', 'danger')
            return redirect(url_for('create_transaction'))

        Trans = {
            'sender': current_user.username,
            'sender_public_key': sender_wallet.public_key,
            'receiver_public_key': receiver_public_key,
            'amount': amount,
        }
        validity =True # is_chain_valid()
        if validity:
            new_block = create_block(Trans)
            print(new_block)
            # إنشاء المعاملة
            transaction = Transaction(
                sender_wallet_id=sender_wallet.id,
                receiver_wallet_id=receiver_wallet.id,
                amount=amount,
                transaction_hash = generate_transaction_hash()
            )
            db.session.add(transaction)
            db.session.commit()
            sender_wallet.balance -= amount
            receiver_wallet.balance += amount
            #  إدخال الكتلة
            block = Block(block_number=new_block['block_number'],
                transaction_id=transaction.id,
                previous_hash=new_block['previous_hash'],
                current_hash=new_block['current_hash'],
                timestamp = transaction.timestamp,
                proof = new_block['proof']
                )
            db.session.add(block)
            db.session.commit()


            flash('تمت المناقلة بنجاح', 'success')
            return redirect(url_for('views.index'))
        else:
            flash('سلسلة الكتل غير صحيحة ', 'danger')
            return redirect(url_for('create_transaction'))
     
    return render_template('transaction.html', user=current_user)


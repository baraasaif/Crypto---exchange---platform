from flask import Blueprint, render_template, request, flash,redirect,url_for
from .models import Wallet, User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .wallet import create_wallet
import hashlib
auth = Blueprint('auth',__name__)

@auth.route('/new_wallet',methods=['GET','POST'])
def new_wallet():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        pHash = hashlib.sha256(password.encode()).hexdigest()
        generate_password_hash(password,method='pbkdf2:sha256')
        email = request.form.get('email')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            print(password)
            print(pHash)
            if user.password_hash == pHash:
                login_user(user, remember=True)
                return redirect(url_for('views.user_info'))
            else:
                print(user.password_hash)
                flash('المستخدم موجود مسبقاً، كلمة سر خاطئة', category='error')
        elif len(password) < 7:
            flash('كلمة السر يجب أن تكون مكونة على الأقل من 7 محارف', category='error')
        else:
            new_user = User(email=email, username=username, password_hash=hashlib.sha256(password.encode()).hexdigest())
            db.session.add(new_user)
            db.session.commit()
            new_w = create_wallet(new_user)
            db.session.add(new_w)
            db.session.commit()
            print("sssssssss")
            logout_user()
            print("sssssssss")
            login_user(new_user, remember=True)
            flash('تم إنشاء المحفظة بنجاح', category='success')
            return redirect(url_for('views.user_info'))
    return render_template("new_wallet.html",user=current_user)
        
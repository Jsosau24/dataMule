from flask import Blueprint, request, redirect, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return redirect(url_for('auth.login'))

    login_user(user)

    if user.type == "Admin":
        return redirect(url_for('admin.home'))
    elif user.type == "Peak":
        return redirect(url_for('peak.home'))
    elif user.type == "Coach":
        return redirect(url_for('coach.home'))
    elif user.type == "Athlete":
        return redirect(url_for('athlete.home'))

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

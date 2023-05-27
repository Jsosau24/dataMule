from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash

from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        colby_id = request.form.get('colby_id')
        password = request.form.get('password')

        user = User.query.filter_by(colby_id=colby_id).first()
        print(user.type)

        if not user or not check_password_hash(user.password, password):
            return render_template("login.html", user=current_user)

        login_user(user, remember = True)

        if user.type == "admin":
            return render_template('signup.html', user=user)
        elif user.type == "peak":
            return render_template('signup.html', user=user)
        elif user.type == "coach":
            return render_template('signup.html', user=user)
        elif user.type == "athlete":
            return render_template('athlete_view.html', user=user)
    
    return render_template('login.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

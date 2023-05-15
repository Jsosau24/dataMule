from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import User
from flask_login import login_required, current_user, login_user, logout_user
import re
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

# logs in user if user exists, username and password are correct
@auth.route('/login', methods = ['GET', 'POST'])
def login():

    if request.method == 'POST':
        colby_id = request.form.get('colby_id')
        password = request.form.get('password')
        user = User.query.filter_by(colby_id = colby_id).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember = True)
                return render_template("athlete_view.html", user=current_user)
            else:
                flash("Password is incorrect")
        else:
            flash("User does not exist")
    
    return render_template("sign_in.html", user=current_user, active_page='login')

#logs out the user and returns to login page
@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))




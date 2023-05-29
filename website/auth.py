from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash

from .models import User, Team, Coach, Admin

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        colby_id = request.form.get('colby_id')
        password = request.form.get('password')

        user = User.query.filter_by(colby_id=colby_id).first()

        if not user or not check_password_hash(user.password, password):
            return render_template("login.html", user=current_user)

        login_user(user, remember = True)

        if user.type == "admin":
            # Ensure the current user is an admin
            if current_user.type != "admin":
                return "<h1>NO ACCESS</h1>"

            # Query all athletes and teams
            athletes = User.query.filter_by(type='athlete').all()
            teams = Team.query.all()

            return render_template('admin_dashboard.html', athletes=athletes, teams=teams, user=user)
        
        elif user.type == "peak":
            return render_template('signup.html', user=user)
        
        elif user.type == "coach":

            coach = Coach.query.filter_by(colby_id=current_user.colby_id).first()
            team  = coach.teams[0]
            athletes = team.athletes

            if not team:
                return "<h1>There are no teams</h1>"
        
            return render_template('team_dashboard.html', user=user,team=team, athletes=athletes)
        
        elif user.type == "athlete":
            return render_template('athlete_view.html', user=user)
    
    return render_template('login.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

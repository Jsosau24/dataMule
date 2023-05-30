from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash

from .models import User, Team, Coach, Admin, Peak

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        colby_id = request.form.get('colby_id')
        password = request.form.get('password')

        user = User.query.filter_by(colby_id=colby_id).first()

        if not user or not check_password_hash(user.password, password):
            return render_template("login.html", user=current_user, athlete=current_user)

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
            peak = Peak.query.filter_by(colby_id=current_user.colby_id).first()
            team_association = next((association for association in peak.team_associations if association.role == 'peak'), None)
            
            if team_association is not None:
                team = team_association.team
                athletes = [association.user for association in team.team_associations if association.role == 'athlete']
            else:
                return "<h1>There are no teams</h1>"
        
            return render_template('team_dashboard.html', user=user,team=team, athletes=athletes)
        
        elif user.type == "coach":

            coach = Coach.query.filter_by(colby_id=current_user.colby_id).first()
            team_association = next((association for association in coach.team_associations if association.role == 'coach'), None)
            
            if team_association is not None:
                team = team_association.team
                athletes = [association.user for association in team.team_associations if association.role == 'athlete']
            else:
                return "<h1>There are no teams</h1>"
        
            return render_template('team_dashboard.html', user=user,team=team, athletes=athletes)
        
        elif user.type == "athlete":
            visible_notes = [note for note in current_user.received_notes if note.visible]

            return render_template('athlete_dashboard.html', athlete=current_user, user=current_user, notes=visible_notes)
    
    return render_template('login.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Coach, Team, Athlete, User

routes = Blueprint('main', __name__)

# athlete view
@routes.route('/athlete')
@login_required
def athlete():
    if current_user.type != "athlete":
        return "<h1>NO ACCESS</h1>"
    
    #add code to use data to create the graphs

    return render_template('athlete_view.html', user=current_user)

# coach/staff view
@routes.route('/team/<int:id>', methods = ['GET', 'POST'])
@login_required
def team(id):

    if current_user.type == "athlete":
        return "<h1>NO ACCESS</h1>"
    
    team = Team.query.get(id)
    if team is None:
        return "<h1>NO TEAM</h1>"
    athletes = team.athletes  

    return render_template('team_dashboard.html', team=team, athletes=athletes, user=current_user)

# admin view
@routes.route('/admin-dashboard')
@login_required
def admin_dashboard():

    # Ensure the current user is an admin
    if current_user.type != "admin":
        return "<h1>NO ACCESS</h1>"

    # Query all athletes and teams
    athletes = User.query.filter_by(type='athlete').all()
    teams = Team.query.all()

    return render_template('admin_dashboard.html', athletes=athletes, teams=teams, user=current_user)

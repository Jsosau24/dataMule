from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Coach, Team, Athlete

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

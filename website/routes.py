from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from .models import Peak, Team, Athlete, User, Note, Coach, TeamUserAssociation
from . import db

routes = Blueprint('main', __name__)

# home route
@routes.route('/')
@login_required
def home():

    user = current_user

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

# athlete view
@routes.route('/athlete')
@login_required
def athlete():
    if current_user.type != "athlete":
        return "<h1>NO ACCESS</h1>"
    
    visible_notes = [note for note in current_user.received_notes if note.visible]

    return render_template('athlete_dashboard.html', athlete=current_user, user=current_user, notes=visible_notes)

# coach/staff view
@routes.route('/team/<int:id>', methods = ['GET', 'POST'])
@login_required
def team(id):

    if current_user.type == "athlete":
        return "<h1>NO ACCESS</h1>"
    
    team = Team.query.get(id)

    # Use the association table to get the athletes in the team
    athletes = [association.user for association in team.team_associations if association.role == 'athlete']

    return render_template('team_dashboard.html', team=team, athletes=athletes, user=current_user)

#route for athlete dashboard for coaches, peak and admin
@routes.route('/athlete/<int:id>', methods = ['GET', 'POST'])
@login_required
def athlete_coach(id):

    if current_user.type == "athlete":
        return "<h1>NO ACCESS</h1>"
    
    athlete = Athlete.query.get(id)

    return render_template('athlete_dashboard.html', athlete=athlete, user=current_user)

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

# create note website 
@routes.route('/note/new', methods=['GET', 'POST'])
@login_required
def new_note():

    if request.method == 'GET':
        print(current_user.type)
        if current_user.type == "peak":

            peak = Peak.query.filter_by(colby_id=current_user.colby_id).first()
            athletes = []
            for team_association in peak.team_associations:
                if team_association.role == 'peak':
                    team = team_association.team
                    athletes.extend([association.user for association in team.team_associations if association.role == 'athlete'])

            # removing duplicates
            athletes = list(set(athletes))

            # sort athletes by last name
            athletes.sort(key=lambda athlete: athlete.last_name)

            return render_template('create_notes-dashboard.html', athletes=athletes, user=current_user)

        elif current_user.type == "admin":

            athletes = User.query.filter_by(type='athlete').all()
            return render_template('create_notes-dashboard.html', athletes=athletes, user=current_user)

    if request.method == 'POST':
        athlete_id = request.form.get('athlete')
        note_text = request.form.get('note')
        status = request.form.get('status')

        # Find the athlete and user (creator)
        athlete = Athlete.query.get(athlete_id)
        user = User.query.get(current_user.id)

        if athlete and user:
            # Create a new Note
            note = Note(text=note_text, 
                        visible=True, 
                        creator=user, 
                        receiver=athlete)
            
            # Change the athlete's status
            athlete.status = status
            
            # add the note to the database
            db.session.add(note)
            db.session.commit()

            # Redirect to wherever you want to go after successfully submitting the note
            if current_user.type == "peak":
                return redirect(url_for('main.home'))



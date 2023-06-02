"""
Jonathan Sosa 
routes.py
may-jun 2023
"""

# routes on the file (you can look these up and it will take you there)
## home --> redirects each user to their homepage
## athlete --> athlete view or athlete main page
## team --> team dasboard everyone but athelte has access
## athlete_coach --> view of an athelte from any other user but athlete
## admin_dashboard --> main view for an admin
## team_edit_dashboard --> dashboard with all the teams where you can select one to edit it
## update_position --> edit the position of an athlete from the team dashboard
## user_edit_dashboard --> dashboard with all the users where you can chose one to edit it
## user_edit --> handles the edits on any user
## team_edit --> page where you can choose users on a team
## update_team --> backend for updating the team
## new_note --> creates a new note
## notes_dashboard --> dasboard with all the notes created by the user
## update_note_visibility --> handles the backend to change the visibility of a note
## new_user --> route to create a new user
## new_user_csv --> creates a number of users using an CSV file
## remove_user --> removes a user form the db

# Imports
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from .models import Peak, Team, Athlete, User, Note, Coach, TeamUserAssociation
from . import db
from website.helper_functions import create_user, create_user_csv
import pandas as pd

#Flask blueprint
routes = Blueprint('main', __name__)

#routes
@routes.route('/')
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


@routes.route('/athlete')
@login_required
def athlete():
    if current_user.type != "athlete":
        return "<h1>NO ACCESS</h1>"
    
    visible_notes = [note for note in current_user.received_notes if note.visible]

    return render_template('athlete_dashboard.html', athlete=current_user, user=current_user, notes=visible_notes)

@routes.route('/team/<int:id>', methods = ['GET', 'POST'])
@login_required
def team(id):

    if current_user.type == "athlete":
        return "<h1>NO ACCESS</h1>"
    
    team = Team.query.get(id)

    # Use the association table to get the athletes in the team
    athletes = [association.user for association in team.team_associations if association.role == 'athlete']

    return render_template('team_dashboard.html', team=team, athletes=athletes, user=current_user)

@routes.route('/athlete/<int:id>', methods = ['GET', 'POST'])
@login_required
def athlete_coach(id):

    if current_user.type == "athlete":
        return "<h1>NO ACCESS</h1>"
    
    athlete = Athlete.query.get(id)

    return render_template('athlete_dashboard.html', athlete=athlete, user=current_user)

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

@routes.route('/team/edit/dashboard')
@login_required
def team_edit_dashboard():

    # Ensure the current user is an admin
    if current_user.type != "admin":
        return "<h1>NO ACCESS</h1>"

    # Query all teams
    teams = Team.query.all()

    return render_template('team_edit_dashboard.html', teams=teams, user=current_user)

@routes.route('/update_position/<int:athlete_id>', methods=['POST'])
@login_required
def update_position(athlete_id):
    athlete = Athlete.query.get(athlete_id)
    if not athlete:
        return jsonify(success=False)

    position = request.json.get('position')

    # Update the athlete's position
    athlete.position = position
    db.session.commit()

    return jsonify(success=True)

@routes.route('/user/edit/dashboard')
@login_required
def user_edit_dashboard():

    # Ensure the current user is an admin
    if current_user.type != "admin":
        return "<h1>NO ACCESS</h1>"

    # Query all users
    users = User.query.all()

    return render_template('user_edit_dashboard.html', users=users, user=current_user)

@routes.route('/user/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def user_edit(id):

    # Ensure the current user is an admin
    if current_user.type != "admin":
        return "<h1>NO ACCESS</h1>"

    # Query all users
    edited_user = User.query.get(id)

    if request.method == 'POST':

        #checks if the admin wants to change the type of user
        if edited_user.type != request.form.get('type'):

            from .models import Admin, Peak, Coach, Athlete

            if request.form.get('type') == "admin":
                u = Admin(colby_id = edited_user.colby_id,
                    first_name = request.form.get('first_name'),
                    last_name = request.form.get('last_name'),
                    password = edited_user.password,
                    email = request.form.get('email')
                    )
                db.session.delete(edited_user)
                db.session.add(u)
                db.session.commit()

            elif request.form.get('type') == "peak":
                u = Peak(colby_id = edited_user.colby_id,
                    first_name = request.form.get('first_name'),
                    last_name = request.form.get('last_name'),
                    password = edited_user.password,
                    email = request.form.get('email')
                    )
                db.session.delete(edited_user)
                db.session.add(u)
                db.session.commit()

            elif request.form.get('type') == "coach":
                u = Coach(colby_id = edited_user.colby_id,
                    first_name = request.form.get('first_name'),
                    last_name = request.form.get('last_name'),
                    password = edited_user.password,
                    email = request.form.get('email')
                    )
                db.session.delete(edited_user)
                db.session.add(u)
                db.session.commit()
            
            elif request.form.get('type') == "athlete":
                u = Athlete(colby_id = edited_user.colby_id,
                    first_name = request.form.get('first_name'),
                    last_name = request.form.get('last_name'),
                    password = edited_user.password,
                    email = request.form.get('email'),
                    gender = request.form.get('gender'),
                    class_year = request.form.get('class_year')
                    )
                db.session.delete(edited_user)
                db.session.add(u)
                db.session.commit()
            
        else:
            edited_user.first_name = request.form.get('first_name')
            edited_user.last_name = request.form.get('last_name')
            edited_user.email = request.form.get('email')
            if edited_user.type == 'athlete':
                edited_user.gender = request.form.get('gender')
                edited_user.class_year = request.form.get('class_year')

            # Save the changes to the database
            db.session.commit()

        return redirect(url_for('main.user_edit_dashboard'))

    return render_template('user_edit.html', edited_user=edited_user, user=current_user)

@routes.route('/team/edit/<int:id>')
@login_required
def team_edit(id):

    # Ensure the current user is an admin
    if current_user.type != "admin":
        return "<h1>NO ACCESS</h1>"

    # Query all athletes and Peak users
    athletes = User.query.filter_by(type='athlete').all()
    peaks = User.query.filter_by(type='peak').all()
    coaches = User.query.filter_by(type='coach').all()
    team = Team.query.get(id)

    def has_athlete(team, athlete):
        return any(association.user == athlete for association in team.team_associations if association.role == 'athlete')
    def has_coach(team, coach):
        return any(association.user == coach for association in team.team_associations if association.role == 'coach')
    def has_peak(team, peak):
        return any(association.user == peak for association in team.team_associations if association.role == 'peak')

    return render_template('team_edit.html', athletes=athletes, peaks=peaks, user=current_user, team=team, coaches=coaches, has_athlete=has_athlete,has_coach=has_coach,has_peak=has_peak)

@routes.route('/update_team/<int:team_id>/<int:user_id>', methods=['POST'])
def update_team(team_id, user_id):
    team = Team.query.get(team_id)
    user = User.query.get(user_id)

    if team and user:
        membership = request.json.get('membership')
        team_association = next(
            (association for association in team.team_associations if association.user == user), None
        )

        if membership:
            if not team_association:
                team_association = TeamUserAssociation(team=team, user=user, role=user.type)
                db.session.add(team_association)
        else:
            if team_association:
                db.session.delete(team_association)

        db.session.commit()
        return jsonify(success=True)
    else:
        return jsonify(success=False)

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

            return render_template('create_notes_dashboard.html', athletes=athletes, user=current_user)

        elif current_user.type == "admin":

            athletes = User.query.filter_by(type='athlete').all()
            return render_template('create_notes_dashboard.html', athletes=athletes, user=current_user)

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
            return redirect(url_for('main.new_note'))
            
# notes dasboard page
@routes.route('/note/dashboard', methods=['GET'])
@login_required
def notes_dashboard():

    if current_user.type == "peak":
        # Get all notes created by the peak
        notes = Note.query.filter_by(creator_id=current_user.id).order_by(Note.created_at.desc()).all()

    else:
        notes = Note.query.order_by(Note.created_at.desc()).all()

    # Render the admin dashboard template with the notes
    return render_template('notes_dasboard.html',user=current_user, notes=notes)

@routes.route('/note/edit/<int:note_id>', methods=['POST'])
def update_note_visibility(note_id):

    note = Note.query.get(note_id)
    if note:
        visibility = request.json.get('visibility')
        note.visible = visibility
        db.session.commit()
        return jsonify(success=True)
    else:
        return jsonify(success=False)
    
@routes.route('/user/new', methods=['GET', 'POST'])
@login_required
def new_user():

    # Ensure the current user is an admin
    if current_user.type != "admin":
        return "<h1>NO ACCESS</h1>"
    
    if request.method == 'POST':

        print('post')
        bol,user = create_user(request.form.get('colby_id'), 
                               request.form.get('first_name'), 
                               request.form.get('last_name'), 
                               request.form.get('email'), 
                               request.form.get('gender'), 
                               request.form.get('class_year'), 
                               request.form.get('type'))
        if bol:
            print('User Created')
            db.session.add(user)
            db.session.commit()
            return(redirect(url_for('main.user_edit_dashboard')))

        else:
            # can also be an array with the colby id and the reason of the error
            print(user)
            return(redirect(url_for('main.new_user')))

    return render_template('user_new.html', user=current_user)

@routes.route('/user/new_csv', methods=['GET', 'POST'])
@login_required
def new_user_csv():

    if request.method == 'POST':
        
        ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}

        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        if 'file' not in request.files:
            flash('No file uploaded')
            return render_template('user_new_csv.html', user=current_user)
        
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return render_template('user_new_csv.html', user=current_user)

        if file and allowed_file(file.filename):
            errors = create_user_csv(file)
            print(errors)
            return(redirect(url_for('main.user_edit_dashboard')))
            
        else:
            flash('Invalid file type')
            return render_template('user_new_csv.html', user=current_user)
        

    return render_template('user_new_csv.html', user=current_user)

@routes.route('/user/remove/<int:id>', methods=['POST'])
@login_required
def remove_user(id):
    # Ensure the current user is an admin
    if current_user.type != "admin":
        return "<h1>NO ACCESS</h1>"

    user = User.query.get(id)

    # Check if the user exists
    if not user:
        return "<h1>User not found</h1>"

    # Remove the user from the database
    db.session.delete(user)
    db.session.commit()

    # Prepare the response JSON
    response = {"success": True}

    return jsonify(response)


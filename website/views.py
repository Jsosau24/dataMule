from urllib import request
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Athlete, Staff, Team, Note
from . import db

views = Blueprint('views', __name__)

#home view
'''
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    """redirect to user's home page
 
    Returns
    -------
    .html: corresponding home page according to user type
    """
    
    role = current_user.role
    if int(role) == 0:
        return render_template("admin_view.html", user=current_user, teams = Team.query.all())
    elif int(role) == 1:
        return render_template("peak_view.html", user=current_user)
    elif int(role) == 2:
        staff = staff.query.filter_by(colby_id=current_user.colby_id).first()
        team = Team.query.filter_by(staff_id=staff.id).first()
        if not team:
            return "<h1>NO ACCESS</h1>"
        return redirect(url_for("views.coach_dashboard", id = team.id))
    elif int(role) == 3:
        return redirect(url_for("views.athlete_dashboard"))
    else:
        return render_template("login.html")
'''

@views.route('/athlete', methods=['GET', 'POST'])
@login_required
def athlete_view():

    return render_template("athlete_view.html", user=current_user)








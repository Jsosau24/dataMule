from flask import Blueprint, render_template
from flask_login import login_required

routes = Blueprint('main', __name__)

@routes.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

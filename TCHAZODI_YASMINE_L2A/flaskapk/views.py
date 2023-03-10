from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@login_required 
def home():
    return render_template("home.html", user=current_user)
    
@views.route('/accueil')
@login_required 
def index():
    return render_template("accueil.html", user=current_user)
    
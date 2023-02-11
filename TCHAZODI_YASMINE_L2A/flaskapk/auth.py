from flask import Blueprint, render_template, request, flash, redirect, url_for 
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET' ,'POST'])
def login():
    if request.method == 'POST':
       email = request.form.get('email')
       password = request.form.get('password')

       user = User.query.filter_by(email=email).first()
       if user: 
        if check_password_hash(user.password, password):
            flash('☻ Vous êtes connecté!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            flash('Mot de passe incorrect!', category='error')
       else:
        flash('L\'email n\'existe pas', category='error ')
    
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET' ,'POST'])
def sign_up():
    flash('Les mot de passes doivent contenir une lettre majuscule,minuscule,contenir des chiffres et des signes alphanumeriques.',category='info')
    flash('la taille de l\'email doit être Au moins 8 caractères celle du nom, du prenom, et du nom d\'utilisateur au moins 2 . Les mots de passes doivent être conforme.', category='info')


    if request.method == 'POST':
        email= request.form.get('email')
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('L\'email existe déjà!', category='error')
        elif len(email) < 8:
            flash('la taille de l\'email est trop petite. Au moins 8 caractères', category='error')
        elif len(nom) < 2:
            flash('la taille du nom est trop petite. Au moins 2 caractères', category='error')
        elif len(prenom) < 3:
            flash('la taille du prénom est trop petite. Au moins 3 caractères', category='error')
        elif len(username) < 2:
            flash('Ce nom d\'utilisateur est trop court. Au moins 2 caractères', category='error')
        elif password1 != password2:
            flash('Les mots de passe saisis ne correspondent pas!', category='error')
        elif len(password1) < 4:
            flash('Au moins 4 caractères pour le mot de passe ', category='error')
        else:
            new_user = User(email=email, nom=nom, prenom=prenom, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Votre Compte a été créé avec succès', category='success')
            
            return redirect(url_for('views.home'))
 


    return render_template("signup.html", user=current_user)

@auth.route('/accueil')
def accueil():
        
        return render_template('accueil.html')

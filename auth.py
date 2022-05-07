#import tous packages
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from __init__ import db


auth = Blueprint('auth', __name__) # Blueprint est un moyen d'organiser view et du code

@auth.route('/login', methods=['GET', 'POST']) # definition page d'authentification -> route = chemin
def login():
    """Fonction login qui gere la page d'authentification -> compte deja existant"""
    if request.method=='GET': # on utilise POST donc si requet get on renvoie a la page d'authentification
        return render_template('login.html')
    else: # on verifie que le user existe
        email = request.form.get('email') 
        password = request.form.get('password') # on recupere l email + password
        remember = True if request.form.get('remember') else False # on regarde si l'utilisateur va garder ses donnes en memoire
        user = User.query.filter_by(email=email).first() # regarde si l'utilisateur existe dans la db
        # -> le password est hashé et on regarde si le password hashé correspond au password hashé dans la db (opérations réalisées par la librairie)
        if not user: # si l'utilisateur n'existe pas
            flash('Please sign up before!')
            return redirect(url_for('auth.signup'))
        elif not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login')) # reload la page si le pass est mauvais
        # si tout  est vérifié on connecte l'utilisateur
        login_user(user, remember=remember)
        return redirect(url_for('main.canvas')) # renvoie a la page canvas

@auth.route('/signup', methods=['GET', 'POST']) # definition page d'inscription -> route = chemin
def signup():
    """Fonction permettant l'inscription de nouveaux membres"""
    if request.method=='GET': # on utilise POST donc si requet get on renvoie a la page d'inscription
        return render_template('signup.html')
    else: # récupere les infos et vérifie que l'email n'existe pas
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first() # retourne l'utilisateur -> en faisant une recherche avec mail
        if user: # si user -> alors l'utilisateur existe et donc on renvoie a la page d'authentification
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))
        # sinon on ajoute l'utilisateur a la db 
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256')) # le pass est hashé en sha256
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login')) # renvoie a la page d'authentification

@auth.route('/logout') # route -> deconnexion
@login_required
def logout(): # deconnexion
    logout_user()
    return redirect(url_for('main.canvas'))
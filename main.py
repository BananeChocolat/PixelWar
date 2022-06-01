#on import les packages
from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from __init__ import create_app, db # on importe les paquets contenus dans le fichier __init__
from datetime import datetime
from editpixel import edit_pixel,save_to_csv
import sqlite3
import logging
import hashlib


log=logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def check_cookie(user,cookie):
    password='PhraseSecrete1'+user+'PhraseSecrete2' # changer sur le vrai site
    hash_password=hashlib.md5(password.encode()).hexdigest()
    return hash_password==cookie

def get_all_users(db):
    username_list=[]
    con=sqlite3.connect(db)
    cur=con.cursor()
    for username in cur.execute('SELECT name FROM User;'):
        if username[0] not in username_list:
            username_list.append(username[0])
    return username_list

username_list=get_all_users('db.sqlite')

jail={}



def add_acc_time(account):
    """Ajoute un compte a la 'prison' permet cooldown"""
    jail[account]=datetime.now()

def check_time(account):
    """Renvoie vrai si le compte n'a pas fait de requete dans les 5 dernieres minutes (delai)"""
    a=datetime.now()
    difference=a-jail[account]
    if difference.total_seconds()>300.0:
        return True
    else:
        return False

def return_time(account):
    """Retourne le temps restant en seconde"""
    a=datetime.now()
    return 300-(abs((jail[account]-a).total_seconds()))

main = Blueprint('main', __name__)

@main.route('/') # route de base / url index
def index():
    print(f'[INDEX] User on index')
    return render_template('index.html') # renvoie la page index.html dans le dossier templates

@main.route('/canvas') # retourne la page profile
# @login_required # permet de verifier si l'utilisateur est connecté -> pas utile ici
def canvas():
    print(f'[CANVAS] User on canvas')
    return render_template('canvas.html') # renvoie la page profile.html et set name = nom_du_compte

app = create_app() # on cree l'app (voir __init__.py)
if __name__ == '__main__': 
    db.create_all(app=create_app()) # cree la db sqlite 
    app.run() 

@main.route('/cooldown')
def cooldown():
    """Fonction get qui gere le cooldown"""
    
    user=request.args.get('user')
    if len(user) >0:
        print(f'Giving cooldown for {user}')
        if user not in jail or return_time(user)<0:
            return jsonify({'user':user,'timer':0})
        else:
            return jsonify({'user':user,'timer':int(return_time(user))})
    else:
        return jsonify({'visitor':True})
    

@main.route('/editpixel', methods=['POST']) 
def foo():
    

    data = request.json
    
    username=data['username']
    cookie=data['cookie']
    if username in username_list and check_cookie(username,cookie):
        if username not in jail : # l'utilisateur n'a jamais fait de requete alors il est ajouté à jail
            add_acc_time(username)
            print(f'[EDIT] Added cooldown for {username} : {jail[username]}')
            x,y,r,g,b = data['position'][0], data['position'][1], data['color'][0], data['color'][1], data['color'][2]
            edit_pixel(x,y,r,g,b, './frontend/canvas.csv')
            return jsonify({'success':'True'}) # il n'a jamais fais de requetes donc c'est validé
        else:
            if check_time(username):  # si le cooldown utilisateur depasse 5min c'est bon sinon non
                add_acc_time(username)
                print(f'[EDIT] New cooldown for {username} : {jail[username]}')
                edit_pixel(data['position'][0],data['position'][1],data['color'][0],data['color'][1],data['color'][2],'./frontend/canvas.csv')
                return jsonify({'success':'True'})
            else:
                
                print(f'[EDIT] Waiting cooldown for {username} : {jail[username]}')
                return jsonify({'success':'False'})
    else:
        print(f'[EDIT] Username not in DB : {username} | cookie : {cookie}')
        return jsonify({'sucess':'False'})

    
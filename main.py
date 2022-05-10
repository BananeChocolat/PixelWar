#on import les packages
from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from __init__ import create_app, db # on importe les paquets contenus dans le fichier __init__
from datetime import datetime
from editpixel import edit_pixel,save_to_csv
import sqlite3





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
    difference=jail[account]-a
    if difference.total_seconds()>300.0:
        return True
    else:
        return False

main = Blueprint('main', __name__)

@main.route('/') # route de base / url index
def index():
    return render_template('index.html') # renvoie la page index.html dans le dossier templates

@main.route('/canvas') # retourne la page profile
# @login_required # permet de verifier si l'utilisateur est connecté -> pas utile ici
def canvas():
    return render_template('canvas.html') # renvoie la page profile.html et set name = nom_du_compte

app = create_app() # on cree l'app (voir __init__.py)
if __name__ == '__main__': 
    db.create_all(app=create_app()) # cree la db sqlite 
    app.run(debug=True) # execute l'app en mode debug


@main.route('/editpixel', methods=['POST']) 
def foo():
    

    data = request.json
    
    username=data['username']
    if username in username_list:
        if username not in jail: # l'utilisateur n'a jamais fait de requete alors il est ajouté à jail
            add_acc_time(username)
            print(f'Added cooldown for {username} : {jail[username]}')
            x,y,r,g,b = data['position'][0], data['position'][1], data['color'][0], data['color'][1], data['color'][2]
            edit_pixel(x,y,r,g,b, './frontend/canvas.csv')
            return jsonify({'success':'True'}) # il n'a jamais fais de requetes donc c'est validé
        else:
            if check_time(username):  # si le cooldown utilisateur depasse 5min c'est bon sinon non
                add_acc_time(username)
                print(f'New cooldown for {username} : {jail[username]}')
                edit_pixel(data['position'][0],data['position'][1],data['color'][0],data['color'][1],data['color'][2],'./frontend/canvas.csv')
                return jsonify({'success':'True'})
            else:
                print(f'Waiting cooldown for {username} : {jail[username]}')
                return jsonify({'success':'False'})
    else:
        print(f'Username not in DB : {username}')
        return jsonify({'sucess':'False'})

    
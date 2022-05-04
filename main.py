#on import les packages
from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from __init__ import create_app, db # on importe les paquets contenus dans le fichier __init__
from datetime import datetime

jail={}



def add_acc_time(account):
    
    jail[account]=datetime.now()

def check_time(account):
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
    print(data)
    if data['username'] not in jail:
        add_acc_time(data['username'])
        return jsonify({'success':'True'})
    else:
        if check_time(data['username']):
            add_acc_time(data['username'])
            return jsonify({'success':'True'})
        else:
            return jsonify({'success':'False'})

    
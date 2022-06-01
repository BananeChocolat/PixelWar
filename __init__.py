from flask import Flask,redirect,url_for
from flask_admin import Admin, AdminIndexView,expose
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op

# documentation pour configuration sqlalchemy : https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
# documentation pour flask-login : https://flask-login.readthedocs.io/en/latest/
# documentation pour blueprint : https://flask.palletsprojects.com/en/2.1.x/tutorial/views/




db = SQLAlchemy()# sqlalchemy permet de creer / manipuler des db avec flask

def create_app():
    """ Fonction qui cree l'application utilisée dans Flask et qui va gerer les authentifications """
    
    app = Flask(__name__,static_folder='./frontend') # on cree l'app flask ,
    app.config['SECRET_KEY'] = 'b0nj0ur-m0nsieur-si-v0us-lisez-le-c0de' # clee utilisée pour encrypter donnes de la base de maniere sécurisée
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' # chemin vers la db (creations + modifications)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # permet de ne pas afficher les messages de debug de modification (recommendée d'être désactivée car consomme)
    db.init_app(app) # on initialise la db avec l'app flask une fois la configuartion finie
    
    
     
    #on adapate le code pour que l'on puisse l'integrer au site
    login_manager = LoginManager() # on cree ce qui va gerer les authentifications => lien website et base données
    login_manager.login_view = 'auth.login' # redirection vers la page de login lorsque l'on veut acceder à une page où compte est requis
    login_manager.init_app(app) # initialisation de l'authentification
    
   

    from models import User # import class user -> modele pour compte
    
    class MyAdminIndexView(AdminIndexView):
        def is_accessible(self):
            if current_user.is_authenticated:
                if current_user.name=='admin1':
                    return True
            else:
                return  False
        def inaccessible_callback(self,name, **kwargs):
            return redirect(url_for('auth.login'))
        
    
    admin = Admin(app, name='Admin', template_mode='bootstrap3',index_view=MyAdminIndexView()) # on cree l'admin
    admin.add_view(ModelView(User, db.session))
    path = op.join(op.dirname(__file__), 'frontend')
    admin.add_view(FileAdmin(path, '/frontend/', name='Static Files'))


    @login_manager.user_loader
    def load_user(user_id): 
        """recharge utilisateur grace a son id"""
        # user id = cle primaire donc on peut utiliser pour recherches
        return User.query.get(int(user_id))
    
    # blueprint permet de gerer l'application et les chemins d'acces
    from auth import auth as auth_blueprint # import blueprint auth (fichier auth.py)
    app.register_blueprint(auth_blueprint)
    # auth_blueprint va etre utilise pour enregistrer comptes / acces -> liaison python SQL
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app # on retourne l'app flask finie ( config + login + gerer db + gerer chemins acces)


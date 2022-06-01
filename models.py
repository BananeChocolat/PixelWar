from flask_login import UserMixin
from __init__ import db

class User(UserMixin, db.Model): #class user qui va gerer toutes les infos nécessaires à l'utilisateur
    id = db.Column(db.Integer, primary_key=True) # cle primaire / id
    email = db.Column(db.String(100), unique=True) # email unique
    password = db.Column(db.String(100)) # mot de passe
    name = db.Column(db.String(1000),unique=True)   # nom de l'utilisateur 

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated
    
   
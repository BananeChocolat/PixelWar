# import packages
import mysql.connector as MySQLdb
import sys
sys.path.insert(0,'../.')
import config
import pandas as pd

#cree une db avec mysql,
def create_db(mysql_user=config.mysql_user, mysql_password=config.mysql_password ,mysql_host=config.mysql_host, db_name=config.db_name):
    """Cree la base de donnée"""
    try:
        conn = MySQLdb.connect(user=mysql_user, host=mysql_host, password=mysql_password) #conect à la db
        print('Connection to mysql server Done : success')
        try:
            cur = conn.cursor() # se connecte à la db | les commandes suivantes seront donc executées si cela fonctionne
            cur.execute("CREATE DATABASE IF NOT EXISTS "+db_name+" ;") #cree la db si elle n'existe pas dans mysql sinon ne fait rien
            conn.commit()  # applique les changements
            print("database created with success")
        finally:
            conn.close() # ferme la db une fois fini si pas d'erreur
            print("connection closed !")
    except:
        print("I am unable to connect to the database") #sinon -> erreur de connexion à la db


#va venir creer la table dans la db
def create_table(mysql_user=config.mysql_user, mysql_password=config.mysql_password ,mysql_host=config.mysql_host,table_name=config.table_name, db_name=config.db_name):
    """ Cree une table dans la base de donnée"""
    try:
        conn = MySQLdb.connect(user=mysql_user, host=mysql_host, password=mysql_password,  database=db_name) # connexion à la db
        print('Connection to mysql server Done : success')
        try:
            cur = conn.cursor() # se connecte à la db | les commandes suivantes seront donc executées si cela fonctionne
            cur.execute("""CREATE TABLE IF NOT EXISTS %s (id INT AUTO_INCREMENT PRIMARY KEY, 
                                                                              email varchar(250), 
                                                                              name varchar(250),
                                                                              password varchar(250) 
                                                                              );""" %(table_name))# cree la table si elle n'existe pas 
            #vachar(250) -> 250 caractères max pour du texte 
            conn.commit()
            print("Table created with success") # si cela fonctionne revoie message de succes
        finally:
            conn.close() # on clot la connexion
            print("connection closed !")

    except:
        print("I am unable to connect to the database") # erreur si pb de connexion

def insert_row(email, name, password, user_name=config.mysql_user, mysql_password=config.mysql_password, host_name=config.mysql_host, db_name=config.db_name, table_name=config.table_name):
    """Procédure permettant d'inserer des infos dans la table"""
    conn = MySQLdb.connect(user=user_name, password=mysql_password, host=host_name, database=db_name)
    try:
        cursor = conn.cursor()
        cursor.execute("""insert into %s (email, name, password) values ('%s', '%s', '%s'); """ %(table_name, email, name, password)) #insere les infos dans la table
        conn.commit()
    finally:
        conn.close()
    print('Row inserted') # si cela fonctionne revoie message de succes


def import_data(query, mysql_user=config.mysql_user, mysql_password=config.mysql_password, mysql_host=config.mysql_host):
    """Permet de recuperer les donnees de la table selon une requete """
    try: #essaye de se connecter à la db 
        conn = MySQLdb.connect(user=mysql_user, host=mysql_host, password=mysql_password)
        print('Connection to mysql server Done : success')
        print(query)
    except:
        print("I am unable to connect to the database")
    try: #essaye d'executer la requete sql
        cur = conn.cursor()
        cur.execute(query)
        results = cur.fetchall() # recupere les donnees de la requete 
        data = pd.DataFrame(list(results), columns=[row[0] for row in cur.description]).reset_index(drop=True) #organise les données grâce à panda
        print(data) # affiche les données
    finally:
        conn.close()
    return (data) # retourne les données

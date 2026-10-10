import sqlite3


class Database():

    # Definir le constructeur de la classe
    def __init__(self):
        self.connection = None

    # Definir une connexion avec la base de données
    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect("db/information.db")
        return self.connection

    # Deconnexion de la base de données
    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None


    # Pour inserer un evenement dans la base de données
    def insertion_evenement(self):
        connection = self.get_connection()
        mycursor = connection.cursor()
        mycursor.execute((
            "insert into Evenement (evenement_nom, evenement_date, evenement_description, "
            "evenement_categorie, evenement_prix, evenement_billets)"
            "VALUES (?, ?, ?, ?, ?, ?)"))
        connection.commit()

    
    # Recherche de touts les evenements
    def get_all_evenement(self):
        cursor = self.get_connection().cursor()
        cursor.execute(
            "SELECT distinct Evenement.evenement_nom, Evenement.evenement_date,"
            "Evenement.evenement_description ,Evenement.evenement_categorie,"
            "Evenement.evenement_prix ,Evenement.evenement_billets"
            " FROM Evenement ORDER BY evenement_nom")
        evenements = cursor.fetchall()
        return evenements
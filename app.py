from database import Database
from flask import Flask, g, request, render_template, Response, redirect, url_for

app = Flask(__name__)


def get_db():
    # Créer une ressource si cette dernière n'existe pas
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


# Fermer/ Désaloueer la ressource si elle existe
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()

# cette classe est destiné pour les routes
@app.route("/accueil.html")
@app.route("/")
def get_accueil():
    return render_template("index.html")

@app.route("/calendrier.html")
def get_calendrier():
    return render_template("calendrier.html")


@app.route("/connexion.html")
def get_connexion():
    return render_template("connexion.html")


@app.route("/recherche.html")
def get_recherche():
    return render_template("recherche.html")

@app.route("/index.html")
def get_index():
    return render_template("index.html")



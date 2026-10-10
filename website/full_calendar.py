from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from flask import Flask
from .models import Festivalier, Adresse, Producteur, Evenement, Inscription
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  # means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime, date
from base64 import b64encode
import base64
from io import BytesIO
from werkzeug.utils import secure_filename
import os
from flask_sqlalchemy import SQLAlchemy

fcal = Blueprint('fullcalendar', __name__)
app = Flask(__name__)


eventstest = [
    {
        'name': 'xxxxx',
        'date_debut': '2023-04-22',
        'date_fin': '2023-04-28',
        'image': '../static/uploads/aladin.jpg'
    }
]


# Méthode pour afficher touts les évènements dans le calendrier
@fcal.route('/full_calendar', methods=['GET', 'POST'])
def full_calendar():
    events = Evenement.query.all()
    return render_template('/no_co/full_calendar.html', events=events)


# Méthode pour afficher tous les événements inscrit par le festivalier dans le calendrier
@fcal.route('/fest_full_calendar', methods=['GET', 'POST'])
def fest_full_calendar():
    inscriptions = Inscription.query.filter_by(
        inscription_evenement="Panier", id_festivalier=current_user.get_id()).all()
    events = inscriptions
    return render_template('/festivalier/fest_full_calendar.html',
                           events=events, user=current_user)


# Méthode pour afficher touts les évènements ajouté par le producteur dans le calendrier
@fcal.route('/prod_full_calendar', methods=['GET', 'POST'])
def prod_full_calendar():
    evenements = Evenement.query.filter(
        Evenement.producteur_id == current_user.id)
    events = evenements
    return render_template('/producteur/prod_full_calendar.html', events=events)

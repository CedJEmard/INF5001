from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
import json
from .models import Evenement, Inscription


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    evenements = Evenement.query.all()
    return render_template("/no_co/programmation.html",
                           user=current_user, evenements=evenements)


# DEPRICATED
@views.route('/calendrier', methods=['GET', 'POST'])
def calendrier():
    return render_template("calendrier.html", user=current_user)
# - - -


@views.route('/home_co', methods=['GET', 'POST'])
def home_co():
    return redirect(url_for('event_festivalier.programmation_festivalier'))


@views.route('/connectAdmin', methods=['GET', 'POST'])
def connectAdmin():
    return render_template("connectFest.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    # this function expects a JSON from the INDEX.js file
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

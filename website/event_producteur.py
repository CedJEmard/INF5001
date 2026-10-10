from flask import Blueprint, render_template, request, flash, redirect
from flask import Flask
from .models import Producteur, Adresse, Evenement
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  # means from __init__.py import db
from flask_login import current_user
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from sqlalchemy import and_
event_producteur = Blueprint('event_producteur', __name__)
app = Flask(__name__)
# Creating the upload folder
upload_folder = os.path.join('static', 'uploads')

app.config['UPLOAD'] = upload_folder


# Méthode pour ajouter un nouvel évènement en tant que producteur
@event_producteur.route('/Producteur', methods=['GET', 'POST'])
def producteur():
    if request.method == 'POST':
        date = request.form.get('date')
        name = request.form.get('name')
        date2 = request.form.get('date2')
        noCiv = request.form.get('noCivique')
        rue = request.form.get('rue')
        codePostal = request.form.get('codePostal')
        ville = request.form.get('ville')
        description = request.form.get('description')
        nbBillet = request.form.get('nbBillet')
        prixBillet = request.form.get('prixBillet')
        categorie = request.form.get('categorie')
        image = request.files['file']
        flash(secure_filename(image.filename))
        filename = secure_filename(image.filename)
        # enregistre le fichier dans le folder upload
        image.save(os.path.join('website', 'static', 'uploads', filename))
        # pour stocker la route(path)de la photo dans la bd
        fp = os.path.join('..', 'static', 'uploads', filename)

        event = Evenement.query.filter_by(name=name).first()

        if event:
            flash('Event already exists.', category='error')

        elif len(name) < 2:
            flash('Name must be greater than 1 character.', category='error')

        else:
            new_adress = Adresse(rue=rue, pays="Canada", ville=ville,
                                 province="Qc", noCivique=noCiv, codePostal=codePostal,)
            db.session.add(new_adress)
            db.session.commit()
            new_event = Evenement(name=name, description=description,
                                  date_debut=datetime.strptime(
                                      date, '%Y-%m-%d'),
                                  date_fin=datetime.strptime(
                                      date2, '%Y-%m-%d'),
                                  nbBillets=nbBillet, prix=prixBillet,
                                  adresse_id=new_adress.id, categorie=categorie,
                                  producteur_id=current_user.id, image=fp)
            db.session.add(new_event)
            db.session.commit()
            return redirect('/Producteur')
    return render_template("/producteur/ajout_event.html", user=current_user)


# Méthode qui affiche touts les évènements du producteurs connectés
@event_producteur.route('/prod_mes_evenements')
def prod_mes_evenements():
    evenements = Evenement.query.filter(
        Evenement.producteur_id == current_user.id)
    return render_template('/producteur/prod_mes_evenements.html',
                           evenements=evenements, user=current_user)


# Méthode qui affiche les détails d'un évènement du producteurs connectés
@event_producteur.route('mon_event/<int:id>', methods=['GET', 'POST'])
def mon_event(id):
    evenements = Evenement.query.all()
    un_evenement = Evenement.query.get(int(id))
    return render_template("/producteur/prod_un_event.html",
                           un_evenement=un_evenement, evenements=evenements)


# Méthode qui modifie un évènement dans la base de donnée
@event_producteur.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    event_to_modify = Evenement.query.get_or_404(id)
    if request.method == "POST":
        event_to_modify.date_debut = datetime.strftime(
            event_to_modify.date_debut, '%Y-%m-%d')
        event_to_modify.date_debut = request.form['date_debut']
        event_to_modify.date_debut = datetime.strptime(
            event_to_modify.date_debut, '%Y-%m-%d')
        event_to_modify.date_fin = datetime.strftime(
            event_to_modify.date_fin, '%Y-%m-%d')
        event_to_modify.date_fin = request.form['date_fin']
        event_to_modify.date_fin = datetime.strptime(
            event_to_modify.date_fin, '%Y-%m-%d')
        event_to_modify.name = request.form['name']
        event_to_modify.description = request.form['description']
        event_to_modify.prix = request.form['prix']
        event_to_modify.nbBillets = request.form['nbBillets']
        db.session.commit()
        flash("Evenement modifier")
        return redirect('/prod_mes_evenements')

    return render_template('/producteur/update.html',
                           event_to_modify=event_to_modify)


# Méthode qui supprime un évènement dans la base de donnée
@event_producteur.route('/supprimer_prod/<int:id>')
def supprimer_prod(id):
    event_to_delete = Evenement.query.get_or_404(id)
    try:
        db.session.delete(event_to_delete)
        db.session.commit()
        flash("evenement supprimer")
        return redirect('/prod_mes_evenements')
    except:
        flash("erreur")


# Méthode pour faire une recherche d'évènement selon les catégories, la ville et le nom de l'évènement connexion producteur
@event_producteur.route('/prod_recherche', methods=['GET', 'POST'])
def prod_recherche():
    if request.method == 'POST':
        categorie = request.form.get('categorie')
        laRecherche = request.form.get('laRecherche')
        laRecherche = "%{}%".format(laRecherche)

        if categorie == 'Catégorie':
            if Evenement.query.filter(Evenement.description.ilike(laRecherche)).all():
                evenement = Evenement.query.filter(
                    Evenement.description.ilike(laRecherche)).all()
            else:
                evenement = Evenement.query.filter(
                    Evenement.name.ilike(laRecherche)).all()
        elif categorie == 'Nom':
            evenement = Evenement.query.filter(
                Evenement.name.ilike(laRecherche)).all()
        elif categorie == 'Ville':
            evenement = Evenement.query.join(Adresse).filter(
                Adresse.ville.ilike(laRecherche)).all()
        elif Evenement.query.filter(Evenement.categorie.ilike(categorie)):
            if Evenement.query.filter(Evenement.categorie.ilike(categorie),
                                      Evenement.name.ilike(laRecherche)).all():
                evenement = Evenement.query.filter(Evenement.categorie.ilike(
                    categorie), Evenement.name.ilike(laRecherche)).all()
            elif Evenement.query.filter(Evenement.categorie.ilike(categorie),
                                        Evenement.description.ilike(laRecherche)).all():
                evenement = Evenement.query.filter(Evenement.categorie.ilike(
                    categorie), Evenement.description.ilike(laRecherche)).all()
            else:
                return render_template("/producteur/prod_recherche.html",
                                       Evenement=Evenement.query.all())

        return render_template('/producteur/prod_mes_evenements.html',
                               evenements=evenement, user=current_user)
    return render_template("/producteur/prod_recherche.html",
                           Evenement=Evenement.query.all())

from flask import Blueprint, render_template, request, redirect, flash
from flask import Flask
from .models import Adresse, Evenement, Inscription
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user

event_in = Blueprint('event_in', __name__)
app = Flask(__name__)


# Méthode qui affiche touts les évènements sans être connecté
@event_in.route('/programmation')
def programmation():
    evenements = Evenement.query.all()
    return render_template('/no_co/programmation.html', evenements=evenements)


# Méthode qui affiche les détails d'un évènement sans être connecté
@event_in.route('un_event/<int:id>', methods=['GET', 'POST'])
def un_event(id):
    evenements = Evenement.query.all()
    un_evenement = Evenement.query.get(int(id))
    return render_template("/no_co/un_event.html",
                           un_evenement=un_evenement, evenements=evenements)


# Méthode qui affiche touts les évènements filtrés par la catégorie concert sans être connecté
@event_in.route('/filtre_concert')
def filtre_concert():
    evenement = Evenement.query.filter_by(categorie="Concert").all()
    return render_template('/no_co/programmation.html', evenements=evenement)


# Méthode qui affiche touts les évènements filtrés par la catégorie sport sans être connecté
@event_in.route('/filtre_sport')
def filtre_sport():
    evenement = Evenement.query.filter_by(categorie="Sport").all()
    return render_template('/no_co/programmation.html', evenements=evenement)


# Méthode qui affiche touts les évènements filtrés par la catégorie humour sans être connecté
@event_in.route('/filtre_humour')
def filtre_humour():
    evenement = Evenement.query.filter_by(categorie="Humour").all()
    return render_template('/no_co/programmation.html', evenements=evenement)


# Méthode qui affiche touts les évènements filtrés par la catégorie festivals sans être connecté
@event_in.route('/filtre_festivals')
def filtre_festivals():
    evenement = Evenement.query.filter_by(categorie="Festivals").all()
    return render_template('/no_co/programmation.html', evenements=evenement)


# Méthode qui affiche touts les évènements filtrés par ordre chronologique sans être connecté
@event_in.route('/filtre_ordre')
def filtre_ordre():
    evenement = Evenement.query.order_by(Evenement.date_debut).all()
    return render_template('/no_co/programmation.html', evenements=evenement)


# Méthode qui affiche touts les évènements filtrés par la catégorie concert connexion festivalier
@event_in.route('/fest_filtre_concert')
def fest_filtre_concert():
    evenement = Evenement.query.filter_by(categorie="Concert").all()
    return render_template('/festivalier/fest_programmation_filtre.html',
                           evenements=evenement)


# Méthode qui affiche touts les évènements filtrés par la catégorie sport connexion festivalier
@event_in.route('/fest_filtre_sport')
def fest_filtre_sport():
    evenement = Evenement.query.filter_by(categorie="Sport").all()
    return render_template('/festivalier/fest_programmation_filtre.html',
                           evenements=evenement)


# Méthode qui affiche touts les évènements filtrés par la catégorie humour connexion festivalier
@event_in.route('/fest_filtre_humour')
def fest_filtre_humour():
    evenement = Evenement.query.filter_by(categorie="Humour").all()
    return render_template('/festivalier/fest_programmation_filtre.html',
                           evenements=evenement)


# Méthode qui affiche touts les évènements filtrés par la catégorie festivals connexion festivalier
@event_in.route('/fest_filtre_festivals')
def fest_filtre_festivals():
    evenement = Evenement.query.filter_by(categorie="Festivals").all()
    return render_template('/festivalier/fest_programmation_filtre.html',
                           evenements=evenement)


# Méthode qui affiche touts les évènements filtrés par ordre chronologique connexion festivalier
@event_in.route('/fest_filtre_ordre')
def fest_filtre_ordre():
    evenement = Evenement.query.order_by(Evenement.date_debut).all()
    return render_template('/festivalier/fest_programmation_filtre.html',
                           evenements=evenement)


# Méthode qui affiche les évènements inscrit des festivaliers filtrés par catégorie sport
# (pour la page Mes Évènements)
@event_in.route('/fest_filtre_sport_mes_evenments')
def fest_filtre_sport_mes_evenments():
    inscription = Inscription.query.filter(
        Inscription.id_festivalier == current_user.id).all()
    evenements = ""
    if inscription:
        evenements = Evenement.query.filter(
            Evenement.id == Inscription.evenement_id, Evenement.categorie == 'Sports')
    return render_template('/festivalier/mes_event_festivalier.html',
                           evenements=evenements, user=current_user)


# Méthode qui affiche les évènements inscrit des festivaliers filtrés par catégorie humour
# (pour la page Mes Évènements)
@event_in.route('/fest_filtre_humour_mes_evenments')
def fest_filtre_humour_mes_evenments():
    inscription = Inscription.query.filter(
        Inscription.id_festivalier == current_user.id).all()
    evenements = ""
    if inscription:
        evenements = Evenement.query.filter(
            Evenement.id == Inscription.evenement_id, Evenement.categorie == 'Humour')
    return render_template('/festivalier/mes_event_festivalier.html',
                           evenements=evenements, user=current_user)


# Méthode qui affiche les évènements inscrit des festivaliers filtrés par catégorie festivals
# (pour la page Mes Évènements)
@event_in.route('/fest_filtre_festivals_mes_evenments')
def fest_filtre_festivals_mes_evenments():
    inscription = Inscription.query.filter(
        Inscription.id_festivalier == current_user.id).all()
    evenements = ""
    if inscription:
        evenements = Evenement.query.filter(
            Evenement.id == Inscription.evenement_id, Evenement.categorie == 'Festivals')
    return render_template('/festivalier/mes_event_festivalier.html',
                           evenements=evenements, user=current_user)


# Méthode qui affiche les évènements inscrit des festivaliers filtrés ordre chronologique
# (pour la page Mes Évènements)
@event_in.route('/fest_filtre_ordre_mes_evenments')
def fest_filtre_ordre_mes_evenments():
    inscription = Inscription.query.filter(
        Inscription.id_festivalier == current_user.id).all()
    evenements = ""
    if inscription:
        evenements = Evenement.query.filter(
            Evenement.id == Inscription.evenement_id, ).order_by(Evenement.date_debut)
    return render_template('/festivalier/mes_event_festivalier.html',
                           evenements=evenements, user=current_user)


# Méthode qui affiche les évènements inscrit des festivaliers filtrés par catégorie concert
# (pour la page Mes Évènements)
@event_in.route('/fest_filtre_concert_mes_evenments')
def fest_filtre_concert_mes_evenments():
    inscription = Inscription.query.filter(
        Inscription.id_festivalier == current_user.id).all()
    evenements = ""
    if inscription:
        evenements = Evenement.query.filter(
            Evenement.id == Inscription.evenement_id, Evenement.categorie == 'Concerts')
    return render_template('/festivalier/mes_event_festivalier.html',
                           evenements=evenements, user=current_user)


# Méthode qui affiche les évènements des producteurs filtrés par catégorie concert
# (pour la page Mes Évènements)
@event_in.route('/prod_filtre_concert')
def prod_filtre_concert():
    evenement = Evenement.query.filter_by(categorie="Concert").all()
    return render_template('/producteur/prod_programmation_filtre.html',
                           evenements=evenement)


# Méthode qui affiche les évènements des producteurs filtrés par catégorie sport
# (pour la page Mes Évènements)
@event_in.route('/prod_filtre_sport')
def prod_filtre_sport():
    evenement = Evenement.query.filter_by(categorie="Sport").all()
    return render_template('/producteur/prod_programmation_filtre.html',
                           evenements=evenement)


# Méthode qui affiche les évènements des producteurs filtrés par catégorie humour
# (pour la page Mes Évènements)
@event_in.route('/prod_filtre_humour')
def prod_filtre_humour():
    evenement = Evenement.query.filter_by(categorie="Humour").all()
    return render_template('/producteur/prod_programmation_filtre.html',
                           evenements=evenement)


# Méthode qui affiche les évènements des producteurs filtrés par catégorie festivals
# (pour la page Mes Évènements)
@event_in.route('/prod_filtre_festivals')
def prod_filtre_festivals():
    evenement = Evenement.query.filter_by(categorie="Festivals").all()
    return render_template('/producteur/prod_programmation_filtre.html',
                           evenements=evenement)


# Méthode qui affiche les évènements des producteurs filtrés par ordre chronologique
# (pour la page Mes Évènements)
@event_in.route('/prod_filtre_ordre')
def prod_filtre_ordre():
    evenement = Evenement.query.order_by(Evenement.date_debut).all()
    return render_template('/producteur/prod_programmation_filtre.html',
                           evenements=evenement)


# Méthode pour faire une recherche d'évènement selon les catégories, la ville et le nom de l'évènement
@event_in.route('/recherche', methods=['GET', 'POST'])
def recherche():
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
                return render_template("/no_co/recherche.html",
                                       Evenement=Evenement.query.all())

        return render_template('/no_co/programmation.html', evenements=evenement)
    return render_template("/no_co/recherche.html", Evenement=Evenement.query.all())

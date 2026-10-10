from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import Flask
from .models import Adresse, Evenement, Inscription
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import current_user
from flask_weasyprint import HTML, render_pdf
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import email
import email.mime.application

event_festivalier = Blueprint('event_festivalier', __name__)
app = Flask(__name__)

SMTP_HOST = "smtp.googlemail.com"
SMTP_PORT = 587


# Méthode pour faire une recherche d'évènement selon les catégories,
# la ville et le nom de l'évènement connexion festivalier
@event_festivalier.route('/fest_recherche', methods=['GET', 'POST'])
def fest_recherche():
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
                return render_template("/festivalier/fest_recherche.html",
                                       Evenement=Evenement.query.all())

        return render_template('/festivalier/programmation_festivalier.html', evenements=evenement)
    return render_template("/festivalier/fest_recherche.html", Evenement=Evenement.query.all())


# Méthode qui affiche touts les évènements pour un festivalier connecté
@event_festivalier.route('/programmation_festivalier')
def programmation_festivalier():
    evenements = Evenement.query.all()
    return render_template('/festivalier/programmation_festivalier.html',
                           evenements=evenements)


# Méthode qui affiche les détails d'un évènement pour un festivalier connecté
@event_festivalier.route('un_event_festivalier/<int:id>', methods=['GET', 'POST'])
def un_event_festivalier(id):
    evenements = Evenement.query.all()
    un_evenement = Evenement.query.get(int(id))
    if request.method == 'POST':
        nb_billets = request.form.get('nb_billets')
        flash(nb_billets)
        inscription(id=un_evenement.id, nb=nb_billets)
    return render_template("/festivalier/un_event_festivalier.html",
                           un_evenement=un_evenement, evenements=evenements)


# Méthode pour inscrire un festivalier à un évènement
@event_festivalier.route('inscription/<int:id>', methods=['GET', 'POST'])
def inscription(id, nb):
    nb_billets = int(nb)
    deja_inscrit = Inscription.query.filter_by(
        evenement_id=int(id), id_festivalier=current_user.id).first()
    if nb_billets is None:
        flash('nombre de billets manquant', category='error')
        return redirect('/programmation_festivalier')
    elif deja_inscrit and deja_inscrit.inscription_evenement == "Panier":
        deja_inscrit.inscription_nb = deja_inscrit.inscription_nb+nb_billets
        db.session.add(deja_inscrit)
        db.session.commit()
        return redirect('/programmation_festivalier')
    elif nb_billets and deja_inscrit:
        new_inscription = Inscription(evenement_id=id, id_festivalier=current_user.id,
                                      inscription_evenement="Panier",
                                      inscription_nb=nb_billets)
        db.session.add(new_inscription)
        db.session.commit()
        flash("ajouter evenement")
    else:
        new_inscription = Inscription(evenement_id=id, id_festivalier=current_user.id,
                                      inscription_evenement="Panier",
                                      inscription_nb=nb_billets)
        db.session.add(new_inscription)
        db.session.commit()
        flash("ajouter evenement")
    evenements = Evenement.query.all()
    return render_template('/festivalier/programmation_festivalier.html',
                           inscription=new_inscription, user=current_user,
                           evenements=evenements)


# Méthode qui affiche touts les évènements dont le festivalier connecté s'est inscrit
@event_festivalier.route('/mes_event_festivalier')
def mes_event_festivalier():
    inscription = Inscription.query.filter(
        Inscription.id_festivalier == current_user.id).all()
    evenements = ""
    if inscription:
        evenements = Evenement.query.filter(
            Evenement.id == Inscription.evenement_id)
    return render_template('/festivalier/mes_event_festivalier.html',
                           evenements=evenements, user=current_user)


# Méthode qui affiche en format pdf touts les évènements dont le festivalier connecté s'est inscrit
@event_festivalier.route('/mes_event_festivalier_pdf')
def mes_event_festivalier_pdf():
    inscription = Inscription.query.filter(
        Inscription.id_festivalier == current_user.id).all()
    evenements = ""
    if inscription:
        evenements = Evenement.query.filter(
            Evenement.id == Inscription.evenement_id)
    return render_template('pdf.html', evenements=evenements, user=current_user)


# Méthode pour finaliser le panier des évènements dont le festivalier connecté s'est inscrit
@event_festivalier.route('/checkout', methods=['GET', 'POST'])
def checkout():
    inscriptions = ""
    events = ""
    prix_total = 0
    if current_user:
        inscriptions = Inscription.query.filter_by(
            inscription_evenement="Panier",
            id_festivalier=current_user.get_id()).all()
        events = Evenement.query.all()
        for inscription in inscriptions:
            for event in events:
                billet = event.prix
                qte = inscription.inscription_nb
                if inscription.evenement_id == event.id:
                    if qte:
                        prix_total = prix_total + (billet*qte)
    if request.method == 'POST':
        numCarte = request.form.get('numCarte')
        description = request.form.get('description')
        name = request.form.get('name')
        telephone = request.form.get('telephone')
        if len(numCarte) < 6:
            flash('Le nombre de chiffre doit etre de 12', category='error')
        elif numCarte:
            inscriptions = Inscription.query.filter_by(
                inscription_evenement="Panier", id_festivalier=current_user.get_id()).all()
            for inscription in inscriptions:
                inscription.inscription_evenement = "Payer"
                db.session.add(inscription)
                db.session.commit()
            return redirect('/paiement_confirmer')
        flash("Paiement non-accepter")
        return render_template("/festivalier/checkout.html", user=current_user)
    return render_template('/festivalier/checkout.html',
                           inscriptions=inscriptions,
                           events=events, prix_total=prix_total)


# Méthode qui confime le paiement du festivalier connecté pour les évènements dont il s'est inscrit
@event_festivalier.route('/paiement_confirmer', methods=['GET', 'POST'])
def paiement_confirmer():
    return render_template('/festivalier/confirmerPaiement.html', user=current_user)


@event_festivalier.route('/download_report')
def download_report():
    from_addr = 'equipe4.inm5001@gmail.com'
    to_addr = current_user.festivalier_email

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = 'Votre Horaire'

    text = "Voici l'horaire des evenement auxquels vous etes inscrit!!"

    html = """<h4>Mon horaire événementiel</h4><br>"""
    inscription = Inscription.query.filter(
        Inscription.id_festivalier == current_user.id).all()
    evenements = ""
    events = ""
    if inscription:
        evenements = Evenement.query.filter(
            Evenement.id == Inscription.evenement_id).all()
        if evenements:
            for evenement in evenements:
                event_name = evenement.name
                event_dae_debut = evenement.date_debut
                event_date_fin = evenement.date_fin
                events = events + """<div class="info-event">""" + """<h3><b>""" + event_name + """</b></h3>""" + "Date de debut : " + event_dae_debut.strftime(
                    '%m/%d/%Y') + "  -----  Date de fin :  " + event_date_fin.strftime('%m/%d/%Y') + """<img src=""" + evenement.image + """alt="event" class="w3-hover-opacity"></div><br>"""

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    part3 = MIMEText(events, 'html')
    msg.attach(part1)
    msg.attach(part2)
    msg.attach(part3)

    with smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT) as server:
        server.starttls()
        server.login('equipe4.inm5001@gmail.com', 'vudsxpyynviucpah')
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
    return redirect(url_for('event_festivalier.mes_event_festivalier'))

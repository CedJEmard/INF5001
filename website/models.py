from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Festivalier(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    festivalier_email = db.Column(db.String(150), unique=True)
    festivalier_password = db.Column(db.String(150))
    festivalier_name = db.Column(db.String(150))
    festivalier_prenom = db.Column(db.String(150))
    festivalier_telephone = db.Column(db.String(150))
    adresse_id = db.Column(db.Integer, db.ForeignKey('adresse.id'))
    inscription_id = db.relationship('Inscription')
    horaire_id = db.relationship('Horaire')


class Adresse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rue = db.Column(db.String(150))
    ville = db.Column(db.String(15))
    province = db.Column(db.String(15))
    pays = db.Column(db.String(15))
    codePostal = db.Column(db.String(15))
    noCivique = db.Column(db.String(10))
    id_festivalier = db.relationship('Festivalier')
    evenement_id = db.relationship('Evenement')


class Producteur(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    NEQ = db.Column(db.String(150))
    description = db.Column(db.String(500))
    telephone = db.Column(db.String(150))
    legitime = db.Column(db.Boolean)
    evenement_id = db.relationship('Evenement')


class Evenement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categorie = db.Column(db.String(150))
    name = db.Column(db.String(150))
    description = db.Column(db.String(500))
    date_debut = db.Column(db.Date)
    date_fin = db.Column(db.Date)
    prix = db.Column(db.Integer)
    image = db.Column(db.String(264), unique=True)
    nbBillets = db.Column(db.Integer)
    adresse_id = db.Column(db.Integer, db.ForeignKey('adresse.id'))
    producteur_id = db.Column(db.Integer, db.ForeignKey('producteur.id'))
    inscription_id = db.relationship('Inscription')


class Paiement(db.Model):
    paiement_montant = db.Column(db.Integer, primary_key=True)
    paiement_noCarte = db.Column(db.String(150))
    paiement_typeCarte = db.Column(db.String(15))
    paiement_banque = db.Column(db.String(15))
    paiement_accepte = db.Column(db.Boolean)
    inscription_id = db.Column(
        db.Integer, db.ForeignKey('inscription.inscription_id'))


class Inscription(db.Model):
    inscription_id = db.Column(db.Integer, primary_key=True)
    inscription_evenement = db.Column(db.String(150))
    inscrition_date = db.Column(db.Date)
    inscription_nb = db.Column(db.Integer)
    evenement_id = db.Column(db.Integer, db.ForeignKey('evenement.id'))
    id_festivalier = db.Column(db.Integer, db.ForeignKey('festivalier.id'))
    paiement_id = db.relationship('Paiement')


class Horaire(db.Model):
    horaire_id = db.Column(db.Integer, primary_key=True)
    horaire_statut = db.Column(db.String(10))
    id_festivalier = db.Column(db.Integer, db.ForeignKey('festivalier.id'))


class Categorie(db.Model):
    categorie_name = db.Column(db.String(150), primary_key=True)
    categorie_no = db.Column(db.Integer)

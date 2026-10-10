from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Festivalier(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    festivalier_email = db.Column(db.String(150), unique=True)
    festivalier_password = db.Column(db.String(150))
    festivalier_name = db.Column(db.String(150))
    festivalier_prenom = db.Column(db.String(150))
    festivalier_telephone = db.Column(db.String(150))
    adresse_id = db.Column(db.Integer, db.ForeignKey('adresse.adresse_id'))
    inscription_id = db.relationship('Inscription')
    horaire_id = db.relationship('Horaire')
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    
class Adresse(db.Model):
    adresse_id = db.Column(db.Integer, primary_key=True)
    adresse_rue = db.Column(db.String(150))
    adresse_ville = db.Column(db.String(15))
    adresse_province = db.Column(db.String(15))
    adresse_pays = db.Column(db.String(15))
    adresse_codePostal = db.Column(db.String(15))
    adresse_noCivique = db.Column(db.String(10))
    id_festivalier = db.relationship('Festivalier')
    evenement_id = db.relationship('Evenement')
    
class Producteur(db.Model):
    producteur_id = db.Column(db.Integer, primary_key=True)
    producteur_email = db.Column(db.String(150), unique=True)
    producteur_password = db.Column(db.String(150))
    producteur_name = db.Column(db.String(150))
    producteur_description = db.Column(db.String(500))
    producteur_telephone = db.Column(db.String(150))
    producteur_legitime = db.Column(db.Boolean)
    evenement_id = db.relationship('Evenement')
    
class Evenement(db.Model):
    evenement_id = db.Column(db.Integer, primary_key=True)
    evenement_categorie = db.Column(db.String(150))
    evenement_name = db.Column(db.String(150))
    evenement_description = db.Column(db.String(500))
    evenement_date = db.Column(db.Date)
    evenement_prix = db.Column(db.Integer)
    evenement_nbBillets = db.Column(db.Integer)
    adresse_id = db.Column(db.Integer, db.ForeignKey('adresse.adresse_id'))
    producteur_id = db.Column(db.Integer, db.ForeignKey('producteur.producteur_id'))
    inscription_id = db.relationship('Inscription')
    
class Paiement(db.Model):
    paiement_montant = db.Column(db.Integer, primary_key=True)
    paiement_noCarte = db.Column(db.String(150))
    paiement_typeCarte = db.Column(db.String(15))
    paiement_banque = db.Column(db.String(15))
    paiement_accepte = db.Column(db.Boolean)
    inscription_id = db.Column(db.Integer, db.ForeignKey('inscription.inscription_id'))
    
class Inscription(db.Model):
    inscription_id = db.Column(db.Integer, primary_key=True)
    inscription_evenement = db.Column(db.String(150))
    inscrition_date = db.Column(db.Date)
    inscription_nb = db.Column(db.Integer)
    evenement_id = db.Column(db.Integer, db.ForeignKey('evenement.evenement_id'))
    id_festivalier = db.Column(db.Integer, db.ForeignKey('festivalier.id'))
    paiement_id = db.relationship('Paiement')
    
class Horaire(db.Model):
    horaire_id = db.Column(db.Integer, primary_key=True)
    horaire_statut = db.Column(db.String(10))
    id_festivalier = db.Column(db.Integer, db.ForeignKey('festivalier.id'))
    
class Categorie(db.Model):
    categorie_name = db.Column(db.String(150), primary_key=True)
    categorie_no = db.Column(db.Integer)
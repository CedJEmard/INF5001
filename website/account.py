from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import Flask
from .models import Festivalier, Adresse, Producteur
from werkzeug.security import generate_password_hash
from . import db
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy

acc = Blueprint('acc', __name__)
app = Flask(__name__)


# Méthode pour afficher la page de profil d'un festivalier
@acc.route('/compte', methods=['GET', 'POST'])
def compte():
    adresse = (current_user.adresse_id)
    un_adresse = Adresse.query.get(adresse)
    postal = un_adresse.codePostal
    rue = un_adresse.rue
    ville = un_adresse.ville
    pays = un_adresse.pays
    no_civique = un_adresse.noCivique
    province = un_adresse.province
    return render_template('/festivalier/profile.html', user=current_user,
                           postal=postal, rue=rue, ville=ville, pays=pays,
                           no_civique=no_civique, province=province)


# Méthode pour afficher la page de modification du profil d'un festivalier
@acc.route('/profilemodif', methods=['GET', 'POST'])
def comptemodif():
    adresse = (current_user.adresse_id)
    un_adresse = Adresse.query.get(adresse)
    postal = un_adresse.codePostal
    rue = un_adresse.rue
    ville = un_adresse.ville
    pays = un_adresse.pays
    no_civique = un_adresse.noCivique
    province = un_adresse.province
    return render_template('/festivalier/modifier_profil.html', user=current_user,
                           postal=postal, rue=rue, ville=ville, pays=pays,
                           no_civique=no_civique, province=province)


# Méthode pour modifier les informations du profil d'un festivalier
@acc.route('/modifsave', methods=['GET', 'POST'])
def modifsave():
    modif_prenom = request.form['modif_prenom']
    modif_nom = request.form['modif_nom']
    modif_telephone = request.form['modif_telephone']
    modif_rue = request.form['modif_rue']
    modif_civique = request.form['modif_civique']
    modif_ville = request.form['modif_ville']
    modif_postal = request.form['modif_postal']
    modif_email = request.form['modif_email']
    passwordInput = request.form['passwordInput']
    reconfirmInput = request.form['reconfirmInput']
    modif_pays = request.form['modif_pays']
    modif_province = request.form['modif_province']

    festivalier = Festivalier.query.filter_by(
        festivalier_email=(current_user.festivalier_email)).first()

    error = False
    if (current_user.festivalier_email) != modif_email:
        user = Festivalier.query.filter_by(
            festivalier_email=modif_email).first()
        if user:
            flash('Email existe déjà.', category='error')
            error = True

    if len(modif_email) < 4:
        flash('Email doit avoir plus de 3 caractères.', category='error')
        error = True

    if len(modif_prenom) < 2:
        flash('Prénom doit être plus que 1 caractère.', category='error')
        error = True

    if passwordInput:
        if passwordInput != reconfirmInput:
            flash('Le password et la confirmation ne sont pas pareils.',
                  category='error')
            error = True
        if len(passwordInput) < 7:
            flash('Password doit avoir au moins 7 caractères.', category='error')
            error = True

    if not error:
        festivalier.festivalier_prenom = modif_prenom
        db.session.commit()
        festivalier.festivalier_name = modif_nom
        db.session.commit()
        festivalier.festivalier_telephone = modif_telephone
        db.session.commit()
        festivalier.festivalier_email = modif_email
        db.session.commit()

        if passwordInput:
            festivalier.festivalier_password = generate_password_hash(
                passwordInput, method='sha256')
            db.session.commit()

        current_address_id = current_user.adresse_id
        current_address = Adresse.query.get(current_address_id)

        current_address.rue = modif_rue
        db.session.commit()
        current_address.noCivique = modif_civique
        db.session.commit()
        current_address.ville = modif_ville
        db.session.commit()
        current_address.pays = modif_pays
        db.session.commit()
        current_address.province = modif_province
        db.session.commit()
        current_address.codePostal = modif_postal
        db.session.commit()
        flash('Sauvegarde reussi!', category='success')
        return redirect(url_for('acc.compte'))
    return render_template("/festivalier/modifier_profil.html", user=current_user)


# Méthode pour afficher la page de profil d'un producteur
@acc.route('/profil_prod', methods=['GET', 'POST'])
def profil_prod():
    return render_template('/producteur/prod_profil.html', user=current_user)


# Méthode pour afficher la page de modification du profil d'un producteur
@acc.route('/profil_prod_modif', methods=['GET', 'POST'])
def profil_modif_prod():
    return render_template('/producteur/prod_profil_modif.html', user=current_user)


# Méthode pour modifier les informations du profil d'un producteur
@acc.route('/modif_save_prod', methods=['GET', 'POST'])
def modif_save_prod():
    modif_name = request.form['modif_name']
    modif_neq = request.form['modif_neq']
    modif_description = request.form['modif_description']
    modif_email = request.form['modif_email']
    passwordInput = request.form['passwordInput']
    reconfirmInput = request.form['reconfirmInput']
    modif_telephone = request.form['modif_telephone']
    producteur = Producteur.query.filter_by(email=(current_user.email)).first()

    error = False
    if (current_user.email) != modif_email:
        user = Producteur.query.filter_by(email=(modif_email)).first()
        if user:
            flash('Email existe déjà.', category='error')
            error = True

    if len(modif_email) < 4:
        flash('Email plus de 3 caractères.', category='error')
        error = True
    if len(modif_neq) != 10:
        flash('NEQ doit être de 10 chiffres', category='error')
        error = True

    if passwordInput:
        if passwordInput != reconfirmInput:
            flash('Le password et la confirmation ne sont pas pareils',
                  category='error')
            error = True
        if len(passwordInput) < 7:
            flash('Password doit avoir au moins 7 caractères.', category='error')
            error = True

    if not error:
        producteur.name = modif_name
        db.session.commit()
        producteur.neq = modif_neq
        db.session.commit()
        producteur.description = modif_description
        db.session.commit()
        producteur.email = modif_email
        db.session.commit()

        if passwordInput:
            producteur.password = generate_password_hash(
                passwordInput, method='sha256')
            db.session.commit()

        producteur.telephone = modif_telephone
        db.session.commit()
        flash('Sauvegarde reussi!', category='success')
        return redirect(url_for('acc.profil_prod'))
    return render_template("/producteur/prod_profil_modif.html", user=current_user)

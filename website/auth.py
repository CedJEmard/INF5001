from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import Festivalier, Adresse, Producteur, Evenement
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  # means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
import requests


auth = Blueprint('auth', __name__)


# Méthode pour se connecter soit en tant que producteur ou festivalier
@auth.route('/connexion', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        connexion_email = request.form.get('email')
        password = request.form.get('password')
        prod_user = Producteur.query.filter_by(email=connexion_email).first()
        user = Festivalier.query.filter_by(
            festivalier_email=connexion_email).first()
        if user or prod_user:
            if connexion_email == "Admin@admin":
                if check_password_hash(user.festivalier_password, password):
                    login_user(user, remember=True)
                    return redirect(url_for('views.connectAdmin'))
                else:
                    flash('Mauvais mot de passe d\'Admin', category='error')
                    return render_template("connecion.thml", user=current_user)

            elif user and check_password_hash(user.festivalier_password, password):
                session['user_type'] = 'fes'
                login_user(user, remember=True)
                return redirect(url_for('views.home_co'))
            elif prod_user and check_password_hash(prod_user.password, password):
                session['user_type'] = 'prod'
                login_user(user=prod_user, remember=True)
                return redirect(url_for('event_producteur.producteur'))
            else:
                flash('Incorrect producteur password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("/no_co/connexion.html", user=current_user)


# Méthode pour créer un nouveau profil festivalier
@auth.route('/signup_fes', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        festivalier_email = request.form.get('festivalier_email')
        festivalier_prenom = request.form.get('festivalier_prenom')
        festivalier_name = request.form.get('festivalier_name')
        festivalier_telephone = request.form.get('festivalier_telephone')
        festivalier_password = request.form.get('festivalier_password')
        password2 = request.form.get('password2')
        noCiv = request.form.get('noCivique')
        rue = request.form.get('rue')
        codePostal = request.form.get('codePostal')
        ville = request.form.get('ville')
        pays = request.form.get('pays')
        province = request.form.get('province')
        user = Festivalier.query.filter_by(
            festivalier_email=festivalier_email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(festivalier_email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(festivalier_prenom) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif festivalier_password != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(festivalier_password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_adress = Adresse(rue=rue, pays=pays, ville=ville,
                                 province=province, noCivique=noCiv, codePostal=codePostal,)
            db.session.add(new_adress)
            db.session.commit()
            new_user = Festivalier(festivalier_email=festivalier_email,
                                   festivalier_password=generate_password_hash(
                                       festivalier_password, method='sha256'),
                                   festivalier_name=festivalier_name,
                                   festivalier_prenom=festivalier_prenom,
                                   festivalier_telephone=festivalier_telephone,
                                   adresse_id=new_adress.id)
            db.session.add(new_user)
            db.session.commit()
            login_user(user=new_user, remember=True)
            return redirect(url_for('views.home_co'))
    return render_template("/no_co/signup_fes.html", user=current_user)


# Méthode pour créer un nouveau profil producteur
@auth.route('/signup_prod', methods=['GET', 'POST'])
def sign_up_prod():
    if request.method == 'POST':
        email = request.form.get('email')
        description = request.form.get('description')
        name = request.form.get('name')
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        NEQ = request.form.get('NEQ')
        user = Producteur.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(NEQ) != 10:
            flash('NEQ doit etre de 10 chiffres', category='error')
        elif password != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = Producteur(email=email, password=generate_password_hash(
                password, method='sha256'), name=name, telephone=telephone, NEQ=NEQ,
                description=description, legitime=False)
            db.session.add(new_user)
            db.session.commit()
            login_user(user=new_user, remember=True)
            return redirect(url_for('event_producteur.producteur', user=current_user))
    return render_template("/no_co/signup_prod.html", user=current_user)


# Méthode pour se déconnecter en tant que producteur ou festivalier
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Festivalier, Adresse
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)



@auth.route('/connexion', methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        connexion_email = request.form.get('email')
        signup_email = request.form.get('festivalier_email')
        
        if signup_email is not None:
            festivalier_email = request.form.get('festivalier_email')
            festivalier_prenom = request.form.get('festivalier_prenom')
            festivalier_name = request.form.get('festivalier_name')
            festivalier_password = request.form.get('festivalier_password')
            user = Festivalier.query.filter_by(festivalier_email=festivalier_email).first()
            
            if user:
                flash('Email already exists.', category='error')
            elif len(festivalier_email) < 4:
                flash('Email must be greater than 3 characters.', category='error')
            elif len(festivalier_prenom) < 2:
                flash('First name must be greater than 1 character.', category='error')
            elif len(festivalier_password) < 7:
                flash('Password must be at least 7 characters.', category='error')
            else:
                
                
                #----------ajout dans la database-------------#
                
                new_adress = Adresse()
                db.session.add(new_adress)
                db.session.commit()
                
                
                new_user = Festivalier(festivalier_email=festivalier_email, festivalier_password=generate_password_hash(festivalier_password, method='sha256'), festivalier_name=festivalier_name, festivalier_prenom=festivalier_prenom,festivalier_telephone=0, adresse_id=new_adress.adresse_id)
                db.session.add(new_user)
                db.session.commit()
                
                #------------------^^^^^^^^^------------------#
                
                login_user(new_user, remember=True)
                
                flash('Account created!', category='success')
                
                
            return redirect('/connexion')
                    
        elif connexion_email is not None:
            password = request.form.get('password')    
            user=Festivalier.query.filter_by(festivalier_email=connexion_email).first()
                
            if user:    
                
                if check_password_hash(user.festivalier_password, password):
                    login_user(user, remember=True)
                    return redirect(url_for('views.connect'))
                else:
                    flash('Incorrect password, try again.', category='error')
                    
            else:
                flash('Email does not exist.', category='error')     
                
        else:
            return render_template("connexion.html", user=current_user)
        
    return render_template("connexion.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, current_user

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .event_in import event_in
    from .event_festivalier import event_festivalier
    from .event_producteur import event_producteur
    from .account import acc
    from .full_calendar import fcal

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(event_in, url_prefix='/')
    app.register_blueprint(event_festivalier, url_prefix='/')
    app.register_blueprint(event_producteur, url_prefix='/')
    app.register_blueprint(acc, url_prefix='/')
    app.register_blueprint(fcal, url_prefix='/')

    from .models import Festivalier, Adresse, Evenement, Producteur, Paiement, Inscription, Horaire, Categorie

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @app.context_processor
    def connect():
        inscriptions = ""
        events = ""
        prix_total = 0
        if current_user:
            inscriptions = Inscription.query.filter_by(
                inscription_evenement="Panier", id_festivalier=current_user.get_id()).all()
            events = Evenement.query.all()
            for inscription in inscriptions:
                for event in events:
                    billet = event.prix
                    qte = inscription.inscription_nb
                    if inscription.evenement_id == event.id:
                        if qte:
                            prix_total = prix_total + (billet*qte)
        return dict(inscriptions=inscriptions, events=events, prix_total=prix_total)

    @login_manager.user_loader
    def load_user(id):
        record = ""
        if 'user_type' in session:
            if session["user_type"] == "fes":
                record = Festivalier.query.get(int(id))
            elif session["user_type"] == "prod":
                record = Producteur.query.get(int(id))
        return record
    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

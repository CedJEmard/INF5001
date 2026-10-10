CREATE TABLE adresse (
    adresse_id integer primary key,
    adresse_noCivique VARCHAR(10),
    adresse_rue VARCHAR(15),
    adresse_ville VARCHAR(15),
    adresse_province VARCHAR(15),
    adresse_pays VARCHAR(15),
    adresse_codePostal VARCHAR(10)
);

CREATE TABLE Festivalier (
    festivalier_id integer primary key,
    festivalier_nom VARCHAR(15),
    festivalier_prenom VARCHAR(15),
    festivalier_courriel VARCHAR(50),
    festivalier_motDePasse VARCHAR(15),
    festivalier_telephone VARCHAR(15),
    adresse_id integer,
    FOREIGN KEY (adresse_id) REFERENCES adresse(adresse_id)
);

CREATE TABLE Producteur (
    producteur_id integer primary key,
    producteur_nom VARCHAR(15),
    producteur_description VARCHAR(150),
    producteur_courriel VARCHAR(50),
    producteur_motDePasse VARCHAR(15),
    producteur_telephone VARCHAR(15),
    producteur_legitime bit
);

CREATE TABLE Evenement (
    evenement_id integer primary key,
    evenement_nom VARCHAR(150),
    evenement_date DATE,
    evenement_description VARCHAR(250),
    evenement_categorie VARCHAR(15),
    evenement_prix INTEGER,
    evenement_billets INTEGER,
    adresse_id integer,
    producteur_id integer,
    FOREIGN KEY (adresse_id) REFERENCES adresse(adresse_id),
    FOREIGN KEY (producteur_id) REFERENCES Producteur(producteur_id)
);

CREATE TABLE Paiement (
    paiement_montant numeric(8,2),
    paiement_noCarte VARCHAR(15),
    paiement_typeCarte VARCHAR(15),
    paiement_banque VARCHAR(10),
    paiement_accepte bit
);

CREATE TABLE Inscription (
    inscription_id integer primary key,
    inscription_evenement VARCHAR(15),
    inscription_date DATE,
    inscription_nb integer,
    evenement_id integer,
    festivalier_id integer,
    FOREIGN KEY (evenement_id) REFERENCES Evenement(evenement_id),
    FOREIGN KEY (festivalier_id) REFERENCES Festivalier(festivalier_id)
);

CREATE TABLE Horaire (
    horaire_id integer primary key,
    horaire_statut VARCHAR(10),
    festivalier_id integer,
    FOREIGN KEY (festivalier_id) REFERENCES Festivalier(festivalier_id)
);


CREATE TABLE Horaire_Inscription (
    inscription_id integer,
    horaire_id integer,
    FOREIGN KEY (inscription_id) REFERENCES Inscription(inscription_id),
    FOREIGN KEY (horaire_id) REFERENCES Horaire(horaire_id)
);


CREATE TABLE Horaire_Evenement (
    evenement_id integer,
    horaire_id integer,
    FOREIGN KEY (evenement_id) REFERENCES Evenement(evenement_id),
    FOREIGN KEY (horaire_id) REFERENCES Horaire(horaire_id)
);


CREATE TABLE Categorie (
    categorie_nom VARCHAR(15) primary key,
    categorie_no integer
);

CREATE TABLE Categorie_Evenement (
    categorie_nom VARCHAR(15),
    evenement_id integer,
    FOREIGN KEY (categorie_nom) REFERENCES Categorie(categorie_nom),
    FOREIGN KEY (evenement_id) REFERENCES Evenement(evenement_id)
);

INSERT INTO Evenement (evenement_nom, evenement_date, evenement_description, evenement_categorie,
evenement_prix, evenement_billets)
VALUES ('DISNEYS ALADDIN', '2023-03-29','ALADDIN, La comédie musicale à succès de broadway',
'enfant', '100.75','50');
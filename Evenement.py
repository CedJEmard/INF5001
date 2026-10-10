class Evenement:
    def __init__(self, id, nom, date, description,
                 categorie, prix, billets):
        self.id = id
        self.nom = nom
        self.date = date
        self.description = description
        self.categorie = categorie
        self.prix = prix
        self.billets = billets
        

    def info_complete_dec(self):
        return {
            'id': self.id,
            'Nom': self.nom,
            'date': self.date,
            'description': self.description,
            'categorie': self.categorie,
            'prix': self.prix,
            'billets': self.billets,
        }



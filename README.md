### UQÀM - INM5001 - Hiver 2023 - équipe 4
# *Horaire Festif*


## Auteurs
Cédric Jutras-Émard - JUTC09079403 

Louis De L'Étoile-Damour - DELL22049808 

Zineb Ben Larabi – BENZ21519706 

Julie Delisle - DELJ14558108

Hourk Sheng Tang - TANH13049700


## Identification du projet
Projet informatique réalisé pour le cours INM5001-Atelier, livré au professeur Vladimir Makarenkov et Achraf Bouaoune, notre client et responsable de projet.

Nous avons développé une application qui permettra: 

* D’assister les utilisateurs dans l’organisation des événements festivaliers
* De permettre aux producteurs d’événements d’ajouter/présenter leur nouvelle représentation
* De visualiser les événements courants et à venir au grand public.

### Mandat
 « Le Ministère de la Culture et des Communications souhaite la création d’une plateforme qui permettra de regrouper les divers festivals au Québec et offrirait à la population une meilleure gestion d’horaire des festivaliers »

### Objectifs du projet 
* Simplifier l'organisation des événements en assistant l'utilisateur dans la création d'un horaire flexible selon leurs intérêts 
* Présenter plusieurs choix d'événements 
* Simplifier la recherche d’événement selon différents critères de recherches
* Plateforme gratuite 
* Il peut télécharger en format PDF ou envoyer par courriel son horaire

### Fonctionnalités
* Inscription sur le site web pour une expérience personnalisé 
* Affichage de tous les événements disponibles 
* Affichage de tous les événements disponibles sous forme de calendrier
* Affichage de tous les événements dont le producteur a créé
* Recherche des événements par catégorie, par mots-clés, par ville et nom.
* Envoi de l’horaire par courriel et téléchargement par PDF
* Ajout d'événements par organisateurs (donc deux types de profil d’utilisateurs à l’inscription : « simple » pour les utilisateurs normaux mentionnés précédemment ou « organisateur » qui auront des options différentes telles que « créer un événement », « modifier un événement », « supprimer un événement ») 
* Ajouter un événement au calendrier de l’utilisateur 


## Installation et fonctionnement

D'abord il faut avoir la dernière version de Python, Flask installé:

Windows:
```bash
pip install -r requirements.txt
```

ios mac:
```bash
python3 -m pip install -r requirements.txt
```

Ensuite pour être en mesure de télécharger les événements en format PDF, il faut installer la dépendance *GTK*: 

https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases


Pour finir il faut cloner le projet :

```bash
git clone https://github.com/Juli3D3lisl3/INM5001_equipe4.git
```

## Exécution

Pour exécuter le projet:

```bash
python main.py
```

Suite à l'exécution, pour l'affichage du site web aller sur:

http://127.0.0.1:5000

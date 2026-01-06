# Weather ChatBot
Un assistant météo intelligent développé en Python avec Tkinter & l’API OpenWeather

# Description

Weather ChatBot est une application Python permettant d’interagir avec un chatbot météo capable de comprendre le langage naturel.

Elle fournit :
- la météo actuelle
- la météo de demain
- la météo dans X heures
- la température
- la pression (QNH)
- le vent
- l'humidité

Le tout via une interface graphique moderne réalisée avec CustomTkinter.

# Fonctionnalités principales
<ins> Compréhension du langage naturel </ins>

Le chatbot analyse les messages de l’utilisateur pour détecter :

- la ville

- le type d’information demandé

- le moment dans le temps (maintenant, demain, dans Xh)

<ins> Données météo en temps réel </ins>

Connecté à l’API OpenWeatherMap, il récupère :

- conditions météo

- température

- vent

- humidité

- pression (QNH)

<ins> Conversation enregistrée </ins>

  Toutes les interactions sont sauvegardées dans un fichier texte : "conversation_history_ChatBot_Meteo.txt"

<ins> Interface graphique moderne </ins>

- Mode clair/sombre

- Zone d’historique

- Champ de saisie

- Bouton envoyer

- Bouton effacer l’historique

# Structure du projet
ChatBot-Meteo/

│

├── assets/                   # Dossier photos

│

├── main.py     # Script principal (interface + chatbot)

├── conversation_history_ChatBot_Meteo.txt

│

├── requirements.txt          # Bibliothèques nécessaires

│

└── README.md                 # Ce fichier

# Installation
1️ Cloner le projet
git clone https://github.com/CodeRunner85/weather-chatbot.git
cd weather-chatbot

2️ Installer les dépendances
pip install -r requirements.txt

3️ Ajouter ta clé API OpenWeather

Dans le fichier main.py, remplace :
API_KEY = "VOTRE CLE API"
par ta clé réelle.

Lancer l’application
python main.py

#

Fichier requirements.txt recommandé !

# Technologies utilisées

Python 3

CustomTkinter pour l’interface GUI

Requests pour les appels à l’API météo

OpenWeatherMap API

Regex pour la compréhension utilisateur

# Objectif du projet

Ce projet fait partie d’un parcours d’apprentissage visant à :

- maîtriser Python

- utiliser des APIs

- construire une interface graphique

- structurer un projet réel

- publier du code sur GitHub

# Auteur

Antoine (CodeRunner85)
Développeur en formation & futur entrepreneur dans l’IA et les logiciels d’automatisation.

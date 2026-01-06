# -*- coding: utf-8 -*-
"""
Created on Thu Jan  1 17:31:33 2026

@author: Antoine
"""

import customtkinter as ctk
import requests
import re
import os
from tkinter import messagebox
from datetime import datetime, timedelta

API_KEY="VOTRE CLE ICI" #inserer votre cle  API OpenWeather ici
    
#------------------------------------------- Enregistrement de la conversation ----------------------------------------

#fonction qui enregistre la conversation

def save_to_history(sender, message):
    with open("conversation_history_ChatBot_Meteo.txt", "a", encoding="utf-8") as f:
        f.write(f"{sender} : {message}\n")
        
#fonction qui charge le fichier
        
def load_history():
    try:
        with open("conversation_history_ChatBot_Meteo.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""
    
#fonction qui supprime l'historique

def clear_history():
    if messagebox.askyesno("Confirmation", "Voulez-vous vraiment effacer l'historique ?"):
        if os.path.exists("conversation_history_ChatBot_Meteo.txt"):
            os.remove("conversation_history_ChatBot_Meteo.txt")

        chat_history.configure(state="normal")
        chat_history.delete("1.0", "end")
        chat_history.configure(state="disabled")
    
#---------------------------------------------- Comprehension de la demande -------------------------------------------

#fonction qui recherche la ville demande dans le text

def detect_city(text):
    villes = ["Paris", "Lyon", "Marseille", "Toulouse", "Bordeaux", "Lille", "Nice", "Nantes"]
    for ville in villes:
        if ville.lower() in text.lower():
            return ville
    return None

#fonction qui comprend la demande

def detect_request_type(text):
    text = text.lower()
    if "meteo" in text or "météo" in text or "temps" in text:
        return "description"
    if "temp" in text:
        return "temperature"
    if "qnh" in text or "pression" in text:
        return "pressure"
    if "vent" in text:
        return "wind"
    if "humid" in text:
        return "humidity"
    return "description"

#fonction qui comprend l'heure souhaite

def detect_time(text):
    text = text.lower()

    if "maintenant" in text or "actuel" in text or "actuelle" in text:
        return "now"

    if "demain" in text:
        return "tomorrow"

    m = re.search(r"dans (\d+)h", text)
    if m:
        return int(m.group(1))

    return "now"  # par défaut
    
#-------------------------------------------- Utilisation de l'API ----------------------------------------------------
    
#utilisation de l'api maintenant

def get_weather_now(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "fr"
    }
    r = requests.get(url, params=params).json()
    return r

#utilisation de l'API pour le temps a venir

def get_weather_forecast(city):
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "fr"
    }
    r = requests.get(url, params=params).json()
    return r

#------------------------------------------- Utilisation du chatbot ---------------------------------------------------

#fonction de reponse du chatbot

def chatbot_response(user_input):

    city = detect_city(user_input)
    if not city:
        return "Merci d’indiquer une ville."

    info = detect_request_type(user_input)
    time_req = detect_time(user_input)

    #METEO ACTUELLE
    
    if time_req == "now":
        data = get_weather_now(city)

    #DEMAIN
    
    elif time_req == "tomorrow":
        data_all = get_weather_forecast(city)
        target_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        data = next((item for item in data_all["list"] if target_date in item["dt_txt"]), None)

        if not data:
            return "Impossible de trouver la météo de demain."

    #DANS X HEURES
    
    elif isinstance(time_req, int):
        data_all = get_weather_forecast(city)
        target_time = datetime.now() + timedelta(hours=time_req)
        closest = min(data_all["list"], key=lambda item: abs(datetime.fromtimestamp(item["dt"]) - target_time))
        data = closest

    else:
        return "Erreur dans l’analyse du moment demandé."

    #------------------------------------------- Extraction des infos -------------------------------------------------

    main = data["main"]
    wind = data.get("wind", {})
    weather_desc = data["weather"][0]["description"]

    if info == "temperature":
        return f"La température à {city} est de {main['temp']}°C."

    if info == "pressure":
        return f"Le QNH (pression) à {city} est de {main['pressure']} hPa."

    if info == "wind":
        return f"Le vent souffle à {wind.get('speed', 0)} m/s à {city}."

    if info == "humidity":
        return f"L'humidité à {city} est de {main['humidity']}%."

    return f"Météo à {city} : {weather_desc}, {main['temp']}°C."

#----------------------------------------------- Interface Custom Tkinter ---------------------------------------------

#fonction pour gerer l'envoie du message

def send_message(event=None):
    user_message = user_input.get()
    if user_message.strip() != "":
        chat_history.configure(state="normal")
        chat_history.insert("end", f"Vous : {user_message}\n", "user")
        save_to_history("Vous", user_message)
        bot_response = chatbot_response(user_message)
        chat_history.insert("end", f"ChatBot : {bot_response}\n", "bot")
        save_to_history("ChatBot", bot_response)
        chat_history.configure(state="disabled")
        chat_history.see("end")
        user_input.delete(0, "end")

#interface du chat bot

app = ctk.CTk()
app.geometry("500x600")
app.title("ChatBot Meteo")

#en-tete

header = ctk.CTkLabel(app, text="Bienvenue sur ChatBot Meteo", font=("Arial",16))
header.pack(pady=10)

#affichage messages

chat_history = ctk.CTkTextbox(app, height=400, state="disabled" )
chat_history.tag_config("user", foreground="lightblue")
chat_history.tag_config("bot", foreground="lightgreen")
chat_history.pack(pady=10, padx=10, fill="both", expand = True)
chat_history.configure(font=("Arial", 16))

#champ de saisie

user_input_frame = ctk.CTkFrame(app)
user_input_frame.pack(pady=10, padx=10, fill="x")

user_input = ctk.CTkEntry(user_input_frame, placeholder_text="Entrez votre question ici ...", width=250)
user_input.pack(side="left")

send_button = ctk.CTkButton(user_input_frame, text="envoyer", command=send_message, width=100)
send_button.pack(side="left", padx=5)

clear_history_button = ctk.CTkButton(user_input_frame, text="effacer l'historique",command=clear_history, fg_color="red")
clear_history_button.pack(side="left")

#associer la touche Enter pour envoyer le message

app.bind("<Return>", send_message)

#chargement de l'historique

history = load_history()
chat_history.configure(state="normal")
for line in history.split("\n"):
    if line.strip() == "":
        continue

    if line.startswith("Vous :"):
        chat_history.insert("end", line + "\n", "user")
    elif line.startswith("ChatBot :"):
        chat_history.insert("end", line + "\n", "bot")
    else:
        chat_history.insert("end", line + "\n")  # au cas où

chat_history.configure(state="disabled")

#lancement de l'application

app.mainloop()

# 🏨 Assistant Hôtel AI

Un projet complet de gestion hôtelière avec **IA conversationnelle**, tableau de bord interactif et CRUD pour la gestion des données.

---

## 🔹 Description

Ce projet combine **LangChain**, **SQLite**, et Python pour créer une application qui permet de :  

- Répondre aux questions sur les clients, chambres, réservations et paiements via un **assistant IA**.  
- Gérer les données hôtelières avec un **CRUD complet** pour clients, chambres, réservations et employés.  
- Suivre les KPIs clés avec un **dashboard interactif**.  
- Accéder à l’application via un **login admin sécurisé**.  

L’objectif est de **faciliter la gestion et l’analyse des données hôtelières** grâce à une interface conviviale et une IA conversationnelle.

---

## 🔹 Technologies utilisées

- **Python 3.10+**  
- **LangChain** (IA conversationnelle)  
- **SQLite** (base de données)  
- **Pandas** (manipulation des données)  
- **Tabulate** (affichage des tableaux)  
- **Flask** (optionnel pour interface web)  
- **Plotly** (visualisation des dashboards)  
- **Faker** (données de test)  

---


## 🔹 Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/tonusername/hotel_ai.git
cd hotel_ai
Créer un environnement virtuel (optionnel mais recommandé) :


python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
Installer les dépendances :


pip install -r requirements.txt
Placer les fichiers CSV dans le dossier data/ :
clients.csv, chambres.csv, reservations.csv, paiements.csv, employes.csv

---

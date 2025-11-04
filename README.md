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
##🔹 Utilisation
Lancer le projet avec Python :


python app.py
L’IA sera prête à répondre aux questions sur les données hôtelières.

Tapez exit ou quit pour fermer l’application.

Pour les fonctionnalités CRUD et dashboard, ouvrir l’interface web (si Flask intégré).

🔹 Exemple de questions pour l’IA
Combien de chambres sont disponibles ?

Montant total payé par le client Jean Dupont.

Liste des employés avec leur poste et salaire.

Statistiques des réservations par mois.

🔹 Fonctionnalités
✅ Assistant IA avec LangChain

✅ Gestion complète des clients, chambres, réservations, paiements et employés

✅ Dashboard pour visualiser les KPIs

✅ Login admin sécurisé

✅ Données importables via CSV

🔹 Auteur
Nawres Tlili

LinkedIn : https://www.linkedin.com/in/nawres-tlili/

Email : tlilinawres207@gmail.com






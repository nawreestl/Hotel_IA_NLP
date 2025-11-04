import pandas as pd
from langchain.chat_models import Ollama
from langchain.schema import HumanMessage

# Lecture des CSV
clients = pd.read_csv("data/clients.csv")
chambres = pd.read_csv("data/chambres.csv")
reservations = pd.read_csv("data/reservations.csv")
paiements = pd.read_csv("data/paiements.csv")
employes = pd.read_csv("data/employes.csv")

# Fonctions pour questions simples
def nb_chambres_libres():
    count = len(chambres[chambres["statut"] == "Libre"])
    return f"Il y a {count} chambres libres actuellement."

def total_depense_client(client_id):
    res = reservations[reservations["client_id"] == client_id]
    total = res["total"].sum()
    return f"Le client {client_id} a dépensé au total {total}€."

def liste_clients_fideles(min_total=1000):
    depenses = reservations.groupby("client_id")["total"].sum()
    fideles = depenses[depenses >= min_total].index.tolist()
    noms = clients[clients["id"].isin(fideles)]["nom"].tolist()
    return f"Clients fidèles (dépenses ≥ {min_total}€) : {', '.join(noms)}"

# LLM Ollama local
llm = Ollama(
    model="llama3",  # ou le modèle local installé
    temperature=0.2
)

# Fonction principale de l'agent
def run_agent(question: str):
    q = question.lower()
    
    if "chambres libres" in q:
        return nb_chambres_libres()
    elif "dépensé" in q:
        try:
            client_id = int(''.join(filter(str.isdigit, question)))
            return total_depense_client(client_id)
        except:
            return "Merci de préciser l'id du client (ex: client 5)."
    elif "clients fidèles" in q or "fidèles" in q:
        return liste_clients_fideles()
    else:
        response = llm([HumanMessage(content=question)])
        return response.content

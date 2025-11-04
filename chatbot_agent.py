import sqlite3
import pandas as pd
from tabulate import tabulate
from langchain_ollama import OllamaLLM
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain.agents import AgentType

# ---------------------------
# ✅ Initialisation de la base de données
# ---------------------------
def init_db():
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    # Création des tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY,
            nom TEXT,
            email TEXT,
            telephone TEXT,
            pays TEXT,
            date_inscription TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chambres (
            id INTEGER PRIMARY KEY,
            numero INTEGER,
            type TEXT,
            prix_nuit REAL,
            statut TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY,
            client_id INTEGER,
            chambre_id INTEGER,
            date_debut TEXT,
            date_fin TEXT,
            total REAL,
            statut TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paiements (
            id INTEGER PRIMARY KEY,
            reservation_id INTEGER,
            montant REAL,
            mode_paiement TEXT,
            date_paiement TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employes (
            id INTEGER PRIMARY KEY,
            nom TEXT,
            poste TEXT,
            salaire REAL,
            date_embauche TEXT
        )
    """)

    # Import des CSV si vide
    count = cursor.execute("SELECT COUNT(*) FROM clients").fetchone()[0]
    if count == 0:
        print("📥 Importation des données depuis /data ...")
        clients = pd.read_csv("data/clients.csv")
        chambres = pd.read_csv("data/chambres.csv")
        reservations = pd.read_csv("data/reservations.csv")
        paiements = pd.read_csv("data/paiements.csv")
        employes = pd.read_csv("data/employes.csv")

        clients.to_sql("clients", conn, if_exists="append", index=False)
        chambres.to_sql("chambres", conn, if_exists="append", index=False)
        reservations.to_sql("reservations", conn, if_exists="append", index=False)
        paiements.to_sql("paiements", conn, if_exists="append", index=False)
        employes.to_sql("employes", conn, if_exists="append", index=False)

        print("✅ Données chargées dans hotel.db")

    conn.commit()
    conn.close()

# ---------------------------
# ✅ Création des agents
# ---------------------------
db = SQLDatabase.from_uri("sqlite:///hotel.db")
llm = OllamaLLM(model="llama3")

sql_agent = create_sql_agent(
    llm=llm,
    db=db,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)

# ---------------------------
# ✅ Fonction principale intelligente
# ---------------------------
def run_agent(question: str):
    sql_keywords = [
        "chambre", "client", "réservation", "paiement", "employé",
        "prix", "date", "total", "statut", "nombre", "combien"
    ]

    question_lower = question.lower()
    is_sql = any(word in question_lower for word in sql_keywords)

    try:
        if is_sql:
            print("🧠 Mode SQL activé...")
            result = sql_agent.invoke({"input": question})
            output = result.get("output", "")

            if isinstance(output, (list, tuple)):
                if len(output) == 1 and isinstance(output[0], (int, float)):
                    return f"📊 Résultat : {output[0]}"
                elif len(output) > 0 and isinstance(output[0], (list, tuple)):
                    df = pd.DataFrame(output)
                    return tabulate(df, headers="keys", tablefmt="grid", showindex=False)
                else:
                    return str(output)
            elif isinstance(output, pd.DataFrame):
                return tabulate(output, headers="keys", tablefmt="grid", showindex=False)
            elif isinstance(output, str):
                return output
            else:
                return f"🧩 Résultat : {output}"

        else:
            print("💬 Mode conversation activé...")
            response = llm.invoke(question)  # correction ici
            return str(response)

    except Exception as e:
        return f"❌ Erreur : {e}"

# ---------------------------
# ✅ Lancement auto
# ---------------------------
if __name__ == "__main__":
    init_db()
    print("🏨 Assistant Hôtel AI prêt à répondre aux questions !")

    while True:
        question = input("\n🗨️  Pose ta question : ")
        if question.lower() in ["exit", "quit"]:
            print("👋 Au revoir !")
            break
        print(run_agent(question))

import sqlite3

def init_users():
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    # Création de la table users si elle n'existe pas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE,
            password TEXT
        )
    """)

    # Ajouter un utilisateur admin par défaut
    cursor.execute("""
        INSERT OR IGNORE INTO users (email, password) 
        VALUES ('admin@hotel.com', 'admin123')
    """)

    conn.commit()
    conn.close()
    print("✅ Table users initialisée avec l'admin par défaut.")

if __name__ == "__main__":
    init_users()

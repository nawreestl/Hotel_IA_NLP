from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import pandas as pd
from chatbot_agent import run_agent  # gestion du bot

app = Flask(__name__)
app.secret_key = "secret123"

# ----------------- PAGE D’ACCUEIL -----------------
@app.route("/")
def index():
    return render_template("index.html")

# ----------------- LOGIN -----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if email == "admin@hotel.com" and password == "admin":
            session["admin"] = True
            return redirect(url_for("dashboard"))
        else:
            error = "❌ Email ou mot de passe incorrect."
    return render_template("login.html", error=error)

# ----------------- LOGOUT -----------------
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("index"))

# ----------------- DASHBOARD -----------------
@app.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect(url_for("login"))
    return render_template("dashboard.html")

# ----------------- CHATBOT -----------------
@app.route("/chatbot")
def chatbot():
    if not session.get("admin"):
        return redirect(url_for("login"))
    return render_template("chatbot.html")

@app.route("/ask", methods=["POST"])
def ask():
    if not session.get("admin"):
        return jsonify({"answer": "⚠️ Non autorisé"})
    data = request.get_json()
    question = data.get("question", "")
    answer = run_agent(question)
    return jsonify({"answer": answer})

# ----------------- CRUD -----------------
@app.route("/crud")
def crud():
    if not session.get("admin"):
        return redirect(url_for("login"))

    conn = sqlite3.connect("hotel.db")
    data = {}
    try:
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in c.fetchall()]
        for table in tables:
            df = pd.read_sql(f"SELECT * FROM {table}", conn)
            data[table] = df.to_dict(orient="records")
    finally:
        conn.close()

    return render_template("crud.html", data=data)

@app.route("/crud/form", methods=["GET","POST"])
def crud_form():
    if not session.get("admin"):
        return redirect(url_for("login"))

    table = request.args.get("table")
    record_id = request.args.get("id")
    conn = sqlite3.connect("hotel.db")
    c = conn.cursor()
    record = {}
    try:
        c.execute(f"PRAGMA table_info({table})")
        columns = [col[1] for col in c.fetchall()]

        if record_id:
            df = pd.read_sql(f"SELECT * FROM {table} WHERE id={record_id}", conn)
            if not df.empty:
                record = df.to_dict(orient="records")[0]

        if request.method == "POST":
            values = {col: request.form.get(col) for col in columns if col != "id"}
            if record_id:
                set_str = ", ".join([f"{k}=?" for k in values.keys()])
                c.execute(f"UPDATE {table} SET {set_str} WHERE id=?", (*values.values(), record_id))
            else:
                cols_str = ", ".join(values.keys())
                placeholders = ", ".join(["?"]*len(values))
                c.execute(f"INSERT INTO {table} ({cols_str}) VALUES ({placeholders})", tuple(values.values()))
            conn.commit()
            return redirect(url_for("crud"))
    finally:
        conn.close()

    return render_template("crud_form.html", table=table, columns=columns, record=record)

@app.route("/crud/delete/<table>/<int:record_id>")
def crud_delete(table, record_id):
    if not session.get("admin"):
        return redirect(url_for("login"))
    conn = sqlite3.connect("hotel.db")
    try:
        conn.execute(f"DELETE FROM {table} WHERE id = ?", (record_id,))
        conn.commit()
    finally:
        conn.close()
    return redirect(url_for("crud"))

# ----------------- API STATS -----------------
@app.route("/api/stats")
def api_stats():
    if not session.get("admin"):
        return jsonify({})

    try:
        conn = sqlite3.connect("hotel.db")
        df_clients = pd.read_sql("SELECT * FROM clients", conn)
        df_chambres = pd.read_sql("SELECT * FROM chambres", conn)
        df_reservations = pd.read_sql("SELECT * FROM reservations", conn)
        df_paiements = pd.read_sql("SELECT * FROM paiements", conn)
    except Exception:
        return jsonify({})
    finally:
        conn.close()

    # === Calculs ===
    nb_clients = len(df_clients)
    nb_chambres = len(df_chambres)
    nb_reservations = len(df_reservations)
    total_paiements = float(round(df_paiements["montant"].sum(), 2)) if not df_paiements.empty else 0.0

    nb_libres = len(df_chambres[df_chambres["statut"].str.lower() == "libre"]) if "statut" in df_chambres.columns else 0
    taux_occupation = round(((nb_chambres - nb_libres) / nb_chambres) * 100, 2) if nb_chambres > 0 else 0.0

    # Réservations par mois
    reservations_par_mois = {}
    if "date_debut" in df_reservations.columns:
        df_reservations["date_debut"] = pd.to_datetime(df_reservations["date_debut"], errors="coerce")
        df_reservations["mois"] = df_reservations["date_debut"].dt.strftime("%Y-%m")
        reservations_par_mois = df_reservations["mois"].value_counts().sort_index().to_dict()

    # Revenu par mois
    revenu_par_mois = {}
    if "date_paiement" in df_paiements.columns:
        df_paiements["date_paiement"] = pd.to_datetime(df_paiements["date_paiement"], errors="coerce")
        df_paiements["mois"] = df_paiements["date_paiement"].dt.strftime("%Y-%m")
        revenu_par_mois = df_paiements.groupby("mois")["montant"].sum().round(2).to_dict()

    # Top pays
    top_pays = df_clients["pays"].fillna("Inconnu").astype(str).value_counts().head(5).to_dict() if "pays" in df_clients.columns else {}

    stats = {
        "clients": nb_clients,
        "chambres": nb_chambres,
        "reservations": nb_reservations,
        "paiements": total_paiements,
        "taux_occupation": taux_occupation,
        "reservations_par_mois": reservations_par_mois,
        "revenu_par_mois": revenu_par_mois,
        "top_pays": top_pays
    }

    return jsonify(stats)

# ----------------- LANCEMENT -----------------
if __name__ == "__main__":
    app.run(debug=True)

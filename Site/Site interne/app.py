from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key")
app.debug = True

# Configuration de la base de données PostgreSQL
DB_HOST = os.environ.get("POSTGRES_HOST", "localhost")
DB_NAME = os.environ.get("POSTGRES_DB", "ramba")
DB_USER = os.environ.get("POSTGRES_USER", "postgres")
DB_PASS = os.environ.get("POSTGRES_PASSWORD", "postgres")

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    # Crée la table users si elle n'existe pas
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(150) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );
    """)
    # Vérifie si l'utilisateur admin existe, sinon le crée
    cur.execute("SELECT * FROM users WHERE username = %s;", ('admin',))
    if not cur.fetchone():
        hashed = generate_password_hash('progtr09')
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s);", ('admin', hashed))
    conn.commit()
    cur.close()
    conn.close()

@app.before_first_request
def before_first_request():
    init_db()

@app.route('/', methods=['GET'])
def index():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password FROM users WHERE username = %s;", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect.", "danger")
    return render_template('portail.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

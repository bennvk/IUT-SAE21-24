from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash
import threading
import json
import base64
import paho.mqtt.client as mqtt

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key")
app.debug = True

# --- DATABASE CONFIG ---
DB_HOST = os.environ.get("POSTGRES_HOST", "site_interne_db")
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
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(150) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );
    """)
    cur.execute("SELECT * FROM users WHERE username = %s;", ('admin',))
    if not cur.fetchone():
        hashed = generate_password_hash('progtr09')
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s);", ('admin', hashed))
    conn.commit()
    cur.close()
    conn.close()

@app.before_request
def before_request():
    if not hasattr(app, 'db_initialized'):
        init_db()
        app.db_initialized = True

# --- LORA DATA PART ---
latest_payload = {}

def decode_lora(latest_payload):
    data_field = latest_payload.get("data")
    temperature = None
    humidity = None
    if data_field:
        try:
            decoded = base64.b64decode(data_field)
            print("Décodé brute:", decoded)
            if len(decoded) >= 4:
                temp_raw = int.from_bytes(decoded[0:2], byteorder='big')
                temperature = temp_raw / 100.0
                hum_raw = int.from_bytes(decoded[2:4], byteorder='big')
                humidity = hum_raw / 100.0
                print(f"Temp: {temperature} ; Hum: {humidity}")
            else:
                print(f"Décodage trop court: {decoded}")
        except Exception as e:
            print("❌ Erreur lors du décodage des données :", e)
    return temperature, humidity

@app.route('/', methods=['GET'])
def index():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    temp, hum = decode_lora(latest_payload)
    return render_template('index.html', temp=temp, hum=hum, raw=latest_payload)

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

# --- MQTT PART ---
def on_connect(client, userdata, flags, rc):
    print("✅ Connecté au broker MQTT avec code:", rc)
    client.subscribe("application/#")

def on_message(client, userdata, msg):
    global latest_payload
    try:
        payload = msg.payload.decode()
        latest_payload = json.loads(payload)
        print("📡 Donnée reçue :", latest_payload)
    except Exception as e:
        print("❌ Erreur de parsing JSON:", e)

def start_mqtt():
    client = mqtt.Client()
    # Modifie les identifiants MQTT ici si besoin :
    client.username_pw_set("pepiniere@pepiniere.rt", "pepiniere")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("10.0.0.11", 1883, 60)
    client.loop_forever()

mqtt_thread = threading.Thread(target=start_mqtt)
mqtt_thread.daemon = True
mqtt_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
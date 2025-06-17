from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
import psycopg2.extras
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'devsecret')

def get_db_connection():
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        return psycopg2.connect(db_url)
    return psycopg2.connect(
        dbname="sae24",
        user="postgres",
        password="postgres",
        host="site_externe_db"
    )

@app.route('/')
def index_fr():
    return render_template('index_fr.html')

@app.route('/about')
def about_fr():
    return render_template('about_fr.html')

@app.route('/batterie')
def batterie_fr():
    return render_template('batterie_fr.html')

@app.route('/chargeur')
def chargeur_fr():
    return render_template('chargeur_fr.html')

@app.route('/ecouteurs')
def ecouteurs_fr():
    return render_template('ecouteurs_fr.html')

@app.route('/enceinte')
def enceinte_fr():
    return render_template('enceinte_fr.html')

@app.route('/panier')
def panier_fr():
    return render_template('panier_fr.html')

@app.route('/support-tel')
def support_tel_fr():
    return render_template('support-tel_fr.html')

@app.route('/en')
def index_en():
    return render_template('index_en.html')

@app.route('/about-en')
def about_en():
    return render_template('about_en.html')

@app.route('/cart-en')
def panier_en():
    return render_template('panier_en.html')

@app.route('/batterie-en')
def batterie_en():
    return render_template('batterie_en.html')

@app.route('/chargeur-en')
def chargeur_en():
    return render_template('chargeur_en.html')

@app.route('/ecouteurs-en')
def ecouteurs_en():
    return render_template('ecouteurs_en.html')

@app.route('/enceinte-en')
def enceinte_en():
    return render_template('enceinte_en.html')

@app.route('/support-tel-en')
def support_tel_en():
    return render_template('support-tel_en.html')

@app.route('/login', methods=['GET', 'POST'])
def login_fr():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            return redirect(url_for('index_fr'))
        else:
            flash('Identifiants invalides', 'danger')
    return render_template('login_fr.html')

@app.route('/register', methods=['GET', 'POST'])
def register_fr():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id FROM users WHERE email = %s', (email,))
        if cur.fetchone():
            flash('Cet email existe déjà.', 'danger')
        else:
            hashed = generate_password_hash(password)
            cur.execute('INSERT INTO users (email, password) VALUES (%s, %s)', (email, hashed))
            conn.commit()
            flash('Compte créé, connectez-vous.', 'success')
            cur.close()
            conn.close()
            return redirect(url_for('login_fr'))
        cur.close()
        conn.close()
    return render_template('register_fr.html')

@app.route('/logout')
def logout_fr():
    session.clear()
    return redirect(url_for('index_fr'))

@app.route('/login-en', methods=['GET', 'POST'])
def login_en():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            return redirect(url_for('index_en'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login_en.html')

@app.route('/register-en', methods=['GET', 'POST'])
def register_en():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id FROM users WHERE email = %s', (email,))
        if cur.fetchone():
            flash('This email already exists.', 'danger')
        else:
            hashed = generate_password_hash(password)
            cur.execute('INSERT INTO users (email, password) VALUES (%s, %s)', (email, hashed))
            conn.commit()
            flash('Account created, please sign in.', 'success')
            cur.close()
            conn.close()
            return redirect(url_for('login_en'))
        cur.close()
        conn.close()
    return render_template('register_en.html')

@app.route('/logout-en')
def logout_en():
    session.clear()
    return redirect(url_for('index_en'))

@app.route('/checkout', methods=['GET'])
def checkout():
    return render_template('checkout.html')

@app.route('/pay', methods=['POST'])
def pay():
    cart_json = request.form.get('cart')
    card_number = request.form.get('card_number')
    user_email = session.get('user_email', 'guest')
    if not cart_json:
        flash('Panier vide.', 'danger')
        return redirect(url_for('panier_fr'))
    cart = json.loads(cart_json)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO orders (user_email, created_at) VALUES (%s, %s) RETURNING id', (user_email, datetime.now()))
    order_id = cur.fetchone()[0]
    for item in cart:
        cur.execute(
            'INSERT INTO order_items (order_id, sku, name, option, price, quantity) VALUES (%s, %s, %s, %s, %s, %s)',
            (order_id, item.get('sku'), item.get('name'), item.get('option'), item.get('price'), item.get('quantity'))
        )
    conn.commit()
    cur.close()
    conn.close()
    # Ne pas utiliser flash ici, affiche le message directement
    return render_template('payment_success.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
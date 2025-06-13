from flask import Flask, render_template

app = Flask(__name__)

@app.route('/index_fr')
def index_fr()
    return render_template('index_fr.html')

@app.route('/batterie_fr')
def batterie_fr()
    return render_template('batterie_fr.html')

@app.route('/ecouteurs_fr')
def ecouteurs_fr()
    return render_template('ecouteurs_fr.html')

@app.route('/panier_fr')
def panier_fr()
    return render_template('panier_fr.html')

@app.route('/about_fr')
def about_fr()
    return render_template('about_fr.html')

@app.route('/index_en')
def index_en():
    return render_template('index_en.html')

@app.route('/batterie_en')
def batterie_en():
    return render_template('batterie_en.html')

@app.route('/ecouteurs_en')
def ecouteurs_en():
    return render_template('ecouteurs_en.html')

@app.route('/panier_en')
def panier_en():
    return render_template('panier_en.html')

@app.route('/about_en')
def about_en():
    return render_template('about_en.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
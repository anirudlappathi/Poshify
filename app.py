from flask import Flask, render_template, request, redirect, url_for
from datalayer import clothes_db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('src/home.html')

@app.route('/home.html', methods=['POST'])
def get_clothes():
    if request.method == 'POST':
        clothing_type = request.form['clothing_type']
        color = request.form['color']
        is_clean = request.form['is_clean']
        result = clothes_db.create_cloth(clothing_type, color, is_clean)
        return redirect(url_for('index'))



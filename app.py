from flask import Flask, render_template, request
from datalayer import clothes_db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/put_clothes', methods=['POST'])
def get_clothes():
    if request.method == 'POST':
        clothing_type = request.form['clothing_type']
        color = request.form['color']
        is_clean = request.form['is_clean']
        result = clothes_db.create_cloth(clothing_type, color, is_clean)
        return render_template('result.html', result=result)



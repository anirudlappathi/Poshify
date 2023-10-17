from flask import Flask, render_template, request
from datalayer import clothes_db, users_db

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
  return render_template("home.html")

@app.route("/clothes_page")
def clothes_page():
   return render_template("clothes_page.html")

@app.route("/result", methods=['POST', "GET"])
def result():
    result = ""
    if request.method == 'POST':
        clothing_type = request.form['clothes_type']
        print(clothing_type)
        color = request.form['color']
        is_clean = request.form['is_clean']
        result = clothes_db.create_cloth(clothing_type, color, is_clean)
    return render_template("clothes_page.html", result=result)               


app.run(host='0.0.0.0', port=81)
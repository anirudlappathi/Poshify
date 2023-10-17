from flask import Flask, render_template, request
from datalayer import clothes_db

Poshify = Flask(__name__)


@Poshify.route("/")
@Poshify.route("/home")
def home():
  return render_template("home.html")

@Poshify.route("/clothes_page")
def clothes_page():
   return render_template("clothes_page.html")

@Poshify.route("/result", methods=['POST', "GET"])
def result():
    result = ""
    if request.method == 'POST':
        clothing_type = request.form['clothes_type']
        print(clothing_type)
        color = request.form['color']
        is_clean = request.form['is_clean']
        result = clothes_db.create_cloth(clothing_type, color, is_clean)
    return render_template("clothes_page.html", result=result)               


Poshify.run(host='0.0.0.0', port=81)
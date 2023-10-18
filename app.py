from flask import Flask, render_template, request
from datalayer import clothes_db, users_db
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

global user_id

@app.route("/")
@app.route("/home")
def home():
  return render_template("home.html")

@app.route("/login")
def login():
   return render_template("login.html")

@app.route("/login_check", methods=["POST", "GET"])
def login_success():
   result = ""
   if request.method == "POST":
      username = request.form['username']
      username_user_id = users_db.get_user_by_username(username)
      if username_user_id is None:
        return render_template("login.html", result=result)
      else:
        user_id = username_user_id
        return render_template("home.html")

@app.route("/create_user")
def make_user_page():
   return render_template("create_user.html")

@app.route("/result_users", methods=["POST", "GET"])
def result_users():
    result = ""
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']

        # TEST BLACK SHIRT IMAGE FOR RIGHT NOW

        user_photo_file_name = "test_img/blackshirt.jpg"
        result = users_db.create_user(username=username, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, user_photo_file_name=user_photo_file_name)
    return render_template("create_user.html", result=result)     

@app.route("/clothes_page")
def clothes_page():
   return render_template("clothes_page.html")

@app.route("/result_clothes", methods=['POST', "GET"])
def result_clothes():
    result = ""
    if request.method == 'POST':
        clothing_type = request.form['clothes_type']
        print(clothing_type)
        color = request.form['color']
        is_clean = request.form['is_clean']
        result = clothes_db.create_cloth(clothing_type, color, is_clean)
    return render_template("clothes_page.html", result=result)               

app.run(host='0.0.0.0', port=81)
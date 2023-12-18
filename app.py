from flask import Flask, render_template, request, session
from datalayer.clothes_db import *
from datalayer.users_db import *
from algorithm.color_algo import GetStyleOutfits
import os
from dotenv import load_dotenv


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
@app.route("/home")
def home():
  return render_template("home.html")

@app.route("/login")
def login():
   return render_template("login.html")

@app.route("/dashboard", methods=["POST", "GET"])
def login_success():
   result = ""
   if request.method == "POST":
      username = request.form['username']
      username_user_id = get_user_id_by_username(username)
      if username_user_id is None:
        return render_template("login.html", result=result)
      else:
        session['user_id'] = username_user_id
        result = (username, username_user_id)
        return render_template("home.html", result=result, user_id=username_user_id, successfullogin="yes")

### NEW CODE HERE
@app.route("/closet", methods=["POST", "GET"])
def closet():
      clothes = get_clothing_type_by_user_id(session['user_id'])
      return render_template("home.html", successfullogin="yes", clothes=clothes)



@app.route("/generate_fit", methods=["POST", "GET"])
def generate_fit():
   tops = get_clothing_by_type(session['user_id'], "T-Shirt")
   bots = get_clothing_by_type(session['user_id'], "Pants")
   shoes = get_clothing_by_type(session['user_id'], "Shoes")
   style = "Basic"

   generate = GetStyleOutfits(style, tops, bots, shoes)

   return render_template("home.html", successfullogin="yes", generate=generate)



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
        result = create_user(username=username, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, user_photo_file_name=user_photo_file_name)
    return render_template("create_user.html", result=result)     

@app.route("/clothes_page")
def clothes_page():
   return render_template("clothes_page.html")

@app.route("/result_clothes", methods=['POST', "GET"])
def result_clothes():
    result = ""

    if request.method == 'POST':
        

        if (session['user_id']):
          user_id = session['user_id']
        else:
           return 'ERROR: NOT LOGGED IN'
        
        
        clothing_name = request.form['clothing_name']
        clothing_type = request.form['clothes_type']
        color = request.form['color']
        is_clean = request.form['is_clean']
        hue = request.form['hue']
        saturation = request.form['saturation']
        value = request.form['value']

        if (is_clean == "y"):
           is_clean = True
        else:
           is_clean = False

        
        result = create_cloth(user_id, clothing_name, clothing_type, color, is_clean, hue, saturation, value)
    return render_template("clothes_page.html", result=result)               

app.run(host='0.0.0.0', port=81)
from flask import Flask, render_template, request, session
from datalayer.clothes_db import *
from datalayer.users_db import *
from algorithm.color_algo import GetStyleOutfits
from algorithm.color_detection_camera import process_image
import os
from dotenv import load_dotenv
import numpy as np

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
@app.route("/home")
def home():
  user_id = None
  if 'user_id' in session:
     user_id = session['user_id']
  return render_template("home.html", user_id=user_id)

@app.route("/login", methods=["POST", "GET"])
def login():
   user_id = None
   if 'user_id' in session:
      user_id = session['user_id']
      return render_template("dashboard.html", result="", user_id=session['user_id'])
   
   if request.method == "POST":
      username = request.form['username']
      user_id = get_user_id_by_username(username)
      if user_id is None:
        return render_template("login.html", result="Username does not exist")
      else:
        session['username'] = username
        session['user_id'] = user_id
        result = (username, user_id)
        return render_template("dashboard.html", result=result, user_id=session['user_id'])
   return render_template("login.html", result="No result yet", user_id=user_id)

@app.route("/signup", methods=["POST", "GET"])
def signup():
    result = ""
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        user_photo_file_name = "test_img/blackshirt.jpg"
        user_id = create_user(username=username, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, user_photo_file_name=user_photo_file_name)
        session['user_id'] = user_id
        return render_template("dashboard.html", user_id=user_id, result=user_id)     
    return render_template("signup.html", result="User not created yet")
     
@app.route("/dashboard", methods=["POST", "GET"])
def dashboard():
   user_id = session.get('user_id')
   if user_id is None:
      render_template("home.html")
   return render_template("dashboard.html", result=session['user_id'], user_id=session['user_id'])

@app.route("/closet", methods=["POST", "GET"])
def closet():
      clothes = get_clothing_type_by_user_id(session['user_id'])
      return render_template("closet.html", user_id=session['user_id'], clothes=clothes)

@app.route("/outfits", methods=["POST", "GET"])
def generate_fit():
   tops = get_clothing_by_type(session['user_id'], "T-Shirt")
   bots = get_clothing_by_type(session['user_id'], "Pants")
   shoes = get_clothing_by_type(session['user_id'], "Shoes")
   styles = ["Basic", "Neutral", "Analogous", "Summer", "Winter"]

   outfits = []
   for style in styles:
      outfits.extend(GetStyleOutfits(style, tops, bots, shoes))

   return render_template("outfits.html", user_id=session['user_id'], outfits=outfits)


@app.route("/add_clothing_manual", methods=['POST', "GET"])
def add_clothing_manual():
   user_id = None
   if 'user_id' in session:
      user_id = session['user_id']

   if request.method == 'POST':
        
        print("start posting")
        if (session['user_id']):
          user_id = session['user_id']
        else:
           return 'ERROR: NOT LOGGED IN'
        
        
        clothing_name = request.form['clothing_name']
        clothing_type = request.form['clothes_type']
        is_clean = request.form['is_clean'] == "y"
        hue = request.form['hue']
        saturation = request.form['saturation']
        value = request.form['value']

        if clothing_name is None or clothing_type is None or is_clean is None or hue is None or saturation is None or value is None:
         return render_template("add_clothing_manual.html", result="Empty Field", user_id=user_id)       

        result = create_cloth(user_id, clothing_name, clothing_type, is_clean, hue, saturation, value)
        image_data = "Placeholder of type image"
        return render_template("add_clothing_manual.html", result=result, user_id=user_id)   
    
   return render_template("add_clothing_manual.html", result="", user_id=user_id)               

@app.route("/add_clothing_camera", methods=['POST', "GET"])
def add_clothing_camera():
   user_id = None
   if 'user_id' in session:
      user_id = session['user_id']

   if request.method == 'POST':
        
        print("start posting")
        if (session['user_id']):
          user_id = session['user_id']
        else:
           return 'ERROR: NOT LOGGED IN'
        
        
        clothing_name = request.form['clothing_name']
        clothing_type = request.form['clothes_type']
        is_clean = request.form['is_clean']
        hue = request.form['hue']
        saturation = request.form['saturation']
        value = request.form['value']

        if (is_clean == "y"):
           is_clean = True
        else:
           is_clean = False

        result = create_cloth(user_id, clothing_name, clothing_type, is_clean, hue, saturation, value)
        image_data = request.form['imageData']
        dominant_color = process_image(image_data)
        print("dominant color: " + str(dominant_color))
        return render_template("add_clothing_camera.html", result=result, user_id=user_id)   
    
   return render_template("add_clothing_camera.html", result="", user_id=user_id)               

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)


app.run(host='0.0.0.0', port=81)
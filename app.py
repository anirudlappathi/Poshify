from datalayer.clothes_db import *
from datalayer.users_db import *
from algorithm.color_algo import GetStyleOutfits
from algorithm.color_detection_camera import process_image

import json
import os
from os import environ as env
from flask import Flask, render_template, request, session, redirect, url_for
from dotenv import find_dotenv, load_dotenv
import uuid

from authlib.integrations.flask_client import OAuth
from urllib.parse import quote_plus, urlencode

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
else:
   print("ERROR: .env FILE NOT FOUND CANNOT CONNECT TO DB AND AUTH0")

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/")
@app.route("/home")
def home():
  return render_template("home.html", session=session.get('user'))

@app.route("/signup", methods=["POST", "GET"])
def signup():
   return oauth.auth0.authorize_redirect(
      redirect_uri=url_for("callback", _external=True),
      screen_hint="signup"
   )

@app.route("/login", methods=["POST", "GET"])
def login():
   return oauth.auth0.authorize_redirect(
      redirect_uri=url_for("callback", _external=True),
      screen_hint="login"
   )

@app.route("/callback", methods=["GET", "POST"])
def callback():
   token = oauth.auth0.authorize_access_token()
   session["user"] = token
   print(session.get("user"))

   user_id = token['userinfo']['sub'][14:]
   print(user_id)
   username = token['userinfo']['nickname']
   password = None
   first_name = token['userinfo']['given_name']
   last_name = token['userinfo']['family_name']
   email = token['userinfo']['email']
   phone_number = None
   user_photo_file_name = token['userinfo']['picture']
   
   create_user(user_id=user_id, username=username, password=password, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, user_photo_file_name=user_photo_file_name)   

   return redirect("/dashboard")

@app.route("/logout")
def logout():
   session.clear()
   return redirect(
      "https://" + env.get("AUTH0_DOMAIN")
      + "/v2/logout?"
      + urlencode(
         {
               "returnTo": url_for("home", _external=True),
               "client_id": env.get("AUTH0_CLIENT_ID"),
         },
         quote_via=quote_plus,
      )
   )
     
@app.route("/dashboard", methods=["POST", "GET"])
def dashboard():
   user = session.get("user")
   if not user:
      print("ERROR: USER NOT LOGGED IN")
      return render_template("home.html", session=session.get('user'))
   user_id = user['userinfo']['sub'][14:]
   if not user_id:
      print("ERROR: NO ID_TOKEN FOUND")
      return render_template("home.html", session=session.get('user'))
   return render_template("dashboard.html", session=user, user_id=user_id, pretty=json.dumps(session.get('user'), indent=4))

@app.route("/closet", methods=["POST", "GET"])
def closet():
      user = session.get("user")
      if not user:
         print("ERROR: USER NOT LOGGED IN")
      user_id = user['userinfo']['sub'][14:]
      if not user_id:
         print("ERROR: NO ID_TOKEN FOUND")

      clothes = get_clothing_name_and_image_by_user_id(user_id)
      print(clothes)
      return render_template("closet.html", session=user, user_id=user_id, clothes=clothes)

@app.route("/outfits", methods=["POST", "GET"])
def generate_fit():
   user = session.get("user")
   if not user:
      print("ERROR: USER NOT LOGGED IN")
      return render_template("home.html", session=session.get('user'))
   user_id = user['userinfo']['sub'][14:]
   if not user_id:
      print("ERROR: NO ID_TOKEN FOUND")
      return render_template("home.html", session=session.get('user'))

   tops = get_clothing_by_type(user_id, "T-Shirt")
   bots = get_clothing_by_type(user_id, "Pants")
   shoes = get_clothing_by_type(user_id, "Shoes")
   styles = ["Basic", "Neutral", "Analogous", "Summer", "Winter"]

   outfits = []
   for style in styles:
      outfits.extend(GetStyleOutfits(style, tops, bots, shoes))

   return render_template("outfits.html", session=user, user_id=user_id, outfits=outfits)

@app.route("/settings", methods=["POST", "GET"])
def settings():
   user = session.get("user")
   if not user:
      print("ERROR: USER NOT LOGGED IN")
      return render_template("home.html", session=session.get('user'))
   user_id = user['userinfo']['sub'][14:]
   if not user_id:
      print("ERROR: NO ID_TOKEN FOUND")
      return render_template("home.html", session=session.get('user'))

   return render_template("settings.html", session=user, user_id=user_id)

@app.route("/add_clothing_manual", methods=['POST', "GET"])
def add_clothing_manual():
   user = session.get("user")
   if not user:
      print("ERROR: USER NOT LOGGED IN")
      return render_template("home.html", session=session.get('user'))
   user_id = user['userinfo']['sub'][14:]
   if not user_id:
      print("ERROR: NO ID_TOKEN FOUND")
      return render_template("home.html", session=session.get('user'))

   if request.method == 'POST':     
        
      clothing_name = request.form['clothing_name']
      clothing_type = request.form['clothes_type']
      is_clean = request.form['is_clean'] == "y"
      hue = request.form['hue']
      saturation = request.form['saturation']
      value = request.form['value']

      image_data = request.files['image']
      if image_data.filename == '':
         return render_template("add_clothing_manual.html", result="No Selected File", session=user, user_id=user_id)   
      
      if image_data:
         filename = str(uuid.uuid4()) + os.path.splitext(image_data.filename)[1]
         image_data.save(os.path.join('static/clothing_images', filename))

      if clothing_name is None or clothing_type is None or is_clean is None or hue is None or saturation is None or value is None:
         return render_template("add_clothing_manual.html", result="Empty Field", user_id=user_id)       

      result = create_cloth(user_id, clothing_name, clothing_type, is_clean, hue, saturation, value, filename)
      return render_template("add_clothing_manual.html", result=result, session=user, user_id=user_id)   
   
   return render_template("add_clothing_manual.html", result="", user_id=user_id)               

@app.route("/add_clothing_camera", methods=['POST', "GET"])
def add_clothing_camera():

   user = session.get("user")
   if not user:
      print("ERROR: USER NOT LOGGED IN")
      return render_template("home.html", session=session.get('user'))
   user_id = user['userinfo']['sub'][14:]
   if not user_id:
      print("ERROR: NO ID_TOKEN FOUND")
      return render_template("home.html", session=session.get('user'))

   if request.method == 'POST':
         
        clothing_name = request.form['clothing_name']
        clothing_type = request.form['clothes_type']
        is_clean = request.form['is_clean']
        hue = request.form['hue']
        saturation = request.form['saturation']
        value = request.form['value']
        uploaded_image = request.file['image']
        print(uploaded_image)
        image_path = f"clothing_images/{clothing_name}.jpg"
        uploaded_image.save(image_path)

        if (is_clean == "y"):
           is_clean = True
        else:
           is_clean = False

        result = create_cloth(user_id, clothing_name, clothing_type, is_clean, hue, saturation, value)
        image_data = request.form['imageData']
        dominant_color = process_image(image_data)
        print("dominant color: " + str(dominant_color))
        return render_template("add_clothing_camera.html", result=result, user_id=user_id)   
    
   return render_template("add_clothing_camera.html", session=user, user_id=user_id)               

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=81)

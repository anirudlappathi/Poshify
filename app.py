from datalayer.clothes_db import *
from datalayer.users_db import *
from algorithm.color_algo import GetStyleOutfits
from algorithm.color_detection_camera import dominant_color_finder_dataurl

import base64
from PIL import Image
from io import BytesIO

import json
import os
from os import environ as env
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
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
      redirect_uri=url_for("callback_signup", _external=True),
      screen_hint="signup"
   )

@app.route("/login", methods=["POST", "GET"])
def login():
   return oauth.auth0.authorize_redirect(
      redirect_uri=url_for("callback_login", _external=True),
      screen_hint="login"
   )

@app.route("/callback_login", methods=["GET", "POST"])
def callback_login():
   token = oauth.auth0.authorize_access_token()
   session["user"] = token
   session["userid"] = token['userinfo']['sub'][14:]
   print(session.get("user"))
   print('LOGIN')
   user_id = session.get('userid')
   print(user_id)
   username = token['userinfo']['nickname']
   password = None
   first_name = token['userinfo']['given_name']
   last_name = token['userinfo']['family_name']
   email = token['userinfo']['email']
   phone_number = None
   user_photo_file_name = token['userinfo']['picture']
   
   #create_user(user_id=user_id, username=username, password=password, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, user_photo_file_name=user_photo_file_name)   

   return redirect("/dashboard")

@app.route("/callback_signup", methods=["GET", "POST"])
def callback_signup():
   print('SIGNUP')

   token = oauth.auth0.authorize_access_token()
   session["user"] = token
   session["userid"] = token['userinfo']['sub'][14:]
   
   missingInfo = []

   user_id = session.get("userid")
   user_photo_file_name = token['userinfo']['picture']
   email = token['userinfo']['email']

   if 'nickname' not in token['userinfo']:
      missingInfo.append('nickname')
   else:
      username = token['userinfo']['nickname']

   if 'given_name' not in token['userinfo']:
      missingInfo.append('given_name')
   else:
      first_name = token['userinfo']['given_name']

   if 'family_name' not in token['userinfo']:
      missingInfo.append('family_name')
   else:
      last_name = token['userinfo']['family_name']

   phone_number = ""
   password = ""
   
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
      return render_template("home.html", session=user)
   user_id = session.get('userid')
   if not user_id:
      print("ERROR: NO ID_TOKEN FOUND")
      return render_template("home.html", session=user)
   return render_template("dashboard.html", session=user, user_id=user_id, pretty=json.dumps(session.get('user'), indent=4))

@app.route("/closet", methods=["POST", "GET"])
def closet():
      user = session.get("user")
      if not user:
         print("ERROR: USER NOT LOGGED IN")
      user_id = session.get('userid')
      if not user_id:
         print("ERROR: NO ID_TOKEN FOUND")

      clothes = get_clothing_name_image_id_by_user_id(user_id)
      print(clothes)
      return render_template("closet.html", session=user, user_id=user_id, clothes=clothes)

@app.route("/outfits", methods=["POST", "GET"])
def generate_fit():
   user = session.get("user")
   if not user:
      print("ERROR: USER NOT LOGGED IN")
      return render_template("home.html", session=session.get('user'))
   user_id = session.get('userid')
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
   user_id = session.get('userid')
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
   user_id = session.get('userid')
   if not user_id:
      print("ERROR: NO ID_TOKEN FOUND")
      return render_template("home.html", session=session.get('user'))

   if request.method == 'POST':     
        
      clothing_name = request.form['clothing_name']
      clothing_type = request.form['clothes_type']
      is_clean = request.form['is_clean'] == "y"

      image_data = request.files['image']

      if image_data.filename == '':
         return render_template("add_clothing_manual.html", result="No Selected File", session=user, user_id=user_id)   
      
      filename = str(uuid.uuid4()) + os.path.splitext(image_data.filename)[1]
      image_data.save(os.path.join('static/clothing_images', filename))

      file_path = os.path.join("static/clothing_images", filename)
      with open(file_path, 'rb') as img_file:
         image_binary = img_file.read()

      encoded_image = base64.b64encode(image_binary)
      dominant_color = dominant_color_finder_dataurl(encoded_image)

      hue = dominant_color[0]
      saturation = dominant_color[1]
      value = dominant_color[2]

      if clothing_name is None or clothing_type is None or is_clean is None or hue is None or saturation is None or value is None:
         return render_template("add_clothing_manual.html", session=user, result="Empty Field", user_id=user_id)       

      result = create_cloth(user_id, clothing_name, clothing_type, is_clean, hue, saturation, value, filename)
      return render_template("add_clothing_manual.html", result=result, session=user, user_id=user_id)   
   
   return render_template("add_clothing_manual.html", session=user, result="", user_id=user_id)               

@app.route("/add_clothing_camera", methods=["POST", "GET"])
def add_clothing_camera():
   user = session.get("user")
   if not user:
      print("ERROR: USER NOT LOGGED IN")
      return render_template("home.html", session=session.get('user'))
   user_id = session.get('userid')
   if not user_id:
      print("ERROR: NO ID_TOKEN FOUND")
      return render_template("home.html", session=session.get('user'))
   if request.method == 'POST':

      clothing_name = request.form['clothing_name']
      clothing_type = request.form['clothes_type']
      is_clean = request.form['is_clean']
      image_data = request.form['imageData']

      has_name = is_clothing_name_by_id(clothing_name, user_id)
      print(has_name)
      if has_name:
         return render_template("add_clothing_camera.html", session=user, result="Name already exists for cloth", user_id=user_id)   
      if clothing_name is None or clothing_type is None or is_clean is None or image_data is None:
         return render_template("add_clothing_camera.html", session=user, result="All data fields not entered", user_id=user_id)   

      if (is_clean == "y"):
         is_clean = True
      else:
         is_clean = False

      # 360 100 100
      hue, saturation, value = dominant_color_finder_dataurl(image_data)
      filename = None

      if image_data:
         filename = str(uuid.uuid4()) + ".jpeg"
         image_binary = base64.b64decode(image_data)
         img = Image.open(BytesIO(image_binary))
         img.save(os.path.join('static/clothing_images', filename), "JPEG")
      else:
         return render_template("add_clothing_camera.html", result="Camera Data invalid or not working", user_id=user_id)   

      result = create_cloth(user_id, clothing_name, clothing_type, is_clean, hue, saturation, value, filename)

      return render_template("add_clothing_camera.html", session=user, result=result, user_id=user_id)   
   
   return render_template("add_clothing_camera.html", session=user, user_id=user_id)               


@app.route('/update', methods=['POST'])
def update_element():
    if request.method == 'POST':
        data = request.get_json()
        updated_text = data.get('updatedText')
        identifier = data.get('identifier')
        user = session.get("user")
        user_id = session.get('userid')
        print("USER ID: " + user_id)

        update_clothing_name_by_identifier(identifier, updated_text, user_id)

        print("Updated Text:", updated_text)
        print("Identifier:", identifier)

        # Return a response with the identifier and a success message
        response_data = {
            'identifier': identifier,
            'message': 'Updated successfully'
        }
        return jsonify(response_data), 200
    else:
        return 'Invalid request', 400

@app.route('/delete', methods=['DELETE'])
def delete_element():
   if request.method == 'DELETE':
      data = request.get_json()
      clothes_id = data.get('clothes_id')
      user_id = session.get('userid')
      url = get_clothing_url_by_id(clothes_id, user_id)
      file_path = os.path.join("static/clothing_images", url)
      if os.path.exists(file_path):
            os.remove(file_path)
            delete_clothing_by_id(clothes_id, user_id)
            return jsonify({'message': f'{clothes_id} deleted successfully'}), 200
      else:
            return jsonify({'message': 'File not found'}), 404
   else:
      return jsonify({'message': 'Method not allowed'}), 405

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=81)

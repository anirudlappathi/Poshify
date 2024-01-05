from datalayer.clothes_db import *
from datalayer.users_db import *
from datalayer.calendar_db import *
from algorithm.color_algo import GetStyleOutfits
from algorithm.color_detection_camera import dominant_color_finder_dataurl

import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

import base64
from PIL import Image
from io import BytesIO

import os
from os import environ as env
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import uuid

from dotenv import find_dotenv, load_dotenv

from authlib.integrations.flask_client import OAuth
from urllib.parse import quote_plus, urlencode

import configparser
config = configparser.ConfigParser()
config.read('config.properties')

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

if config.get("DEFAULT", "DEVTYPE") == "aws":
   import boto3
   s3 = boto3.client('s3')
   CLOTHING_BUCKET_NAME = "poshify-clothingimages"

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
   print('LOGIN')

   token = oauth.auth0.authorize_access_token()
   session["user"] = token
   session["userid"] = token['userinfo']['sub'][14:]
   
   phone_number = None
   password = None

   user_id = session.get("userid")
   user_photo_file_name = token['userinfo']['picture']
   email = token['userinfo']['email']

   missingInfo = []

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
   
   session['missingInfo'] = missingInfo
   if len(missingInfo) == 0:
      create_user(user_id=user_id, username=username, password=password, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, user_photo_file_name=user_photo_file_name)   
   else:
      return render_template('onboarding.html', session=session['user'], user_id=session['userid'], missingInfo=missingInfo)

   return redirect("/dashboard")

@app.route("/callback_signup", methods=["GET", "POST"])
def callback_signup():
   print('SIGNUP')

   token = oauth.auth0.authorize_access_token()
   session["user"] = token
   session["userid"] = token['userinfo']['sub'][14:]
   
   phone_number = ""
   password = ""

   user_id = session.get("userid")
   user_photo_file_name = token['userinfo']['picture']
   email = token['userinfo']['email']

   missingInfo = []

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

   session['missingInfo'] = missingInfo
   if len(missingInfo) == 0:
      create_user(user_id=user_id, username=username, password=password, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, user_photo_file_name=user_photo_file_name)   
   else:
      create_user(user_id=user_id, username=token['userinfo'].get('nickname'), password=password, first_name=token['userinfo'].get('given_name'), last_name=token['userinfo'].get('family_name'), email=email, phone_number=phone_number, user_photo_file_name=user_photo_file_name)   
      return render_template('onboarding.html', session=session['user'], user_id=session['userid'], missingInfo=missingInfo)

   return redirect("/dashboard")

@app.route('/onboarding', methods=['POST'])
def onboarding():
   print('started')
   user = session.get("user")
   if not user:
      print("ERROR: USER NOT LOGGED IN")
      return redirect("/home", code=302)
   user_id = session.get('userid')
   if not user_id:
      print("ERROR: NO ID_TOKEN FOUND")
      return redirect("/home", code=302)

   missingInfo = session['missingInfo']
   if len(missingInfo) == 0:
      return render_template("dashboard.html", session=session['user'], user_id=session['userid'])

   if request.method == 'POST':
      for info in missingInfo:
         user_data_to_add_to_db = request.form.get(info)
         if user_data_to_add_to_db is None:
            return render_template("onboarding.html", missingInfo=missingInfo, result="Add all user info")
         update_data_given_row(session['userid'], info, user_data_to_add_to_db)

      return render_template("dashboard.html", session=session['user'], user_id=session['userid'])
   
   return render_template("onboarding.html", session=session['user'], user_id=session['userid'], missingInfo=missingInfo)

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
      return redirect("/home", code=302)
   user_id = session.get('userid')
   if not user_id:
      print("ERROR: NO ID_TOKEN FOUND")
      return redirect("/home", code=302)
   return render_template("dashboard.html", session=user, user_id=user_id)


@app.route("/closet", methods=["POST", "GET"])
def closet():
      user = session.get("user")
      if not user:
         print("ERROR: USER NOT LOGGED IN")
         return redirect("/home", code=302)
      user_id = session.get('userid')
      if not user_id:
         print("ERROR: NO ID_TOKEN FOUND")
         return redirect("/home", code=302)

      clothes = get_clothing_name_image_id_by_user_id(user_id)
         
      filters = [[] for i in range(3)]
      if 'filters' in session:
         filters = session['filters']

      return render_template("closet.html", session=user, user_id=user_id, clothes=clothes, filters=filters, config=config.get("DEFAULT", "CLOTHING_IMAGES_FILEPATH"))



@app.route("/outfits", methods=["POST", "GET"])
def generate_fit():
   user = session.get("user")
   if not user:
      print("ERROR: USER NOT LOGGED IN")
      return redirect("/home", code=302)
   user_id = session.get('userid')
   if not user_id:
      print("ERROR: NO ID_TOKEN FOUND")
      return redirect("/home", code=302)

   tops = get_clothing_by_type(user_id, "T-Shirt")
   bots = get_clothing_by_type(user_id, "Pants")
   shoes = get_clothing_by_type(user_id, "Shoes")

   outfits = GetStyleOutfits(tops, bots, shoes)
   print("outfit count: ", len(outfits))
   calendarInfo = get_image_paths_per_day(user_id)
   print("ajslka", calendarInfo)
   if calendarInfo:
      return render_template("outfits.html", session=user, user_id=user_id, outfits=outfits, calendarInfo = calendarInfo, config=config.get("DEFAULT", "CLOTHING_IMAGES_FILEPATH"))
   else:
      return render_template("outfits.html", session=user, user_id=user_id, outfits=outfits, config=config.get("DEFAULT", "CLOTHING_IMAGES_FILEPATH"))

@app.route("/settings", methods=["POST", "GET"])
def settings():
   user = session.get("user")
   if not user:
      print("ERROR: USER NOT LOGGED IN")
      return redirect("/home", code=302)
   user_id = session.get('userid')
   if not user_id:
      print("ERROR: NO ID_TOKEN FOUND")
      return redirect("/home", code=302)

   return render_template("settings.html", session=user, user_id=user_id)

@app.route("/add_clothing_manual", methods=['POST', "GET"])
def add_clothing_manual():
   user = session.get("user")
   if not user:
      print("ERROR: USER NOT LOGGED IN")
      return redirect("/home", code=302)
   user_id = session.get('userid')
   if not user_id:
      print("ERROR: NO ID_TOKEN FOUND")
      return redirect("/home", code=302)

   if request.method == 'POST':     
      
      clothing_name = request.form['clothing_name']
      clothing_type = request.form['clothes_type']
      is_clean = request.form['is_clean'] == "y"
      
      image_data = request.files['image']

      has_name = has_clothing_name_by_id(clothing_name, user_id)
      if has_name:
         return render_template("add_clothing_manual.html", session=user, result="Name already exists for cloth", user_id=user_id)   
      if clothing_name is None or clothing_type is None or is_clean is None or image_data is None:
         return render_template("add_clothing_manual.html", session=user, result="All data fields not entered", user_id=user_id)   


      if image_data.filename == '':
         return render_template("add_clothing_manual.html", result="No Selected File", session=user, user_id=user_id)   
      
      filename = str(uuid.uuid4()) + os.path.splitext(image_data.filename)[1]


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

      if config.get("DEFAULT", "DEVTYPE") == "local":
         image_data.save(os.path.join('static/clothing_images', filename))
      else:
         s3.put_object(Body=image_data, Bucket=CLOTHING_BUCKET_NAME, Key=f"clothing_images/{filename}")

      return render_template("add_clothing_manual.html", result=result, session=user, user_id=user_id)   
   
   return render_template("add_clothing_manual.html", session=user, result="", user_id=user_id)               

@app.route("/add_clothing_camera", methods=["POST", "GET"])
def add_clothing_camera():
   user = session.get("user")
   if not user:
      print("ERROR: USER NOT LOGGED IN")
      return redirect("/home", code=302)
   user_id = session.get('userid')
   if not user_id:
      print("ERROR: NO ID_TOKEN FOUND")
      return redirect("/home", code=302)
   
   if request.method == 'POST':

      clothing_name = request.form['clothing_name']
      clothing_type = request.form['clothes_type']
      is_clean = request.form['is_clean']
      image_data = request.form['imageData']

      has_name = has_clothing_name_by_id(clothing_name, user_id)
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

      if image_data:
         filename = str(uuid.uuid4()) + ".jpeg"
         hue, saturation, value = dominant_color_finder_dataurl(image_data)
         image_binary = base64.b64decode(image_data)
         img = Image.open(BytesIO(image_binary))
         if config.get("DEFAULT", "DEVTYPE") == "local":
            img.save(os.path.join('static/clothing_images', filename), "JPEG")
         else:
            s3.put_object(Body=image_binary, Bucket=CLOTHING_BUCKET_NAME, Key=f"clothing_images/{filename}")
      else:
         return render_template("add_clothing_camera.html", result="Camera Data invalid or not working", user_id=user_id)   

      result = create_cloth(user_id, clothing_name, clothing_type, is_clean, hue, saturation, value, filename)

      return render_template("add_clothing_camera.html", session=user, result=result, user_id=user_id)   
   
   return render_template("add_clothing_camera.html", session=user, user_id=user_id)               


@app.route('/update', methods=['POST'])
def update_element():
   user = session.get("user")
   if not user:
      print("ERROR: USER NOT LOGGED IN")
      return redirect("/home", code=302)
   user_id = session.get('userid')
   if not user_id:
      print("ERROR: NO ID_TOKEN FOUND")
      return redirect("/home", code=302)
   
   if request.method == 'POST':
      data = request.get_json()
      updated_text = data.get('updatedText')
      has_name = has_clothing_name_by_id(updated_text, user_id)
      clothing_name = data.get('identifier')
      print(clothing_name, updated_text)
      if updated_text.lower() == clothing_name.lower():
         print('same name')
         response_data = {
            'identifier': updated_text,
            'message': 'Same name'
         }
         update_clothing_name_by_clothing_name(clothing_name, updated_text, user_id)
         return jsonify(response_data), 200
      elif has_name:
         print('has name')
         response_data = {
            'identifier': clothing_name,
            'message': 'Name exists'
         }
         return jsonify(response_data), 200
      print('gangangn')
      user = session.get("user")
      user_id = session.get('userid')
      print("USER ID: " + user_id)

      update_clothing_name_by_clothing_name(clothing_name, updated_text, user_id)

      print("Updated Text:", updated_text)
      print("Identifier:", clothing_name)

      # Return a response with the identifier and a success message
      response_data = {
            'identifier': updated_text,
            'message': 'Updated successfully'
      }
      return jsonify(response_data), 200
   else:
      return 'Invalid request', 400

@app.route('/update_cleanliness', methods=['POST'])
def update_cleanliness():
   user = session.get("user")
   if not user:
      print("ERROR: USER NOT LOGGED IN")
      return redirect("/home", code=302)
   user_id = session.get('userid')
   if not user_id:
      print("ERROR: NO ID_TOKEN FOUND")
      return redirect("/home", code=302)
   if request.method == 'POST':
      data = request.get_json()
      clothid = data.get('clothesId')
      new_status = data.get('cleanlinessStatus')

      update_cleanliness_status(clothid, new_status)
      response_data = {
            'clothid': clothid,
            'message': 'Updated successfully'
      }
      return jsonify(response_data), 200

@app.route('/delete', methods=['DELETE'])
def delete_element():
   user = session.get("user")
   if not user:
      print("ERROR: USER NOT LOGGED IN")
      return redirect("/home", code=302)
   user_id = session.get('userid')
   if not user_id:
      print("ERROR: NO ID_TOKEN FOUND")
      return redirect("/home", code=302)
   if request.method == 'DELETE':
      data = request.get_json()
      clothes_id = data.get('clothes_id')
      user_id = session.get('userid')
      url = get_clothing_url_by_id(clothes_id, user_id)
      if config.get("DEFAULT", "DEVTYPE") == "local":
         filepath = os.path.join("static/clothing_images", url)
      else:
         s3.delete_object(Bucket=CLOTHING_BUCKET_NAME, Key=f'clothing_images/{url}')
      if os.path.exists(filepath):
            os.remove(filepath)
            delete_clothing_by_id(clothes_id, user_id)
            return jsonify({'message': f'{clothes_id} deleted successfully'}), 200
      else:
            return jsonify({'message': 'File not found'}), 404
   else:
      return jsonify({'message': 'Method not allowed'}), 405
   
@app.route("/update_filters", methods=["POST"])
def update_filters():
   user = session.get("user")
   if not user:
      print("ERROR: USER NOT LOGGED IN")
      return redirect("/home", code=302)
   user_id = session.get('userid')
   if not user_id:
      print("ERROR: NO ID_TOKEN FOUND")
      return redirect("/home", code=302)
   if request.method == 'POST':
      filter_data = request.get_json()
      articles_data = filter_data.get('articles')
      # color_data = filter_data.get('color_data')
      # is_clean_data = filter_data.get('is_clean_data')
      session['filters'] = [articles_data]

      return ({'message': f'{articles_data} filter added successfully'}), 200


@app.route('/save_outfit', methods=['POST'])
def save_outfit():
   try:
      outfit_data = request.json
      user_id = session.get('userid')
      day_of_week = outfit_data.get('day_of_week')
      image_paths = outfit_data.get('image_paths')
      outfit_type = outfit_data.get('outfitType')
      print("DAY OF WEEK: ", day_of_week)
      print("IOMAGE PATHS: ", image_paths)
      print("OUTFIT TYPE: ", outfit_type)

      create_entry(user_id, day_of_week, image_paths, outfit_type)
      return 'Outfit data received and saved successfully.', 200
   
   except Exception as e:
      print(f"Error saving outfit data: {str(e)}")
      return 'Failed to process outfit data.', 500

@app.route('/delete_outfit', methods=['POST'])
def delete_outfit():
   try:
      outfit_data = request.json
      user_id = session.get('userid')
      day_of_week = outfit_data.get('day_of_week')
      image_paths = outfit_data.get('image_paths')
      outfit_type = outfit_data.get('outfitType')
      

      delete_entry(user_id, day_of_week, image_paths[0], outfit_type)
      delete_entry(user_id, day_of_week, image_paths[1], outfit_type)
      delete_entry(user_id, day_of_week, image_paths[2], outfit_type)
      return 'Outfit data received and saved successfully.', 200
   
   except Exception as e:
      print(f"Error deleting outfit data: {str(e)}")
      return 'Failed to process outfit data.', 500

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=config.get("DEFAULT", "PORT"))

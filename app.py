from flask import Flask, render_template, request, session
from datalayer.clothes_db import *
from datalayer.users_db import *
from algorithm.color_algo import GetStyleOutfits
import os
from dotenv import load_dotenv
import cv2
import numpy as np
import base64

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

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
      username_user_id = get_user_id_by_username(username)
      if username_user_id is None:
        return render_template("login.html", result=result)
      else:
        session['user_id'] = username_user_id
        result = (username, username_user_id)
        succesfullogin = "yes"
        return render_template("home.html", result=result, user_id=username_user_id, successfullogin=succesfullogin)


###
###
###
##3
### NEW CODE HERE
@app.route("/get_all_cloth", methods=["POST", "GET"])
def get_all_cloth():
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
        image_data = request.form['imageData'].split(",")[1]  # Remove 'data:image/jpeg;base64,' prefix
        result = create_cloth(user_id, clothing_name, clothing_type, color, is_clean, hue, saturation, value)

        if result == "Cloth created successfully":
            dominant_color = process_image(image_data)
            # Save the dominant color information into the database
            # For example: save_dominant_color(user_id, clothing_name, dominant_color    
    
    
    return render_template("clothes_page.html", result=result)               



def process_image(image_data):
    img_data = base64.b64decode(image_data)
    nparr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Your OpenCV processing logic here to find dominant color
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    k = 5
    HSVframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    HSVframe = HSVframe.reshape((-1, 3))
    HSVframe = np.float32(HSVframe)

    _, labels, centers = cv2.kmeans(HSVframe, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    dominant_color = centers[np.argmax(np.bincount(labels.flatten()))]
    print("Dominant color:", dominant_color)

    return dominant_color.tolist()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)


app.run(host='0.0.0.0', port=81)
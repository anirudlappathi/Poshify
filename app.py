from flask import Flask, render_template, request, session
from datalayer import clothes_db, users_db
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

@app.route("/login_check", methods=["POST", "GET"])
def login_success():
   result = ""
   if request.method == "POST":
      username = request.form['username']
      username_user_id = users_db.get_user_id_by_username(username)
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
      clothes = clothes_db.get_clothing_type_by_user_id(session['user_id'])
      return render_template("home.html", successfullogin="yes", clothes=clothes)


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
        
        print("POSTING CLOTHING")

        if (session['user_id']):
          user_id = session['user_id']
        else:
           return 'ERROR: NOT LOGGED IN'
        
        print("POSTING CLOTHING")
        
        clothing_type = request.form['clothes_type']
        color = request.form['color']
        is_clean = request.form['is_clean']

        print("POSTING CLOTHING")

        if (is_clean == "y"):
           is_clean = True
        else:
           is_clean = False

           print("POSTING CLOTHING")
        
        print("ALL VALUES: ", user_id, clothing_type, color, is_clean)
        result = clothes_db.create_cloth(user_id, clothing_type, color, is_clean)
    return render_template("clothes_page.html", result=result)               

app.run(host='0.0.0.0', port=81)
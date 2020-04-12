from flask import Flask, render_template, session, request, send_file, Response, redirect, url_for, flash
from flask_session import Session
from flask_images import resized_img_src
from datetime import datetime

app = Flask(__name__)

app.secret_key = "hello there"

# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

users = []
owner = {
    "name": "John Doe",
    "phone_num": "(521) 824-2004",
    "email": "johndoe@gmail.com",
    "password": "hello123"
}
users.append(owner)

time = datetime.now()
timeStr = ""

month = str(time.month)

for i in range(len(month)):
    if month[i] == "0":
        month = month[0:i:] + month[i + 1::]
    else:
        break

day = str(time.day)

for i in range(len(day)):
    if day[i] == "0":
        day = day[0:i:] + day[i + 1::]
    else:
        break

year = str(time.year)
year = year[2:]

if time.hour == 0:
    timeStr = time.strftime(month + "/" + day + "/" + year + " 12:%M AM")
elif time.hour > 0 and time.hour < 12:
    timeStr = time.strftime(month + "/" + day + "/" + year + " %H:%M AM")
elif time.hour == 12:
    timeStr = time.strftime(month + "/" + day + "/" + year + " 12:%M PM")
elif time.hour >= 12 and time.hour < 24:
    hr = time.hour - 12
    timeStr = time.strftime(month + "/" + day + "/" + year + " " + str(hr) + ":%M PM")

requests = []
req = {
    "user": owner,
    "title": "Hospital Requires Respirators",
    "quan": "7",
    "type": "N95 Respirators",
    "date": timeStr
}
requests.append(req)
req2 = {
    "user": owner,
    "title": "I Need Masks",
    "quan": "24",
    "type": "Surgical Masks",
    "date": timeStr
}
requests.append(req2)

@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
def index():
    global requests
    global users

    if request.method == "POST" and "currentUser" in session:
        req = {
            "user": session["currentUser"],
            "title": request.form["item_name"],
            "quan": request.form["item_quantity"],
            "type": request.form["type"],
            "date": getCurrentTime()
        }

        if len(req["title"]) == 0:
            print("Please enter a valid request title!")
            #flash("Please enter a valid request title!")

        if len(req["quan"]) == 0:
            print("Please enter a valid description!")
            #flash("Please enter a valid description!")

        
        requests.append(req)

        return render_template("index.html")
    else:
        return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    global requests
    global users

    if request.method == "POST":
        # Get login form data

        newUser = {
            "email": request.form["em"],
            "password": request.form["pw"]
        }

        accountMatch = False

        for user in users:
            if newUser.get("email") == user.get("email") and newUser.get("password") == user.get("password"):
                session["currentUser"] = user
                #session["isLoggedIn"] = True
                accountMatch = True

        if accountMatch:
            return redirect(url_for('index'))
        else:
            flash("Incorrect email or password!")
            return render_template("login.html")
        
    elif "currentUser" in session:
        return redirect(url_for('index'))
    elif request.method == "GET" or "currentUser" not in session:
        return render_template("login.html")

@app.route("/mask_info", methods=["GET"])
def mask_info():

    if "currentUser" in session:
        return render_template("mask_info.html")
    elif request.method == "GET" or "currentUser" not in session:
        return render_template("login.html")

@app.route("/virus_info", methods=["GET"])
def virus_info():

    if "currentUser" in session:
        return render_template("virus_info.html")
    elif request.method == "GET" or "currentUser" not in session:
        return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    global requests
    global users

    if request.method == "POST":
        # Get register form data
        
        newUser = {
            "name": request.form["nm"],
            "phone_num": request.form["ph"],
            "email": request.form["em"],
            "password": request.form["pw"]
        }

        errorList = []

        if len(newUser["name"]) == 0:
            errorList.append("name")
            #flash("Please enter your name!")
            #return render_template("register.html")
        
        if len(str(newUser["phone_num"])) == 0:
            errorList.append(("phone number"))
            #flash("Please enter your phone number!")
            #return render_template("register.html")

        if len(newUser["email"]) == 0:
            errorList.append(("email"))
            #flash("Please enter an email!")
            #return render_template("register.html")

        # bob@g.com
        if newUser["email"].find("@") == -1 or newUser["email"].find(".") == -1:
            if "email" not in errorList:
                errorList.append(("email"))
            #flash("Please enter a valid email!")
            #return render_template("register.html")

        if len(newUser["password"]) == 0:
            errorList.append("password")
            #flash("Please enter a password!")
            #return render_template("register.html")

        if len(errorList) > 0:
            errorStr = "Please enter a valid "
            for i in range(len(errorList)):
                if len(errorList) == 1:
                    errorStr += errorList[i] + "."
                    print(errorStr)
                    return render_template("register.html")
                elif len(errorList) == 2:
                    errorStr += errorList[0] + " and " + errorList[1] + "."
                    print(errorStr)
                    return render_template("register.html")
                else:
                    errorStr += errorList[i]

                    if i == len(errorList) - 2:
                        errorStr += ", and "
                    elif i == len(errorList) - 1:
                        errorStr += "."
                    else:
                        errorStr += ", "
            print(errorStr)
            return render_template("register.html")

        accountExists = False

        for user in users:
            if newUser.get("email") == user.get("email"):
                accountExists = True
        
        if not accountExists:
            # 012 345 6789
            phoneNum = str(newUser.get("phone_num"))
            newUser["phone_num"] = "(" + phoneNum[0:3] + ") " + phoneNum[3:6] + " - " + phoneNum[6:]


            users.append(newUser)
            #session["isLoggedIn"] = True
            session["currentUser"] = newUser
            return redirect(url_for('index'))
        else:
            flash("Account with that email exists!")
            return render_template("register.html")
    
    elif "currentUser" in session:
        return redirect(url_for('index'))
    elif request.method == "GET" or "currentUser" not in session:
        return render_template("register.html")

@app.route("/userlist")
def userlist():
    global requests
    global users

    list = ""

    for user in users:
        list += "[Name: " + user.get("name") + ", Phone Number: " + str(user.get("phone_num")) + ", Email: " + user.get("email") + ", Password: " + user.get("password") + "] "

    if len(list) == 0:
        list = "None"

    return list

@app.route("/logout")
def logout():

    #session["isLoggedIn"] = False
    #session["currentUser"] = None
    session.pop("currentUser", None)
    return redirect(url_for("index"), code=302)

@app.route("/mask")
def mask():
    filename = 'mask.webp'
    return send_file(filename, mimetype='image/webp')

@app.route("/cdcmask")
def cdcmask():
    filename = 'cdcmask.png'
    return send_file(filename, mimetype='image/png')

@app.route("/diy")
def diy():
    filename = 'diy.png'
    return send_file(filename, mimetype='image/png')

@app.route("/tshirt")
def tshirt():
    filename = 'tshirt.png'
    return send_file(filename, mimetype='image/png')

@app.route("/map")
def map():
    filename = 'map.png'
    return send_file(filename, mimetype='image/png')

@app.route("/counties")
def counties():
    with open("countyCoords.txt", "r") as f:
        return Response(f.read(), mimetype='text/plain')

# @app.route("/counties")
# def counties():
#     file = "/home/maskshare/mysite/countyCoords.txt"
#     with open(file, "r") as f:
#         return Response(f.read(), mimetype='text/plain')

@app.context_processor
def context_processor():
    global requests
    global users

    isLoggedIn = False
    currentUser = None

    if "currentUser" in session:
        isLoggedIn = True
        currentUser = session["currentUser"]

    return dict(isLoggedIn=isLoggedIn, users=users, currentUser=currentUser, requests=requests)
    #return dict(key='reeE')

def getCurrentTime():
    now = datetime.now()
    time = ""

    month = str(now.month)

    for i in range(len(month)):
        if month[i] == "0":
            month = month[0:i:] + month[i + 1::]
        else:
            break

    day = str(now.day)

    for i in range(len(day)):
        if day[i] == "0":
            day = day[0:i:] + day[i + 1::]
        else:
            break

    year = str(now.year)
    year = year[2:]

    if now.hour == 0:
        time = now.strftime(month + "/" + day + "/" + year + " 12:%M AM")
    elif now.hour > 0 and now.hour < 12:
        time = now.strftime(month + "/" + day + "/" + year + " %H:%M AM")
    elif now.hour == 12:
        time = now.strftime(month + "/" + day + "/" + year + " 12:%M PM")
    elif now.hour >= 12 and now.hour < 24:
        hr = now.hour - 12
        time = now.strftime(month + "/" + day + "/" + year + " " + str(hr) + ":%M PM")

    return time

if __name__ == "__main__":
    app.run(debug=True)
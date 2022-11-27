import os

from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user


from database import User
from database import Offer

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


app = Flask(__name__, static_folder="./static")

app.config["SECRET_KEY"] = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.get(id=int(id))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")


@app.route("/")
def index():
    users = []
    offers = Offer.select()
    size = len(offers)
    for number in range(size):
        user_id = offers[number].user_id
        user = User.get(id=user_id)
        users.append(user)

    return render_template("index.html", users=users, offers=offers, size=size)


@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = User.get(email=email)
    if check_password_hash(user.password, password):
        login_user(user)
        return redirect("/mypage")
    return redirect("/login")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def register():
    name = request.form["name"]
    age = request.form["age"]
    gender = request.form["gender"]
    address = request.form["address"]
    tel = request.form["tel"]
    email = request.form["email"]
    password = request.form["password"]

    User.create(
        name=name,
        age=age,
        gender=gender,
        address=address,
        tel=tel,
        email=email,
        password=generate_password_hash(password, method="sha256"),
    )

    return redirect("/login")


@app.route("/mypage")
# ログイン時しか見れない
@login_required
def mypage():
    return render_template("mypage.html")


@app.route("/offer_form")
def offer():
    return render_template("offer_form.html")


# @login_manager.user_loader
# def load_users():
#     if current_user.is_authenticated():
#         user = current_user.get_id()  # return username in get_id()
#     else:
#         user = None  # or 'some fake value', whatever


@app.route("/offer_form", methods=["POST"])
def offer1():
    example = request.form["example"]
    date = request.form["date"]
    time = request.form["time"]
    place = request.form["place"]
    photo1 = request.files["photo1"]
    photo2 = request.files["photo2"]
    photo3 = request.files["photo3"]
    detail = request.form["detail"]

    user_id = current_user.get_id()

    file_name1 = str(photo1.filename)
    photo1_path = "static/images/" + "01" + file_name1

    file_name2 = str(photo2.filename)
    photo2_path = "static/images/" + "02" + file_name2

    file_name3 = str(photo3.filename)
    photo3_path = "static/images/" + "03" + file_name3

    photo1.save(os.path.join("static/images/", file_name1))
    photo2.save(os.path.join("static/images/", file_name2))
    photo3.save(os.path.join("static/images/", file_name3))

    Offer.create(
        example=example,
        user_id=user_id,
        date=date,
        time=time,
        place=place,
        photo1=photo1_path,
        photo2=photo2_path,
        photo3=photo3_path,
        detail=detail,
    )

    return redirect("/offer_form")


@app.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return redirect("/login")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

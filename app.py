from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

import os
import uuid

app = Flask(__name__)

# ================= CONFIG =================

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "secret123"
)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "sqlite:///database.db"
)

app.config["UPLOAD_FOLDER"] = "static/uploads"

app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# ================= DATABASE =================

db = SQLAlchemy(app)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

# ================= USER TABLE =================

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(
        db.String(120),
        unique=True
    )

    password = db.Column(db.String(200))

# ================= LOVE WEBSITE TABLE =================

class LoveSite(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(db.Integer)

    lover_name = db.Column(db.String(100))

    share_id = db.Column(
        db.String(200),
        unique=True
    )

    images = db.Column(db.Text)

# ================= LOGIN MANAGER =================

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))

# ================= REGISTER =================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        email = request.form.get("email")

        password = request.form.get("password")

        existing = User.query.filter_by(
            email=email
        ).first()

        if existing:
            return "Email already exists"

        hashed = generate_password_hash(password)

        user = User(
            email=email,
            password=hashed
        )

        db.session.add(user)

        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

# ================= LOGIN =================

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")

        password = request.form.get("password")

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            return redirect(
                url_for("history")
            )

        return "Wrong Email or Password"

    return render_template("login.html")

# ================= LOGOUT =================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))

# ================= HISTORY PAGE =================

@app.route("/history")
@login_required
def history():

    sites = LoveSite.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "history.html",
        sites=sites
    )

# ================= CREATE LOVE WEBSITE =================

@app.route("/create", methods=["GET", "POST"])
@login_required
def create():

    if request.method == "POST":

        name = request.form.get("name")

        files = request.files.getlist("photos")

        if len(files) < 3:
            return "Minimum 3 images required"

        saved_files = []

        for file in files:

            if file.filename != "":

                filename = (
                    str(uuid.uuid4())
                    + "_"
                    + secure_filename(file.filename)
                )

                filepath = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )

                file.save(filepath)

                saved_files.append(filename)

        share_id = str(uuid.uuid4())

        site = LoveSite(

            user_id=current_user.id,

            lover_name=name,

            share_id=share_id,

            images=",".join(saved_files)
        )

        db.session.add(site)

        db.session.commit()

        return redirect(

            url_for(
                "love_page",
                share_id=share_id
            )
        )

    return render_template("upload.html")

# ================= SHAREABLE LOVE WEBSITE =================

@app.route("/love/<share_id>")
def love_page(share_id):

    site = LoveSite.query.filter_by(
        share_id=share_id
    ).first()

    if not site:
        return "Link not found"

    images = site.images.split(",")

    return render_template(

        "index.html",

        name=site.lover_name,

        images=images,

        share_link=request.host_url +
        "love/" +
        share_id
    )

# ================= RUN APP =================

if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    port = int(
        os.environ.get("PORT", 8080)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
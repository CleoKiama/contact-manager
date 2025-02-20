from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import mongo
from app.auth import bp
from app.auth.forms import (
    LoginForm,
    ResetPasswordRequestForm,
    ResetPasswordForm,
    RegistrationForm,
)
from app.auth.email import send_password_reset_email
from app.models import User
from urllib.parse import urlparse  # Changed to use Python's built-in urlparse
from werkzeug.security import generate_password_hash


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = {
            "email": form.email.data,
            "password": generate_password_hash(form.password.data),
        }
        if mongo.db.users.find_one({"email": form.email.data}):
            flash("Email already registered")
            return redirect(url_for("auth.register"))
        mongo.db.users.insert_one(user)
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", title="Register", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user_data = mongo.db.users.find_one({"email": form.email.data})
        if user_data and User.check_password(user_data["password"], form.password.data):
            user = User(user_data)
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            if not next_page or urlparse(next_page).netloc != "":
                next_page = url_for("main.index")
            return redirect(next_page)
        flash("Invalid email or password")
    return render_template("auth/login.html", title="Sign In", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user_data = mongo.db.users.find_one({"email": form.email.data})
        if user_data:
            user = User(user_data)
            send_password_reset_email(user)
        flash("Check your email for instructions to reset your password")
        return redirect(url_for("auth.login"))
    return render_template(
        "auth/reset_password_request.html", title="Reset Password", form=form
    )


@bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for("main.index"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        mongo.db.users.update_one(
            {"_id": user.id},
            {"$set": {"password": generate_password_hash(form.password.data)}},
        )
        flash("Your password has been reset.")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html", form=form)

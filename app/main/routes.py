from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import mongo
from app.main import bp
from app.main.forms import ContactForm


@bp.route("/")
@bp.route("/index")
def index():
    return render_template("main/index.html", title="Home")


@bp.route("/add_contact", methods=["GET", "POST"])
@login_required
def add_contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = {
            "user_id": current_user.id,
            "mobile": form.mobile.data,
            "email": form.email.data,
            "address": form.address.data,
            "registration_number": form.registration_number.data,
        }
        mongo.db.contacts.insert_one(contact)
        flash("Contact added successfully!")
        return redirect(url_for("main.index"))
    return render_template("main/add_contact.html", title="Add Contact", form=form)


@bp.route("/search_contact", methods=["GET", "POST"])
@login_required
def search_contact():
    reg_number = request.args.get("registration_number", "")
    contact = None
    if reg_number:
        contact = mongo.db.contacts.find_one(
            {"registration_number": reg_number, "user_id": current_user.id}
        )
    return render_template("main/search_contact.html", contact=contact)

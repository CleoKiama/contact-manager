from bson import ObjectId  # Add this at the top with other imports
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import mongo
from app.main import bp
from app.main.forms import ContactForm
import math


@bp.route("/")
@bp.route("/index")
@login_required
def index():
    page = request.args.get("page", 1, type=int)
    per_page = 12  # Number of contacts per page
    search = request.args.get("search", "")

    # Build the query
    query = {"user_id": current_user.id}
    if search:
        query["$or"] = [
            {"registration_number": {"$regex": search, "$options": "i"}},
            {"email": {"$regex": search, "$options": "i"}},
        ]

    # Get total number of contacts for pagination
    total_contacts = mongo.db.contacts.count_documents(query)
    total_pages = math.ceil(total_contacts / per_page)

    # Get contacts for current page
    contacts = mongo.db.contacts.find(query).skip((page - 1) * per_page).limit(per_page)

    return render_template(
        "main/index.html",
        title="Home",
        contacts=contacts,
        page=page,
        total_pages=total_pages,
        search=search,
    )


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


# Update the edit_contact function:
@bp.route("/edit_contact/<contact_id>", methods=["GET", "POST"])
@login_required
def edit_contact(contact_id):
    try:
        contact = mongo.db.contacts.find_one(
            {"_id": ObjectId(contact_id), "user_id": current_user.id}
        )
    except:
        flash("Invalid contact ID.", "error")
        return redirect(url_for("main.index"))

    if not contact:
        flash("Contact not found.", "error")
        return redirect(url_for("main.index"))

    form = ContactForm()
    if form.validate_on_submit():
        try:
            result = mongo.db.contacts.update_one(
                {"_id": ObjectId(contact_id), "user_id": current_user.id},
                {
                    "$set": {
                        "mobile": form.mobile.data,
                        "email": form.email.data,
                        "address": form.address.data,
                        "registration_number": form.registration_number.data,
                    }
                },
            )
            if result.modified_count:
                flash("Contact updated successfully!", "success")
            else:
                flash("No changes were made.", "info")
            return redirect(url_for("main.index"))
        except Exception as e:
            flash("An error occurred while updating the contact.", "error")

    elif request.method == "GET":
        form.mobile.data = contact.get("mobile")
        form.email.data = contact.get("email")
        form.address.data = contact.get("address")
        form.registration_number.data = contact.get("registration_number")

    return render_template(
        "main/edit_contact.html", title="Edit Contact", form=form, contact=contact
    )


@bp.route("/delete_contact/<contact_id>", methods=["POST"])
@login_required
def delete_contact(contact_id):
    try:
        result = mongo.db.contacts.delete_one(
            {"_id": ObjectId(contact_id), "user_id": current_user.id}
        )
        if result.deleted_count:
            flash("Contact deleted successfully!", "success")
        else:
            flash("Contact not found.", "error")
    except:
        flash("An error occurred while deleting the contact.", "error")

    return redirect(url_for("main.index"))


@bp.route("/search_contact", methods=["GET"])
@login_required
def search_contact():
    reg_number = request.args.get("registration_number", "")
    contact = None
    if reg_number:
        contact = mongo.db.contacts.find_one(
            {"registration_number": reg_number, "user_id": current_user.id}
        )
    return render_template("main/search_contact.html", contact=contact)

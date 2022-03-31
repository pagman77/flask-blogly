"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash, session
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "asdf"


connect_db(app)
db.create_all()

@app.get("/")
def redirect_to_users():
    """ redirects to the list of users """
    return redirect("/users")

@app.get("/users")
def show_users():
    """ query the database and show all users """

    users = User.query.all()

    return render_template("user.html", users = users, title = "Users")

@app.get("/users/new")
def show_add_form():
    """ shows the add form for users """
    return render_template("new-user-form.html", title = "Create New User")

@app.post("/users/new")
def add_user():
    """ add user and redirect to /users """
    first_name = request.form["firstName"]
    last_name = request.form["lastName"]
    img_url = request.form.get("imageURL") or None

    new_user = User(first_name=first_name,last_name=last_name,image_url=img_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")

@app.get("/users/<user_id>")
def show_user(user_id):
    """ show information about the given user """
    user = User.query.get(user_id)

    return render_template("user-detail.html", title = "User Detail", user=user)

@app.get("/users/<user_id>/edit")
def edit_user(user_id):
    """Show the edit page for a user """

    user = User.query.get(user_id)

    return render_template("user-edit.html", title = "Edit a User", user=user)

@app.post("/users/<user_id>/edit")
def process_edit(user_id):
    """processes the edit form and return user to /users page """

    user = User.query.get(user_id)

    user.first_name = request.form["firstName"]
    user.last_name = request.form["lastName"]
    user.image_url = request.form.get("imageURL")

    db.session.commit()

    return redirect("/users")

@app.post("/users/<user_id>/delete")
def delete_user(user_id):
    """ deletes the user """

    user = User.query.get(user_id)
    db.session.delete(user)

    db.session.commit()
    flash("User successfully deleted")


    return redirect("/users")




"""Blogly application."""

from flask import Flask, render_template, redirect, session
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.get("/")
def redirect_to_users():
    """ redirects to the list of users """
    return redirect("/users")

@app.get("/users")
def show_users():
    """ query the database and show all users """
    #User.query.all()

@app.get("/users/new")
def show_add_form():
    """ shows the add form for users """
    return render_template("new-user.html")

@app.post("/users/new")
def add_user():
    """ add user and redirect to /users """
    # asdf = respose[asdf]

    return redirect("/users")

@app.get("/users/<userId>")
def show_user(userId):
    """ show information about the given user """

    #return render_template("xxx.html" user= user)

@app.get("/users/<userId>/edit")
def edit_user(userId):
    """ Show the edit page for a user """

    #return render_template(xxxx)

@app.post("/users/<userId>/edit")
def process_edit(userId):
    """ processes the edit form and return user to /users page """
    # response blah balh
    return redirect("/users")

@app.post("/users/<userId>/delete")
def delete_user(userId):
    """ deletes the user """
    #query for userid find user then delete him

    return redirect("/users")




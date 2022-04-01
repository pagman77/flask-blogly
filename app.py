"""Blogly application."""

from sqlite3 import Timestamp
from flask import Flask, render_template, redirect, request, flash, session
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "asdf"


connect_db(app)
db.create_all()



### USERS ###

@app.get("/")
def redirect_to_users():
    """Redirects to the list of users."""

    return redirect("/users")


@app.get("/users")
def show_users():
    """Query the database and show all users."""

    users = User.query.all()

    return render_template("user.html", users = users, title = "Users")


@app.get("/users/new")
def show_add_form():
    """Shows the add form for users."""

    return render_template("new-user-form.html", title = "Create New User")

@app.post("/users/new")
def add_user():
    """Add user and redirect to /users."""

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    img_url = request.form.get("image-url") or None

    new_user = User(first_name=first_name,last_name=last_name,image_url=img_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.get("/users/<user_id>")
def show_user(user_id):
    """Show information about the given user."""

    user = User.query.get(user_id)
    posts = user.posts

    return render_template("user-detail.html", title = "User Detail", user=user, posts=posts)


@app.get("/users/<user_id>/edit")
def edit_user(user_id):
    """Show the edit page for a user """

    user = User.query.get(user_id)

    return render_template("user-edit.html", title="Edit a User", user=user)


@app.post("/users/<user_id>/edit")
def process_edit(user_id):
    """Processes the edit form and return user to /users page."""

    user = User.query.get(user_id)

    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.image_url = request.form.get("image-url")

    db.session.commit()

    flash("User successfully updated")
    return redirect("/users")


@app.post("/users/<user_id>/delete")
def delete_user(user_id):
    """Deletes user posts, deletes the user."""

    user = User.query.get(user_id)

    Post.query.filter_by(user_id=user_id).delete()
    db.session.commit()

    db.session.delete(user)
    db.session.commit()

    flash("User successfully deleted")
    return redirect("/users")

### END USERS ###


### POSTS ###

@app.get("/users/<user_id>/posts/new")
def add_new_post(user_id):
    """Display new post form."""

    user = User.query.get(user_id)

    return render_template("new-post.html", user=user, title= "Create New Post")


@app.post("/users/<user_id>/posts/new")
def commit_new_post(user_id):
    """Commit post to database and redirect."""

    post_title = request.form["post-title"]
    post_content = request.form["post-content"]

    post = Post(title = post_title, content=post_content, user_id = user_id)

    db.session.add(post)
    db.session.commit()

    flash("Post added!")
    return redirect(f"/users/{user_id}")


@app.get("/posts/<post_id>")
def show_post_detail_page(post_id):
    """Shows the post detail page."""

    post = Post.query.get(post_id)

    return render_template("post-detail.html",post=post)


@app.get("/posts/<post_id>/edit")
def show_edit_page(post_id):
    """Show the edit post page."""

    post = Post.query.get(post_id)

    return render_template("edit-post.html", post=post)


@app.post("/posts/<post_id>/edit")
def commit_post_edit(post_id):
    """Commit post edit to database and redirect."""

    post = Post.query.get(post_id)

    post_title = request.form["post-title"]
    post_content = request.form["post-content"]

    post.title = post_title
    post.content = post_content

    db.session.add(post)
    db.session.commit()

    flash("Post Edited")
    return redirect(f"/posts/{post_id}")


@app.post("/posts/<post_id>/delete")
def delete_post(post_id):
    """Delete the post."""

    post = Post.query.get(post_id)
    user_id = post.user_id

    db.session.delete(post)
    db.session.commit()

    flash("Post Deleted")
    return redirect(f"/users/{user_id}")

### END POSTS ###
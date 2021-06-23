from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterUserForm, LoginUserForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


# **********************
#     ROUTING
# **********************
@app.route("/")
def landing_page():
    """Redirects to Register."""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register new user."""

    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("Username taken. Please pick another.")
            return render_template("register.html", form=form)
        session['username'] = new_user.username
        return redirect(f"/users/{new_user.username}")
    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log-in User."""

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ['Invalid username or password']
    
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    """Logout user -> delete session username."""

    session.pop('username')

    return redirect("/")


@app.route("/users/<username>")
def show_user_page(username):
    """View for user page."""

    if 'username' not in session:
        flash("Must be logged in!")
        return redirect("/login")
    else:
        user = User.query.get_or_404(username)
        user_feedback = Feedback.query.filter_by(username=username)
        session_user = session['username']

        return render_template("user-page.html", user=user, user_feedback=user_feedback, session_user=session_user)


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """Show add feedback form and process said form."""

    if 'username' not in session:
        flash("Please login first!")
        return redirect('/')
    if session['username'] != username:
        flash("Not authorized.")
        return redirect('/')

    form = FeedbackForm()
    user = User.query.get_or_404(username)
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Feedback Added')

        return redirect(f'/users/{username}')

    return render_template("add-feedback.html", form=form, user=user)


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    if 'username' not in session:
        flash("Please login first!")
        return redirect('/')
    if session['username'] != username:
        flash("Not authorized.")
        return redirect('/')

    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted.")
    return redirect('/logout')


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    if 'username' not in session:
        flash("Please login first!")
        return redirect('/')
    feedback = Feedback.query.get_or_404(feedback_id)
    if session['username'] != feedback.user.username:
        flash("Not authorized.")
        return redirect('/')

    form = FeedbackForm()
    title = feedback.title
    content = feedback.content

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f"/users/{feedback.user.username}")

    return render_template("edit-feedback.html", title=title, content=content, form=form, feedback_id=feedback_id)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete a piece of feedback."""
    if 'username' not in session:
        flash("Please login first!")
        return redirect('/')
    feedback = Feedback.query.get_or_404(feedback_id)
    if session['username'] != feedback.user.username:
        flash("Not authorized.")
        return redirect('/')
    
    feedback = Feedback.query.get_or_404(feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    flash("Feedback deleted.")
    return redirect(f'/users/{feedback.user.username}')

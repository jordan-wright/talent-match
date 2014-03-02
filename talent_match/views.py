from talent_match import app, db, bcrypt
from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import login_user, login_required, logout_user
from models import User
from forms import LoginForm, RegisterForm


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # Validate the submitted data
    if form.validate_on_submit():
        # Get the user by email address
        user = User.query.filter_by(email=form.email.data).limit(1).first()
        # Check that the user exists, and that the password is correct
        if user and bcrypt.check_password_hash(user.pwd_hash, form.password.data):
            # Log the user in
            login_user(user, remember=True)
            # Redirect to the URL for the index page (will change to profile later)
            return redirect(url_for('index'))
        else:
            flash('Invalid Username/Password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Successfully logged out', 'success')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
<<<<<<< HEAD
    if request.method == "GET":
        return render_template("register.html")
    else:
        # Validate the form
        # Register a user
        pass


@app.route('/profile', methods=['GET', 'POST'])
def prfile():
    return render_template("profile.html")        
=======
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(form.username.data, form.email.data, bcrypt.generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
>>>>>>> FETCH_HEAD


@app.route('/profile', methods=['GET', 'POST'])
def prfile():
    return render_template("profile.html") 

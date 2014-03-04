from talent_match import app, db, bcrypt
from flask import render_template, request, redirect, url_for, flash, g
from flask.ext.login import login_user, login_required, logout_user
from models import User
from forms import LoginForm, RegisterForm, EditProfileForm


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
            next = request.args.get('next')
            if next:
                return redirect(next)
            # Redirect to the URL for the profile page
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
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(form.firstName.data, form.lastName.data, form.username.data, form.email.data, bcrypt.generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template("profile.html") 

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def editProfile():
    form = EditProfileForm()
    if form.validate_on_submit():
        g.user.firstName = form.firstName.data
        g.user.lastName = form.lastName.data
        g.user.quickIntro = form.quickIntro.data
        g.user.background = form.background.data
        g.user.email = form.email.data
        g.user.phoneNumber = form.phoneNumber.data
        g.user.website = form.website.data
        db.session.commit()
        return redirect(url_for('profile'))
    form.quickIntro.data = g.user.quickIntro # or "Default Quick Intro"
    form.background.data = g.user.background 
    return render_template('/edit.html', form=form) 


@app.route('/talents', methods=['GET', 'POST'])
def list():
    user = dict(isAdmin = True, name='Steve', email='test-only-a-test')

    talents = [ dict(name='Harp', category='Music'), dict(name='Flute', category='Music')]
    #form = PickCategoriesForm()
    form = None
    return render_template("talents.html", form=form, talents=talents, user=user)

@app.route('/categories', methods=['GET', 'POST'])
def listTalentCategories():
    user = dict(isAdmin = True, name='Steve', email='test-only-a-test')
    #form = PickCategoriesForm()
    form = None
    categories = [ 'Music', 'Volunteer', 'Software', 'Graphic Design', 'Planning', 'Mechanical Engineering' ]
    return render_template("categories.html", form=form, categories=categories, user=user)

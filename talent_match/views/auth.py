from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from flask.ext.login import login_user, login_required, logout_user

# Project 5 - Steve - Adjusted imports to minimal subset
from ..models.userProfile import  User, Seeker, Provider
from ..forms import LoginForm, RegisterForm, DeleteProfileForm, PasswordResetForm

from talent_match import bcrypt, db
import logging

logger = logging.getLogger(__name__)

app = Blueprint('auth', __name__, template_folder="templates")

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
            return redirect(url_for('profile.profile'))
        else:
            flash('Invalid Username/Password', 'danger')
    return render_template('login.html', form=form)

@login_required
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('Successfully logged out', 'success')
    return redirect(url_for('.login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(form.firstName.data, form.lastName.data, form.username.data, form.email.data, bcrypt.generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()

        ## Project 3: Steve - adding the automatic creation of the seeker, provider objects associated with a user.
        seeker = Seeker(user.id)
        provider = Provider(user.id)
        db.session.add(seeker)
        db.session.add(provider)
        db.session.commit()

        flash('Registration Successful!', 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)

@app.route('/password_reset', methods=['POST'])
@login_required
def change_password():
    form = PasswordResetForm()
    if form.validate_on_submit():
        # Check that the user exists, and that the password is correct
        if bcrypt.check_password_hash(g.user.pwd_hash, form.current_password.data):
            g.user.pwd_hash = bcrypt.generate_password_hash(form.new_password.data)
            db.session.commit()
            # Redirect to the URL for the profile page
            flash('Password updated successfully!', 'success')
            return redirect(url_for('profile.settingsProfile'))
        else:
            flash('Invalid Password', 'danger')
    return render_template('settings.html', password_form=form, delete_form=DeleteProfileForm())

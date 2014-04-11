from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from flask.ext.login import login_user, login_required, logout_user
from ..models import User, Category, Skill, Seeker, Provider, ProviderSkill, Activity, ActivitySkill, Invitation
from ..forms import LoginForm, RegisterForm, EditProfileForm, EditCategoryForm, EditSkillForm, SearchForm, CreateInviteForm, ActivityForm
from talent_match import bcrypt, db
import json

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
from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from flask.ext.login import login_user, login_required, logout_user
from ..models import User, Category, Skill, Seeker, Provider, ProviderSkill, Activity, ActivitySkill, Invitation
from ..forms import LoginForm, RegisterForm, EditProfileForm, EditCategoryForm, EditSkillForm, SearchForm, CreateInviteForm, ActivityForm
from talent_match import db
import json

app = Blueprint('profile', __name__, template_folder="templates", url_prefix="/profile")

@app.route('/', defaults={'username': None}, methods=['GET', 'POST'])
@app.route('/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = g.user
    if username and username != g.user.username:
        user = User.query.filter_by(username=username).first_or_404()

    skills = Skill.query.join(ProviderSkill).join(Provider).join(User).filter(User.id == user.id).all()
    return render_template("profile.html", user=user, skills=skills, gUser=g.user) 

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
        flash('Profile Update Successful!', 'success')
        return redirect(url_for('.profile'))
    form.quickIntro.data = g.user.quickIntro # or "Default Quick Intro"
    return render_template("profile_edit.html", form=form)
    form.background.data = g.user.background
    skills = Skill.query.join(ProviderSkill).join(Provider).join(User).filter(User.id == g.user.id).all()
    return render_template("profile_edit.html", form=form, skills=skills)
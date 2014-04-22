from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from flask.ext.login import login_user, login_required, logout_user
from ..models import User, Category, Skill, Seeker, Provider, ProviderSkill, Activity, ActivitySkill, Invitation
from ..forms import LoginForm, RegisterForm, EditProfileForm, EditCategoryForm, EditSkillForm, SearchForm, CreateInviteForm, ActivityForm, DeleteProfileForm, PasswordResetForm
from talent_match import db
import json
import logging

logger = logging.getLogger(__name__)

app = Blueprint('profile', __name__, template_folder="templates", url_prefix="/profile")

@app.route('/', defaults={'username': None}, methods=['GET', 'POST'])
@app.route('/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = g.user
    if username and username != g.user.username:
        user = User.query.filter_by(username=username).first_or_404()

    # This was the original query; it was replaced so that we could display the "volunteer" flag.
    # skills = Skill.query.join(ProviderSkill).join(Provider).join(User).filter(User.id == user.id).all()
    #
    # Project 4 - minor change to display the volunteer flag.
    skills = ProviderSkill.query.join(Provider).join(User).join(Skill).filter(User.id == user.id, Skill.deleted != True, ProviderSkill.skillID == Skill.id).all()
    return render_template("profile.html", user=user, skills=skills, gUser=g.user, canEditSkills=(user.id==g.user.id), editProfile=False)

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
    form.quickIntro.data = g.user.quickIntro
    #return render_template("profile_edit.html", form=form)
    form.background.data = g.user.background
    # Project 4 - minor change to display the volunteer flag.
    skills = ProviderSkill.query.join(Provider).join(User).join(Skill).filter(g.user.id == User.id, Skill.deleted != True, ProviderSkill.skillID == Skill.id).all()
    return render_template("profile_edit.html", form=form,  user=g.user, skills=skills, editProfile=True)

@app.route('/settings', methods=['GET'])
@login_required
def settingsProfile():
    return render_template('settings.html', delete_form=DeleteProfileForm(), password_form=PasswordResetForm())

@app.route('/delete', methods=['POST'])
@login_required
def deleteProfile():
    form = DeleteProfileForm()
    if form.validate_on_submit():
        # Delete all invitations created by the user
        Invitation.query.filter_by(invitingUserID=g.user.id).delete()
        # Delete all activities and activitySkills owned by the user
        for activity in Activity.query.filter_by(seekerID=g.user.id).all():
            ActivitySkill.query.filter_by(activityID=activity.id).delete()
            db.session.delete(activity)
        # Delete the seeker profile
        db.session.delete(Seeker.query.filter_by(userID=g.user.id).first())
        # Delete the providerSkills
        ProviderSkill.query.filter_by(providerID=g.user.id).delete()
        # Delete the provider profile
        db.session.delete(Provider.query.filter_by(userID=g.user.id).first())
        # Delete the user profile
        db.session.delete(g.user)
        # Commit the changes
        db.session.commit()
        flash('Profile deleted successfully', 'success')
        return redirect(url_for('index.index'))
		
@login_required
@app.route('/edit/skill/', methods=['GET', 'POST'])
def editProviderSkills():
    form = None
    skills = ProviderSkill.query.join(Provider).join(User).join(Skill).filter(g.user.id == User.id, Skill.deleted != True, ProviderSkill.skillID == Skill.id).all()
    return render_template("edit_provider_skill.html", form=form,  user=g.user, skills=skills, userID=g.user.id)

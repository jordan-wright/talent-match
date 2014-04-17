from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from flask.ext.login import login_user, login_required, logout_user
from ..models import User, Category, Skill, Seeker, Provider, ProviderSkill, Activity, ActivitySkill, Invitation
from ..forms import LoginForm, RegisterForm, EditProfileForm, EditCategoryForm, EditSkillForm, SearchForm, CreateInviteForm, ActivityForm
from talent_match import db
import json

app = Blueprint('invites', __name__, template_folder="templates", url_prefix="/invites")

@app.route('/', methods=['GET', 'POST'])
@login_required
def invites():
    invitationList = []
    for invite, active in db.session.query(Invitation, Activity).\
        filter(Invitation.activityID == Activity.id, Invitation.receivingUserID == g.user.id).all():
            newInvite=dict(activityName=active.name, description=active.description, accepted=invite.accepted, id=invite.id)
            invitationList.append(newInvite)

    return render_template("invites.html", invitationList=invitationList)

@app.route('/submit', methods=['GET', 'POST'])
@login_required
def inviteSubmit():
    invitationID = request.values.get('id')
    status = request.values.get('status')
    invitionList = []
    invition = db.session.query(Invitation).filter(Invitation.receivingUserID == g.user.id).all()
    for invites in invition:
        invitionList.append(invites.id)

    if (int(invitationID) in invitionList):
            invitation = None
            newStatus = False
            if (status == '1'): 
                newStatus = True

            if (invitationID != None):
                invitation = Invitation.query.get(invitationID)
                invitation.accepted = newStatus
                db.session.commit()

            flash('Status Has Been Updated!', 'success')
    else:
        flash('Something Went Wrong, Try Again!', 'danger')

    return redirect(url_for('.invites'))

@app.route('/send', methods=['GET', 'POST'])
@login_required
def sendInvite():
    receivingUserID = request.values.get('inviteUserID')
    activityID = request.values.get('activityID')
    skillID = request.values.get('skillID')

    if (inviteUserID and activityID and skillID):
        invitation = Invitation(activityID, skillID, g.user.id, receivingUserID)
        db.session.add(invitation)
        db.session.commit()

    return redirect(url_for('profile.profile(inviteUser.username)'))

@app.route('/create', methods=['GET', 'POST'])
@login_required
def createInvite():
    form = CreateInviteForm()
    inviteUserID = request.values.get('id')
    skillsList = []

    if (inviteUserID != None):
        inviteUser = User.query.get(inviteUserID)
        if (form.activities.choices == None):
            form.activities.choices = db.session.query(Activity).join(Seeker).\
                filter(Activity.seekerID == Seeker.id, Seeker.userID == g.user.id).add_column(Activity.name)
        
        if (form.skills.choices == None):
            providerSkills = db.session.query(Skill).join(ProviderSkill).\
                filter(Provider.userID == inviteUserID, ProviderSkill.skillID == Skill.id , ProviderSkill.providerID == inviteUserID).all()
            for skill in providerSkills:
                 skillsList.append((skill.name, skill.name))
        form.skills.choices = skillsList

    return render_template("invites_create.html", form=form, inviteUser=inviteUser, user=g.user)
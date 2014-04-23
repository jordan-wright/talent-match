from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from flask.ext.login import login_user, login_required, logout_user
from ..models import User, Category, Skill, Seeker, Provider, ProviderSkill, Activity, ActivitySkill, Invitation, InvitationRequest
from ..forms import LoginForm, RegisterForm, EditProfileForm, EditCategoryForm, EditSkillForm, SearchForm, CreateInviteForm, ActivityForm
from talent_match import db
import json
import logging

logger = logging.getLogger(__name__)

app = Blueprint('invites', __name__, template_folder="templates", url_prefix="/invites")


# View all of the invites that the user has
@app.route('/', methods=['GET', 'POST'])
@login_required
def invites():
    invitationList = []
    for invite, active in db.session.query(Invitation, Activity).\
        filter(Invitation.activityID == Activity.id, Invitation.receivingUserID == g.user.id).all():
            newInvite=dict(activityName=active.name, description=active.description, accepted=invite.accepted, id=invite.id,
                           user=invite.invitingUser)  # adding for project 4 - Steve
            invitationList.append(newInvite)

    ## Project 4 - minor changes to allow the same template to display invitations sent and invitations received.
    return render_template("invites.html", invitationList=invitationList, isRecepientRole=True, isRequest=False)

##
## Project 4 - Steve - changes to allow the same template to display invitations sent and invitations received.
## This method requires a logged in user and will accept an optional Activity identifier parameter to filter
## the displayed invitations to a specific Activity.
##
@app.route('/sent', methods=['GET', 'POST'])
@login_required
def invitesFromThisUser():
    invitationList = []
    # Extract the activity ID parameter if present (either by 'id' or 'activityID')
    activityID = request.values.get('id')
    if ( activityID == None):
        activityID = request.values.get('activityID')
    # If the activity ID parameter is present, display only those invitations associated with that activity.
    if (activityID):
        for invite, active in db.session.query(Invitation, Activity).\
            filter(Invitation.activityID == Activity.id, Invitation.invitingUserID == g.user.id, Activity.id == activityID).all():
                newInvite=dict(activityName=active.name, description=active.description, accepted=invite.accepted, id=invite.id, user=invite.receivingUser)
                invitationList.append(newInvite)
    # If no activity ID parameter is present, display all invitations associated with that the user
    else:
        for invite, active in db.session.query(Invitation, Activity).\
            filter(Invitation.activityID == Activity.id, Invitation.invitingUserID == g.user.id).all():
                newInvite=dict(activityName=active.name, description=active.description, accepted=invite.accepted, id=invite.id, user=invite.receivingUser)
                invitationList.append(newInvite)

    return render_template("invites.html", invitationList=invitationList, isRecepientRole=False, isRequest=False)


# Submit a status update for an Accept/Reject
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


@app.route('/view/request', methods=['GET', 'POST'])
@login_required
def viewInviteRequest():
    requestList = []
    for request, active in db.session.query(InvitationRequest, Activity).\
        filter(InvitationRequest.activityID == Activity.id, InvitationRequest.activityUserID == g.user.id, InvitationRequest.accepted == None).all():
            newRequest=dict(activityName=active.name, description=active.description, user=request.requesterUser) 
            requestList.append(newRequest)       

    ## Project 4 - minor changes to allow the same template to display invitations sent and invitations received.
    return render_template("invites.html", invitationList=requestList, isRequest=True)


@app.route('/requests', methods=['GET', 'POST'])
@login_required
def inviteRequests():
    invitationID = request.values.get('inviteID')
    invition = Invitation.query.filter_by(id=invitationID).limit(1).first()
    activity = Activity.query.filter_by(id=invition.activityID).limit(1).first()
    seeker = Seeker.query.filter_by(id=activity.seekerID).limit(1).first()

    if (activity.id and seeker.userID):
        db.session.delete(Invitation.query.filter_by(id=invitationID).first())
        newRequest = InvitationRequest(activity.id, g.user.id, seeker.userID)
        db.session.add(newRequest)
        db.session.commit()
        flash('Request Has Been Sent!', 'success')

    return redirect(url_for('.invites'))


# Create an Invation to send
@app.route('/create', methods=['GET', 'POST'])
@login_required
def createInvite():
    form = CreateInviteForm()
    inviteUserID = request.values.get('id')
    skillsList = []
    activityList = []

    if (inviteUserID != None):
        inviteUser = User.query.get(inviteUserID)
        if (form.activities.choices == None):
            activities = db.session.query(Activity).join(Seeker).\
                filter(Activity.seekerID == Seeker.id, Seeker.userID == g.user.id).all()
            for activity in activities:
                activityList.append((activity.name, activity.name))
        form.activities.choices = activityList
        
        if (form.skills.choices == None):
            providerSkills = db.session.query(Skill).join(ProviderSkill).\
                filter(Provider.userID == inviteUserID, ProviderSkill.skillID == Skill.id , ProviderSkill.providerID == inviteUserID).all()
            for skill in providerSkills:
                 skillsList.append((skill.name, skill.name))
        form.skills.choices = skillsList
        form.inviteUserID.data = inviteUserID

    if (g.user.id == int(inviteUserID)):
        flash('Invitation Cannot Be Sent!', 'danger') 
    elif form.validate_on_submit():
        receivingUser = User.query.filter_by(id=form.inviteUserID.data).limit(1).first()
        activity = Activity.query.filter_by(name=form.activities.data).limit(1).first()
        skill = Skill.query.filter_by(name=form.skills.data).limit(1).first()
        inviteRequest = InvitationRequest.query.filter_by(activityID=activity.id, requesterUserID=receivingUser.id, activityUserID=g.user.id, accepted=None).limit(1).first()

        if (receivingUser and activity and skill):
            if (inviteRequest):
                inviteRequest.accepted = True
            invitation = Invitation(activity.id, skill.id, g.user.id, receivingUser.id)
            db.session.add(invitation)
            db.session.commit()

            flash('Invitation Has Been Sent!', 'success')
            return redirect(url_for('profile.profile', username=receivingUser.username))


    return render_template("invites_create.html", form=form, inviteUser=inviteUser, user=g.user)

# Project 4 - Steve - Cancel an invitation (before it was accepted)
@app.route('/cancel', methods=['GET', 'POST'])
@login_required
def cancelInvite():
    invitationID = request.values.get('id')
    if (invitationID == None):
        invitationID = request.values.get('invitationID')
    if (invitationID != None):
        invitation = Invitation.query.get(invitationID)
        if (invitation):
            db.session.delete(invitation)
            db.session.commit()
    # This is the only location that can cancel an invitation.
    return redirect("/invites/sent")

from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from flask.ext.login import login_user, login_required, logout_user
from ..models import User, Category, Skill, Seeker, Provider, ProviderSkill, Activity, ActivitySkill, Invitation
from ..forms import LoginForm, RegisterForm, EditProfileForm, EditCategoryForm, EditSkillForm, SearchForm, CreateInviteForm, ActivityForm
from talent_match import db
import json

app = Blueprint('activity', __name__, template_folder="templates", url_prefix="/activity")

@app.route('/list', methods=['GET', 'POST'])
@login_required
def listActivityRequests():
    activities = db.session.query(Activity).join(Seeker).\
        filter(Activity.seekerID == Seeker.id, Seeker.userID == g.user.id).all()

    form = None
    return render_template("activity_list.html", activities=activities, user=g.user)

# Project 3 - Steve
# Either create a new activity for the current user or edit an existing activity.
#
# Example: /activity/edit?id=4      (edit)
# Example: /activity/edit           (create)
#
@login_required
@app.route('/edit', methods=['GET', 'POST'])
def editActivity():
    print(request)
    isAddActivity = True # assume add to start
    activityID = None
    form = ActivityForm()

    # Validate the submitted data
    if form.validate_on_submit():
        print(form.data)

        isCreate = False # initialization
        name = form.name.data
        description = form.description.data
        beginDate = form.beginDate.data
        endDate = form.endDate.data
        user = g.user
        activity = None

        if (form.id.data == ''):
            isCreate = True
        if (isCreate):
            activity = Activity(name,description,user)
            db.session.add(activity)
        else:
            activity = Activity.query.get(form.id.data)
            activity.description = description
            activity.name = name

        if (beginDate):
            activity.beginDate = beginDate
            form.beginDate.data = activity.beginDate
        if (endDate):
            activity.endDate = endDate
            form.endDate.data = activity.endDate
        ##
        ## Future: include location, distance
        ##

        # one save for add/update
        db.session.commit()
        form.description.data = activity.description
        form.name.data = activity.name
        form.id.data = activity.id
        form.beginDate.data = activity.beginDate
        form.endDate.data = activity.endDate

        # transition from (or back to) the edit skill view:
        # bug fix: must redirect here to get the appropriate edit/value set in place.
        return redirect('/activity/edit?id=' + str(activity.id))
    else:
        activityID = request.values.get('id')
        activity = None


        if (activityID):
            isAddActivity = False
            activity = Activity.query.get(activityID)

            form.description.data = activity.description
            form.name.data = activity.name
            form.id.data = activity.id

            form.beginDate.data = activity.beginDate
            form.endDate.data = activity.endDate
            ## Future: forZipCode, distance
        else:
            isAddActivity = True
            form.id.data = None

    return render_template("edit_activity.html", activity=activity, form=form, activityID=activityID, isAddActivity=isAddActivity)

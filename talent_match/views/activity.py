import logging

from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from flask.ext.login import login_user, login_required, logout_user

# Project 5 - Steve - adjusting imports to minimal set after model changes.
from talent_match import db
from ..models.userProfile import Seeker, User
from ..models.invitation import Invitation
from ..models.activity import  Activity, ActivityFeedback
from ..forms import ActivityForm, FeedbackForm


logger = logging.getLogger(__name__)

app = Blueprint('activity', __name__, template_folder="templates", url_prefix="/activity")

@app.route('/list', methods=['GET', 'POST'])
@login_required
def listActivityRequests():
    activities = db.session.query(Activity).join(Seeker).\
        filter(Activity.seekerID == Seeker.id, Seeker.userID == g.user.id).all()

    for activity in activities:
        invitationCount = 0
        invitationAcceptedCount = 0

    form = None
    return render_template("activity_list.html", activities=activities, user=g.user)



@app.route('/profile', methods=['GET', 'POST'])
@login_required
def viewActivityProfile():
    activityID = request.values.get('id')
    activity = None
    oldFeedback = None
    isPartOfActivity = False
    sum = 0
    form = FeedbackForm()

    if (form.rating.choices == None):
        form.rating.choices = [('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1')]

    if form.validate_on_submit():
        activity = Activity.query.get(activityID)
        oldFeedback = ActivityFeedback.query.filter_by(activityID=activity.id, feedbackUserID=g.user.id).limit(1).first()
        if (oldFeedback != None):
            db.session.delete(oldFeedback)
            db.session.commit()
        
        seeker = Seeker.query.get(activity.seekerID)
        newFeedback = ActivityFeedback(activity.id, seeker.userID , g.user.id, form.feedback.data, form.rating.data)
        db.session.add(newFeedback)
        db.session.commit()
        form.feedback.data = ''
        flash('Feedback has been posted!', 'success')
    
    if (activityID):
        activity = Activity.query.get(activityID)
        PartOfActivity = Invitation.query.filter_by(activityID = activity.id, receivingUserID = g.user.id, accepted=True).limit(1).first()
        if (PartOfActivity != None):
            isPartOfActivity = True
        feedback = ActivityFeedback.query.filter_by(activityID = activity.id).all()
        feedbackCount = ActivityFeedback.query.filter_by(activityID = activity.id).count()
        for feed in feedback:
            sum += feed.rating
        if (feedbackCount > 0):
            avg = sum/feedbackCount
        else:
            avg = 'N/A'

    return render_template("activity_profile.html", activity=activity, feedback=feedback, form=form, canLeaveFeedback=isPartOfActivity, avgRating=avg)



# Project 3 - Steve
# Either create a new activity for the current user or edit an existing activity.
#
# Example: /activity/edit?id=4      (edit)
# Example: /activity/edit           (create)
#
@login_required
@app.route('/edit', methods=['GET', 'POST'])
def editActivity():
    logging.info(request)
    isAddActivity = True # assume add to start
    activityID = None
    form = ActivityForm()

    # Validate the submitted data
    if form.validate_on_submit():
        logging.info(form.data)

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

            if (activity.beginDate):
                form.beginDate.data = activity.beginDate
            if (activity.endDate):
                form.endDate.data = activity.endDate
            ## Future: forZipCode, distance
        else:
            isAddActivity = True
            form.id.data = None

    return render_template("edit_activity.html", activity=activity, form=form, activityID=activityID, isAddActivity=isAddActivity)


## Project 4 - Steve - Mark activity as complete
#
# Mark an existing activity created by the user as complete.
#
# Example: /activity/complete?id=4
#
@login_required
@app.route('/complete', methods=['GET', 'POST'])
def markActivityAsComplete():

    activityID = request.values.get('id')
    if ( activityID == None):
        activityID = request.values.get('activityID')
    if (activityID):
        activity = Activity.query.get(activityID)
        if (activity):
            activity.completionStatus = True
        db.session.commit()

    return redirect('/activity/list')
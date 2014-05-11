import json
import logging

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask.ext.login import login_required

# Project 5 - Steve - adjusting imports to minimal set after model changes.
from talent_match import db
from ..models.talentInfo import Category, Skill
from ..models.userProfile import User, ProviderSkill
from ..models.activity import Activity, ActivitySkill


logger = logging.getLogger(__name__)
app = Blueprint(
    'api', __name__, template_folder="templates", url_prefix="/api")

# Project 3 - Steve
#
# Return a list of categories in JSON form.
# The data format is designed to be friendly to an Ext.js data store.
#
# Example: /categories/categories.json
#
# Result:
# {
#   'success' : true
#   'message' : 'Loaded data'
#   'data'    :  [ (category data goes here) ]
# }
##
# Project 4 - added what looks like a redundant route, below; however, this may be necessary based
# on recent testing and debugging.  Please do not remove without talking to Steve.
##


@app.route('/categories/categories', methods=['GET'])
@app.route('/categories/categories.json', methods=['GET'])
@app.route('/categories', methods=['GET'])
@app.route('/categories.json', methods=['GET'])
def categoriesAsJson():
    # Project 4 - Steve - adding the deleted filter to remove deleted categories and sort by name.
    #categoryList = Category.query.filter_by(deleted=False).order_by(Category.name).all()
    categoryList = Category.query.filter_by(
        deleted=False).order_by(Category.name).all()
    data = [category.serialize for category in categoryList]
    # Note: we can opt to switch to json.dumps to remove the key sorting if
    # desired.
    result = jsonify(
        {
            "success": True,
            "message": "Loaded data",
            "data": data
        })
    return result

# Project 3 - Steve
#
# Return a list of skills in JSON form.
# The data format is designed to be friendly to an Ext.js data store.
#
# Example: /skills/skills.json?categoryID=1
# Example: /skills/skills.json?id=2
#
# Result:
# {
#   'success' : true
#   'message' : 'Loaded data'
#   'data'    : [ (skill data goes here) ]
# }


@app.route('/skills', methods=['GET', 'POST'])
@app.route('/skills/skills.json', methods=['GET', 'POST'])
def skillsAsJson():
    # To get a list of skills, the caller must provide a category id to filter
    # the skills.
    categoryID = request.values.get('id')
    if (categoryID == None):
        categoryID = request.values.get('categoryID')
    if (categoryID == None):
        return redirect(url_for('index.index'))
    else:
        # Project 4 - Steve - adding the deleted filter to remove deleted
        # categories and sort by name.
        skillList = Skill.query.filter_by(
            categoryID=categoryID, deleted=False).order_by(Skill.name).all()
        # Coerce the result to return an empty array instead of a null.
        if (skillList == None):
            skillList = []
        data = [skill.serialize for skill in skillList]

        result = jsonify({
            "success": True,
            "message": "Loaded data",
            "data": data
        })
        return result

# Project 3 - Steve
# ------------------------------------------------------------------
# For an Ext.js Data Store for an Activity Skill model,
# this provides the appropriate REST endpoint for get 1, put, delete
# ------------------------------------------------------------------


@app.route('/activitySkills/<int:activitySkillID>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/activitySkills/<int:activitySkillID>.json', methods=['GET', 'PUT', 'DELETE'])
def activitySkillInstance(activitySkillID):
    result = json.dumps(
        {
            "success": False,
            "message": "Invalid activity skill ID provided.",
        })

    logging.info(request)
    logging.info(request.data)

    activitySkill = ActivitySkill.query.get(activitySkillID)
    if (activitySkill):
        # read a single ActivitySkill object:
        if request.method == 'GET':
            activitySkillList = [activitySkill]
            data = [
                activitySkill.serialize for activitySkill in activitySkillList]
            result = json.dumps(
                {
                    "success": True,
                    "message": "Loaded data",
                    "data": data
                })
        # Update an existing ActivitySkill object:
        elif request.method == 'PUT':
            # This is similar to the POST (add) code in the next route, below:
            existingSkillString = request.data
            if (existingSkillString):
                # convert the form/input data:
                existingSkillInfo = json.loads(existingSkillString)
                category = Category.query.filter_by(
                    name=existingSkillInfo['category']).first()
                skill = Skill.query.filter_by(
                    categoryID=category.id, name=existingSkillInfo['skill']).first()
                # make the changes and save:
                activitySkill.skillID = skill.id
                db.session.commit()
                # return the serialized object (same as GET, above):
                activitySkillList = [activitySkill]
                data = [
                    activitySkill.serialize for activitySkill in activitySkillList]
                result = json.dumps(
                    {
                        "success": True,
                        "message": "Loaded data",
                        "data": data
                    })
        # Delete an existing ActivitySkill object:
        elif request.method == 'DELETE':
            db.session.delete(activitySkill)
            db.session.commit()
            result = json.dumps(
                {
                    "success": True,
                    "message": "Deleted activity skill"
                })

    return result

# Project 3 - Steve
# ------------------------------------------------------------------------
# For an Ext.js Data Store for an Activity Skill model,
# this provides the appropriate REST endpoint for get many(list), and add
# operations
# ------------------------------------------------------------------------


@app.route('/activitySkills', methods=['GET', 'POST'])
#@app.route('/activitySkills/', methods=['GET', 'POST'])
@app.route('/activitySkills.json')
def activitySkillsAsJson():
    # To get a list of activity skills, the caller must provide the activity ID
    activityID = request.values.get('id')
    if (activityID == None):
        activityID = request.values.get('activityID')
    if (activityID == None):
        return redirect(url_for('index.index'))  # this could be improved

    if request.method == 'POST':
        newSkillString = request.data
        activitySkill = None
        if (newSkillString):
            # this seems to come to us as a string, so we'll convert it back to
            # an object
            newSkill = json.loads(newSkillString)
            result = \
                {
                    "success": False,
                    "message": "Invalid activity skill ID provided.",
                }
            if (newSkill):
                # look up the skill and category
                category = Category.query.filter_by(
                    name=newSkill['category']).first()
                skill = Skill.query.filter_by(
                    categoryID=category.id, name=newSkill['skill']).first()
                activitySkill = ActivitySkill(activityID, skill.id)
                db.session.add(activitySkill)
                db.session.commit()

        if (activitySkill):
            # This should be all that we need to use:
            #data = activitySkill.serialize
            #
            # However, we are re-using the same serialization used in the collection request to try to see if this
            # works better, instead.
            activitySkillList = [activitySkill]
            data = [
                activitySkill.serialize for activitySkill in activitySkillList]

            result = json.dumps(
                {
                    "success": True,
                    "message": "Loaded data",
                    "data": data
                })
        return result

    if request.method == 'GET':
        activity = Activity.query.get(activityID)
        activitySkillList = activity.getActivitySkillList()
        # Coerce the result to return an empty array instead of a null.
        if (activitySkillList == None):
            activitySkillList = []
        data = [activitySkill.serialize for activitySkill in activitySkillList]

        result = json.dumps(
            {
                "success": True,
                "message": "Loaded data",
                "data": data
            })
        return result

# Project 4 - Steve
# ------------------------------------------------------------------
# For an Ext.js Data Store for an Provider Skill model,
# this provides the appropriate REST endpoint for get 1, put, delete
# ------------------------------------------------------------------


@app.route('/providerSkills/<int:providerSkillID>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/providerSkills/<int:providerSkillID>.json', methods=['GET', 'PUT', 'DELETE'])
def providerSkillInstance(providerSkillID):
    result = json.dumps(
        {
            "success": False,
            "message": "Invalid provider skill ID provided.",
        })

    logging.info(request)
    logging.info(request.data)

    providerSkill = ProviderSkill.query.get(providerSkillID)
    if (providerSkill):
        # read a single ActivitySkill object:
        if request.method == 'GET':
            providerSkillList = [providerSkill]
            data = [
                providerSkill.serialize for providerSkill in providerSkillList]
            result = json.dumps(
                {
                    "success": True,
                    "message": "Loaded data",
                    "data": data
                })
        # Update an existing ActivitySkill object:
        elif request.method == 'PUT':
            # This is similar to the POST (add) code in the next route, below:
            existingSkillString = request.data
            if (existingSkillString):
                # convert the form/input data:
                existingSkillInfo = json.loads(existingSkillString)
                category = Category.query.filter_by(
                    name=existingSkillInfo['category']).first()
                skill = Skill.query.filter_by(
                    categoryID=category.id, name=existingSkillInfo['skill']).first()
                # make the changes and save:
                providerSkill.skillID = skill.id
                providerSkill.will_volunteer = existingSkillInfo[
                    'will_volunteer']
                db.session.commit()
                # return the serialized object (same as GET, above):
                providerSkillList = [providerSkill]
                data = [
                    providerSkill.serialize for providerSkill in providerSkillList]
                result = json.dumps(
                    {
                        "success": True,
                        "message": "Loaded data",
                        "data": data
                    })
        # Delete an existing ActivitySkill object:
        elif request.method == 'DELETE':
            db.session.delete(providerSkill)
            db.session.commit()
            result = json.dumps(
                {
                    "success": True,
                    "message": "Deleted activity skill"
                })

    return result

# Project 4 - Steve
# ------------------------------------------------------------------------
# For an Ext.js Data Store for an Activity Skill model,
# this provides the appropriate REST endpoint for get many(list), and add
# operations
# ------------------------------------------------------------------------


@app.route('/providerSkills', methods=['GET', 'POST'])
@app.route('/providerSkills.json')
def providerSkillsAsJson():
    # To get a list of activity skills, the caller must provide the activity ID
    userID = request.values.get('id')
    if (userID == None):
        userID = request.values.get('userID')
    if (userID == None):
        # this could be improved; this is an error
        return redirect(url_for('index.index'))
    user = User.query.get(userID)
    if (not user):
        # this could be improved; this is an error
        return redirect(url_for('index.index'))

    if request.method == 'POST':
        newSkillString = request.data
        providerSkill = None
        if (newSkillString):
            # this seems to come to us as a string, so we'll convert it back to
            # an object
            newSkill = json.loads(newSkillString)
            result = \
                {
                    "success": False,
                    "message": "Invalid activity skill ID provided.",
                }
            if (newSkill):
                # look up the skill and category
                category = Category.query.filter_by(
                    name=newSkill['category']).first()
                skill = Skill.query.filter_by(
                    categoryID=category.id, name=newSkill['skill']).first()
                providerSkill = ProviderSkill()
                providerSkill.skillID = skill.id
                providerSkill.providerID = user.providerProfile.id
                providerSkill.will_volunteer = newSkill['will_volunteer']
                db.session.add(providerSkill)
                db.session.commit()

        if (providerSkill):
            # This should be all that we need to use:
            #data = activitySkill.serialize
            #
            # However, we are re-using the same serialization used in the collection request to try to see if this
            # works better, instead.
            providerSkillList = [providerSkill]
            data = [
                providerSkill.serialize for providerSkill in providerSkillList]

            result = json.dumps(
                {
                    "success": True,
                    "message": "Loaded data",
                    "data": data
                })
        return result

    if request.method == 'GET':
        providerSkillList = user.getProviderSkillList()

        # Coerce the result to return an empty array instead of a null.
        if (providerSkillList == None):
            providerSkillList = []
        data = [providerSkill.serialize for providerSkill in providerSkillList]

        result = json.dumps(
            {
                "success": True,
                "message": "Loaded data",
                "data": data
            })
        return result

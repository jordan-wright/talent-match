from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from flask.ext.login import login_user, login_required, logout_user
from ..models import User, Category, Skill, Seeker, Provider, ProviderSkill, Activity, ActivitySkill, Invitation
from ..forms import LoginForm, RegisterForm, EditProfileForm, EditCategoryForm, EditSkillForm, SearchForm, CreateInviteForm, ActivityForm
from talent_match import db
import json

app = Blueprint('api', __name__, template_folder="templates", url_prefix="/api")

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
@app.route('/categories', methods=['GET'])
@app.route('/categories.json', methods=['GET'])
def categoriesAsJson():
    categoryList = Category.query.all()
    data = [category.serialize for category in categoryList]
    # Note: we can opt to switch to json.dumps to remove the key sorting if desired.
    result = jsonify(
            {
                "success": True,
                "message": "Loaded data",
                "data" : data
            })

    # return jsonify(skills=[skill.serialize for skill in Skill.query.filter(Skill.name.like("%" + query + "%")).all()])
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
    # To get a list of skills, the caller must provide a
    categoryID = request.values.get('id')
    if ( categoryID == None):
        categoryID = request.values.get('categoryID')
    if (categoryID == None):
        return redirect(url_for('index.index'))
    else:
        skillList = Skill.query.filter_by(categoryID=categoryID).all()
        # Coerce the result to return an empty array instead of a null.
        if (skillList == None):
            skillList = []
        data = [skill.serialize for skill in skillList]

        result = jsonify({
            "success": True,
            "message": "Loaded data",
            "data" : data
        })
        return result

# Project 3 - Steve
## ------------------------------------------------------------------
## For an Ext.js Data Store for an Activity Skill model,
## this provides the appropriate REST endpoint for get 1, put, delete
## ------------------------------------------------------------------
@app.route('/activitySkills/<int:activitySkillID>', methods=['GET','PUT','DELETE'])
@app.route('/activitySkills/<int:activitySkillID>.json', methods=['GET','PUT', 'DELETE'])
def activitySkillInstance(activitySkillID):
    result = json.dumps(
    {
        "success": False,
        "message": "Invalid activity skill ID provided.",
    })

    print request
    print request.data


    activitySkill = ActivitySkill.query.get(activitySkillID)
    if (activitySkill):
        # read a single ActivitySkill object:
        if request.method == 'GET':
            activitySkillList = [ activitySkill ]
            data = [activitySkill.serialize for activitySkill in activitySkillList]
            result = json.dumps(
                {
                    "success": True,
                    "message": "Loaded data",
                    "data" : data
                })
        # Update an existing ActivitySkill object:
        elif request.method == 'PUT':
            ## This is similar to the POST (add) code in the next route, below:
            existingSkillString = request.data
            if (existingSkillString):
                # convert the form/input data:
                existingSkillInfo = json.loads(existingSkillString)
                category = Category.query.filter_by(name=existingSkillInfo['category']).first()
                skill = Skill.query.filter_by(categoryID=category.id, name=existingSkillInfo['skill']).first()
                # make the changes and save:
                activitySkill.skillID = skill.id
                db.session.commit()
                # return the serialized object (same as GET, above):
                activitySkillList = [ activitySkill ]
                data = [activitySkill.serialize for activitySkill in activitySkillList]
                result = json.dumps(
                    {
                        "success": True,
                        "message": "Loaded data",
                        "data" : data
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
## ------------------------------------------------------------------------
## For an Ext.js Data Store for an Activity Skill model,
## this provides the appropriate REST endpoint for get many(list), and add
## operations
## ------------------------------------------------------------------------
@app.route('/activitySkills', methods=['GET', 'POST'])
#@app.route('/activitySkills/', methods=['GET', 'POST'])
@app.route('/activitySkills.json')
def activitySkillsAsJson():
    # To get a list of activity skills, the caller must provide the activity ID
    activityID = request.values.get('id')
    if ( activityID == None):
        activityID = request.values.get('activityID')
    if (activityID == None):
        return redirect(url_for('index.index'))  # this could be improved

    if request.method == 'POST':
        newSkillString = request.data
        activitySkill = None
        if (newSkillString):
            # this seems to come to us as a string, so we'll convert it back to an object
            newSkill = json.loads(newSkillString)
            result = \
            {
                "success": False,
                "message": "Invalid activity skill ID provided.",
            }
            if (newSkill):
                # look up the skill and category
                category = Category.query.filter_by(name=newSkill['category']).first()
                skill = Skill.query.filter_by(categoryID=category.id, name=newSkill['skill']).first()
                activitySkill = ActivitySkill(activityID, skill.id)
                db.session.add(activitySkill)
                db.session.commit()

        if (activitySkill):
            # This should be all that we need to use:
            #data = activitySkill.serialize
            #
            # However, we are re-using the same serialization used in the collection request to try to see if this
            # works better, instead.
            activitySkillList = [ activitySkill ]
            data = [activitySkill.serialize for activitySkill in activitySkillList]

            result = json.dumps(
                {
                    "success": True,
                    "message": "Loaded data",
                    "data" : data
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
                "data" : data
            })
        return result
from talent_match import app, db, bcrypt
from flask import render_template, request, redirect, url_for, flash, g, jsonify
from flask.ext.login import login_user, login_required, logout_user
from models import User, Category, Skill, Seeker, Provider, ProviderSkill, Activity, ActivitySkill
from forms import LoginForm, RegisterForm, EditProfileForm, EditCategoryForm, EditSkillForm, SearchForm, ActivityForm
from sqlalchemy.sql import func
from functools import wraps
from config import POSTS_PER_PAGE
import json

def json_default(o):
    return o.__dict__

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not g.user.is_admin:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return render_template('index.html')


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
            return redirect(url_for('profile'))
        else:
            flash('Invalid Username/Password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Successfully logged out', 'success')
    return redirect(url_for('login'))


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
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/profile', defaults={'username': None}, methods=['GET', 'POST'])
@app.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = g.user
    if username and username != g.user.username:
        user = User.query.filter_by(username=username).first_or_404()
    return render_template("profile.html", user=user) 

@app.route('/profile/edit', methods=['GET', 'POST'])
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
        return redirect(url_for('profile'))
    form.quickIntro.data = g.user.quickIntro # or "Default Quick Intro"
    form.background.data = g.user.background 
    return render_template("profile_edit.html", form=form)

@app.route('/search', methods=['GET', 'POST'])
@app.route('/search/<int:page>', methods = ['GET', 'POST'])
@login_required
def search(page = 1): #, setquery = ''):
    form = SearchForm(csrf_enabled=False)
    query = form.query.data or request.values.get('setquery')
    users = User.query.join(Provider).join(ProviderSkill).join(Skill).filter(Skill.name.like("%" + query + "%")).paginate(page, POSTS_PER_PAGE, False)
    return render_template('search.html', query=query, users=users, )


@app.route('/activity/list', methods=['GET', 'POST'])
@login_required
def listActivityRequests():
    activities = db.session.query(Activity).join(Seeker).\
        filter(Activity.seekerID == Seeker.id, Seeker.userID == g.user.id).all()

    form = None
    return render_template("activity_list.html", activities=activities, user=g.user)

@app.route('/skills', methods=['GET', 'POST'])
@admin_required
def listSkills():
    # original test stuff
    # user = dict(isAdmin = True, name='Steve', email='test-only-a-test')
    # talents = [ dict(name='Harp', category='Music'), dict(name='Flute', category='Music')]
    # form = PickCategoriesForm()

    categoryID = request.values.get('categoryID')
    skillList = []
    category = None
    categoryName = None
    categoryFirst = True  # display category first or skill first in the table
    if categoryID:
        print("Looking up skills by categoryID=" + categoryID)
        category = Category.query.get(categoryID)
    if category:
        # show skills for a specific category
        categoryFirst = False   # since the category is fixes, list the skill column first
        myCategoryID = categoryID
        for cat,skill in db.session.query(Category, Skill).\
            filter(Category.id == Skill.categoryID).\
            filter(Skill.categoryID == myCategoryID).all():
                print(cat)
                print(skill)
                newSkill=dict(name=skill.name, categoryName=cat.name, description=skill.description, count='Not available yet',id=skill.id)
                skillList.append(newSkill)

    else:
        # show all skills for all categories
        categoryFirst = True    # for better viewing all skills, put the category column first, then the skill.
        for cat,skill in db.session.query(Category, Skill).\
            filter(Category.id == Skill.categoryID).all():
                newSkill=dict(name=skill.name, categoryName=cat.name, description=skill.description, count='Not available yet', id=skill.id)
                skillList.append(newSkill)

    if (skillList != None):
        skillList.sort(key=lambda test: (test['categoryName'], test['name']))

    form = None
    return render_template("skills.html", form=form, skillList=skillList, user=g.user, categoryName=categoryName, categoryFirst=categoryFirst)

@app.route('/skills/search', methods=['GET', 'POST'])
@login_required
def searchSkills():
    query = request.values.get('query')
    if not query: return redirect(url_for('index'))
    return jsonify(skills=[skill.serialize for skill in Skill.query.filter(Skill.name.like("%" + query + "%")).all()])

@app.route('/categories', methods=['GET', 'POST'])
@admin_required
def listCategories():
    #user = dict(isAdmin = True, name='Steve', email='test-only-a-test')
    #form = PickCategoriesForm()
    form = None

    # original category query
    #categories =  Category.query.all()
    #categories.sort(key= lambda category: category.name)

    # new category query - replacement that includes the count:
    # reminder: may be able to use "from_statement" to utilize 'raw' sql statements
    #
    # This still seems to have a bug with the EmptyCategoryTest (category with no skills).
    # There is something here that will need to be addressed long-term.
    categories = []
    for cat, myCount in db.session.query(Category, func.count('Skill.*')).\
        outerjoin(Skill).\
        group_by(Category).all():
            newCat=dict(id=cat.id, name=cat.name, description=cat.description, count=myCount)
            categories.append(newCat)
    categories.sort(key= lambda category: category['name'])

    return render_template("categories.html", form=form, categories=categories, user=g.user)

@app.route('/categories/edit', methods=['GET', 'POST'])
@admin_required
def editCategory():
    isAddTalent = True # assume add to start
    form = EditCategoryForm()
    # Validate the submitted data
    if form.validate_on_submit():
        print(form.data)
        print(form.name.data)
        print(form.description.data)
        isCreate = False
        if (form.id.data == ''):
            isCreate = True
        if (isCreate):
            category = Category.query.filter_by(name=form.name.data).limit(1).first()
            if (category != None):
                print('existing category error')
                flash('Category already exists', 'error')
                return render_template("edit_category.html", editCategory=None, form=form, isAddTalent=True)
            else:
                category = Category(form.name.data, form.description.data)
                db.session.add(category)
                db.session.commit()
        else:
            category = Category.query.get(form.id.data)
            category.description = form.description.data
            category.name = form.name.data

        db.session.commit()
        return redirect('/categories')
    else:
        categoryID = request.values.get('id')
        category = None
        if categoryID != None:
            isAddTalent = False
            category = Category.query.get(categoryID)
            form.description.data = category.description
            form.id.data = categoryID
        else:
            isAddTalent = True
            form.id.data = None

        return render_template("edit_category.html", editCategory=category, form=form, isAddTalent=isAddTalent)

@app.route('/skills/edit', methods=['GET', 'POST'])
@admin_required
def editSkill():
    print(request)
    dir(request)
    isAddSkill = True # assume add to start
    form = EditSkillForm()

    # There is a better way to do this, but this will work for today.
    if (form.category.choices == None):
        categoryChoices = []
        categoryList = Category.query.all()
        categoryList.sort(key= lambda category: category.name)
        for category in categoryList:
            categoryChoices.append( (category.name, category.name) )
        form.category.choices = categoryChoices

    print('About to check the validation status of the form ...')
    if form.validate_on_submit():
        isCreate = False # initialization
        if (form.id.data == ''):
            isCreate = True
        if (isCreate):
            print(form.category.data)
            category = Category.query.filter_by(name=form.category.data).limit(1).first()
            print(category)
            testSkillName = form.name.data
            print(testSkillName)
            skill = Skill.query.\
                filter_by(categoryID=category.id).\
                filter_by(name=testSkillName).\
                first()
            if (skill != None):
                print('existing skill error')
                flash('Skill already exists', 'error')
                return render_template("edit_skill.html", editSkill=None, form=form, isAddSkill=True)
            else:
                print('trying to add the skill ... ')
                skill = Skill(category.id,testSkillName, form.description.data)
                skill.categoryID = category.id
                db.session.add(skill)
                db.session.commit()
        else:
            testSkillName = form.name.data
            skill = Skill.query.get(form.id.data)
            category = Category.query.get(skill.categoryID)
            ## check to make sure that no other existing skills for this category have the same name as the new name.
            ##otherSkill = Skill.query.\
            ##    filter_by(categoryID=category.id).\
            ##    filter_by(name=testSkillName).\
            ##    filter_by(id!=skill.id).\
            ##    first()
            ##if (skill != None):
            ##    print('existing skill error - name already exists')
            ##    flash('Skill already exists', 'error')
            ##    return render_template("edit_skill.html", editSkill=skill, form=form, isAddSkill=False)
            if (skill) and (category):
                skill.categoryID = category.id
                skill.description = form.description.data
                skill.name = form.name.data
            else:
                print('Error in data - data not saved')

        db.session.commit()
        return redirect('/skills')

    else:
        skillID = request.values.get('id')
        skill = None
        print(request.values)
        if skillID:
            isAddSkill = False
            skill = Skill.query.get(skillID)

            if (skill):
                form.description.data = skill.description
                form.id.data = skill.id

                categoryForExistingSkill = Category.query.get(skill.categoryID)
                if (categoryForExistingSkill):
                    print(skill)
                    print(categoryForExistingSkill)
                    form.category.default = categoryForExistingSkill.name

            else:
                print('GAAAAAHH!!!!!!! This is an error.')
        else:
            print('Add skill?')
            isAddSkill = True
            form.id.data = None

        return render_template("edit_skill.html", editSkill=skill, form=form, isAddSkill=isAddSkill)

# This should be removed with the merge
@login_required
@admin_required
@app.route('/activity/listAll', methods=['GET', 'POST'])
def listAllActivities():
    pass

# Project 3 - Steve
# Either create a new activity for the current user or edit an existing activity.
#
# Example: /activity/edit?id=4      (edit)
# Example: /activity/edit           (create)
#
@login_required
@app.route('/activity/edit', methods=['GET', 'POST'])
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
@app.route('/categories_ds/categories', methods=['GET'])
@app.route('/categories_ds/categories.json', methods=['GET'])
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
@app.route('/skills_ds/skills.json', methods=['GET', 'POST'])
def skillsAsJson():
    # To get a list of skills, the caller must provide a
    categoryID = request.values.get('id')
    if ( categoryID == None):
        categoryID = request.values.get('categoryID')
    if (categoryID == None):
        return redirect(url_for('index'))
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
@app.route('/activity_ds/activitySkills/<int:activitySkillID>', methods=['GET','PUT','DELETE'])
@app.route('/activity_ds/activitySkills/<int:activitySkillID>.json', methods=['GET','PUT', 'DELETE'])
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
@app.route('/activity_ds/activitySkills/', methods=['GET', 'POST'])
def activitySkillsAsJson():
    # To get a list of activity skills, the caller must provide the activity ID
    activityID = request.values.get('id')
    if ( activityID == None):
        activityID = request.values.get('activityID')
    if (activityID == None):
        return redirect(url_for('index'))  # this could be improved

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

# Project 3 - Steve
#
# This is an internal test function to show the skill editing grid for an Activity
# While internal, it can be used to help debug issues if they occur.
#
# Example:
# /activity/test?id=4   where id=the activity ID (key)
#
@app.route('/activity/test2', methods=['GET', 'POST'])
def testSteveExtJsPrototype():
    activityID = 1
    tempID = request.values.get('id')
    if (tempID):
        activityID = tempID
    else:
        tempID = request.values.get('activityID')
        if (tempID):
            activityID = tempID

    return render_template("test2.html", activityID=activityID, temp="Hi Steve This is Steve Again")  # replace this later


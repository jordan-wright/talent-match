from talent_match import app, db, bcrypt
from flask import render_template, request, redirect, url_for, flash, g, jsonify
from flask.ext.login import login_user, login_required, logout_user
from models import User, Category, Skill, Seeker, Provider, ProviderSkill, Activity
from forms import LoginForm, RegisterForm, EditProfileForm, EditCategoryForm, EditSkillForm, SearchForm
from sqlalchemy.sql import func
from functools import wraps
from config import POSTS_PER_PAGE

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
@app.route('/serach/<query>')
@app.route('/search/<query>/<int:page>', methods = ['GET', 'POST'])
@login_required
def search(page = 1): #, setquery = ''):
    form = SearchForm(csrf_enabled=False)
    query = form.query.data or setquery
    users = User.query.join(Provider).join(ProviderSkill).join(Skill).filter(Skill.name.like("%" + query + "%")).paginate(page, POSTS_PER_PAGE, False)
    return render_template('search.html', query=query, users=users, )


@app.route('/activity/requests', methods=['GET', 'POST'])
@login_required
def listActivityRequests():
    activities = db.session.query(Activity).join(Seeker).\
        filter(Activity.seekerID == Seeker.id, Seeker.userID == g.user.id).all()

    form = None
    return render_template("activity_requests.html", activities=activities, user=g.user)




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
            #print(category.name)
            #print(category.description)
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
            #print category.name
            # categoryChoices.append( (category.name, category.id) )
            # categoryChoices.append( (category.id, category.name) )
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
        print('here - in the regular render')

        if (form.errors):
            print(form.errors)
        if form.category.errors:
            print(form.category.errors)
        if form.description.errors:
            print(form.description.errors)
        if form.id.errors:
            print(form.id.errors)
        if form.name.errors:
            print(form.name.errors)

        skillID = request.values.get('id')
        skill = None
        print(request.values)
        if skillID:
            print('Checking the skill ... skip this for now' )
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



        # <!-- {{ form.category(class="form-control", required=true, autofocus=true) }} -->


        return render_template("edit_skill.html", editSkill=skill, form=form, isAddSkill=isAddSkill)
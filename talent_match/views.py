from talent_match import app, db, bcrypt
from flask import render_template, request, redirect, url_for, flash, g
from flask.ext.login import login_user, login_required, logout_user
from models import User, Category, Skill
from forms import LoginForm, RegisterForm, EditProfileForm
from sqlalchemy.sql import func

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
        flash('Registration Successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template("profile.html") 

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
        return redirect(url_for('profile'))
    form.quickIntro.data = g.user.quickIntro # or "Default Quick Intro"
    form.background.data = g.user.background 
    return render_template('/edit.html', form=form) 


@app.route('/skills', methods=['GET', 'POST'])
@login_required
def list():
    # original test stuff
    # user = dict(isAdmin = True, name='Steve', email='test-only-a-test')
    # talents = [ dict(name='Harp', category='Music'), dict(name='Flute', category='Music')]
    # form = PickCategoriesForm()

    categoryID = None
    if (request.args):
        categoryID = request.args['categoryID']
    elif request.form:
        categoryID = request.form['categoryID']
        print('found a post')
    skillList = []
    category = None
    categoryName = None
    categoryFirst = True  # display category first or not.
    if categoryID:
        print("Looking up skills by categoryID=" + categoryID)
        category = Category.query.get(categoryID)
    if category:
        categoryFirst = False
        #print(category)
        #categoryName = category.name
        #skillList = Skill.query.join(Category).\
        #            filter(Category.id == category.id).\
        #            order_by(Category.name).\
        #            order_by(Skill.name).all()

        myCategoryID = categoryID
        for cat,skill in db.session.query(Category, Skill).\
            filter(Category.id == Skill.categoryID).\
            filter(Skill.categoryID == myCategoryID).all():
                print(cat)
                print(skill)
                newSkill=dict(name=skill.name, categoryName=cat.name, description=skill.description, count='Not available yet')
                skillList.append(newSkill)

    else:
        categoryFirst = True
        for cat,skill in db.session.query(Category, Skill).\
            filter(Category.id == Skill.categoryID).all():
                newSkill=dict(name=skill.name, categoryName=cat.name, description=skill.description, count='Not available yet')
                skillList.append(newSkill)

    if (skillList != None):
        skillList.sort(key=lambda test: (test['categoryName'], test['name']))
    #x = dir(skillList[0])
    #print(x)

    form = None
    return render_template("skills.html", form=form, skillList=skillList, user=g.user, categoryName=categoryName, categoryFirst=categoryFirst)

@app.route('/categories', methods=['GET', 'POST'])
@login_required
def listTalentCategories():
    #user = dict(isAdmin = True, name='Steve', email='test-only-a-test')
    #form = PickCategoriesForm()
    form = None

    # original category query
    #categories =  Category.query.all()
    #categories.sort(key= lambda category: category.name)

    # reminder: may be able to use "from_statement" to utilize 'raw' sql statements
    # new category query - replacement that includes the count:
        #filter((Skill.categoryID is None) or (Category.id == Skill.categoryID)).\

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

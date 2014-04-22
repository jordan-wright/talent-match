from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from flask.ext.login import login_user, login_required, logout_user
from ..models import User, Category, Skill, Seeker, Provider, ProviderSkill, Activity, ActivitySkill, Invitation
from ..forms import LoginForm, RegisterForm, EditProfileForm, EditCategoryForm, EditSkillForm, SearchForm, CreateInviteForm, ActivityForm
from functools import wraps
from sqlalchemy.sql import func
from talent_match import db
import json

app = Blueprint('categories', __name__, template_folder="templates", url_prefix="/categories")

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not g.user.is_admin:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/', methods=['GET', 'POST'])
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

    # Project 4 - Steve - bug fix for issue #6 (originally in Project 2)
    # Using this is the fix to get the count correct for an empty category.
    categories = []
    categoryList = Category.query.all()
    for cat in categoryList:
        myCount = 0
        if (cat.skillList):
            myCount = len(cat.skillList)
        categories.append(dict(id=cat.id, name=cat.name, description=cat.description, count=myCount))
    categories.sort(key= lambda category: category['name'])

    return render_template("categories.html", form=form, categories=categories, user=g.user)

@app.route('/edit', methods=['GET', 'POST'])
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
from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from flask.ext.login import login_user, login_required, logout_user
from ..models import User, Category, Skill, Seeker, Provider, ProviderSkill, Activity, ActivitySkill, Invitation, InvitationRequest
from ..forms import LoginForm, RegisterForm, EditProfileForm, EditCategoryForm, EditSkillForm, SearchForm, CreateInviteForm, ActivityForm
from functools import wraps
from talent_match import db
import json
import logging

logger = logging.getLogger(__name__)

app = Blueprint('skills', __name__, template_folder="templates", url_prefix="/skills")

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
                newSkill=dict(name=skill.name, categoryName=cat.name, description=skill.description, count='Not available yet',id=skill.id, deleted=skill.deleted)
                skillList.append(newSkill)

    else:
        # show all skills for all categories
        categoryFirst = True    # for better viewing all skills, put the category column first, then the skill.
        for cat,skill in db.session.query(Category, Skill).\
            filter(Category.id == Skill.categoryID).all():
                newSkill=dict(name=skill.name, categoryName=cat.name, description=skill.description, count='Not available yet', id=skill.id, deleted=skill.deleted)
                skillList.append(newSkill)

    if (skillList != None):
        skillList.sort(key=lambda test: (test['categoryName'], test['name']))

    form = None
    return render_template("skills.html", form=form, skillList=skillList, user=g.user, categoryName=categoryName, categoryFirst=categoryFirst)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def searchSkills():
    query = request.values.get('query')
    if not query: return redirect(url_for('index.index'))
    # Original:
    # return jsonify(skills=[skill.serialize for skill in Skill.query.filter(Skill.name.like("%" + query + "%")).all()])
    ## Project 4 - Steve/Nick - adding a check on the typeahead query to exclude skills from a deleted category.
    return jsonify(skills=[skill.serialize for skill in Skill.query.join(Category).filter(Skill.deleted==False,Category.deleted==False,Skill.name.like("%" + query + "%")).all()])


@app.route('/delete', methods=['GET', 'POST'])
@admin_required
def deleteSkill():
    skillID = request.values.get('id')
    skill = None
    if skillID:
        skill = Skill.query.get(skillID)
        if (skill):
            skill.deleted = True
            db.session.commit()
    # Steve - putting this back to the right filter.
    # return redirect('/skills')
    return redirect('/skills?categoryID=' + str(skill.categoryID))  # Steve - putting this back to the right filter.


@app.route('/restore', methods=['GET', 'POST'])
@admin_required
def restoreSkill():
    skillID = request.values.get('id')
    skill = None
    if skillID:
        skill = Skill.query.get(skillID)
        if (skill):
            skill.deleted = False
            db.session.commit()
    #return redirect('/skills')
    return redirect('/skills?categoryID=' + str(skill.categoryID))  # Steve - putting this back to the right filter.

@app.route('/edit', methods=['GET', 'POST'])
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
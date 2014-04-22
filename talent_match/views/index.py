from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from flask.ext.login import login_user, login_required, logout_user
from ..models import User, Category, Skill, Seeker, Provider, ProviderSkill, Activity, ActivitySkill, Invitation
from ..forms import LoginForm, RegisterForm, EditProfileForm, EditCategoryForm, EditSkillForm, SearchForm, CreateInviteForm, ActivityForm
import json
from talent_match import db
from config import POSTS_PER_PAGE

app = Blueprint('index', __name__, template_folder="templates")

@app.route('/', methods=['GET', 'POST'])
def index():
    if g.user.is_authenticated():
	    pending_invites = db.session.query(Invitation).filter(Invitation.receivingUserID == g.user.id, Invitation.accepted == None).count()
	    return render_template('index.html', invite_count=pending_invites)
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
@app.route('/search/<int:page>', methods = ['GET', 'POST'])
@login_required
def search(page = 1): #, setquery = ''):
    form = SearchForm(csrf_enabled=False)

    query = form.query.data or request.values.get('query')
    users = User.query.join(Provider).join(ProviderSkill).join(Skill).join(Category).filter(Skill.categoryID == Category.id, Category.deleted != True, Skill.deleted != True, Skill.name.like("%" + query + "%")).paginate(page, POSTS_PER_PAGE, False)

    return render_template('search.html', query=query, users=users, gUser=g.user)
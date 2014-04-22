from ..talent_match import app, db, bcrypt
from flask import render_template, request, redirect, url_for, flash, g, jsonify
from flask.ext.login import login_user, login_required, logout_user
from models import User, Category, Skill, Seeker, Provider, ProviderSkill, Activity, ActivitySkill, Invitation, InvitationRequest
from forms import LoginForm, RegisterForm, EditProfileForm, EditCategoryForm, EditSkillForm, SearchForm, CreateInviteForm, ActivityForm
from sqlalchemy.sql import func
from functools import wraps
from config import POSTS_PER_PAGE
import json
import logging

logger = logging.getLogger(__name__)

# Jordan - We can remove this file soon.

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


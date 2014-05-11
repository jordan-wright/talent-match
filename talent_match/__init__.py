from flask import Flask, g
from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.bcrypt import Bcrypt
from flask.ext.login import LoginManager, current_user
from flask.ext.gravatar import Gravatar

# Create the basic Flask application
app = Flask(__name__)
app.config.from_object('config')


# Create the object-to-relational mapping engine for the application
db = SQLAlchemy(app)

# Project 5 - moved this until after the db object was created.
# Note: this should occur here.
from talent_match.models.userProfile import User


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt(app)
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='mm',
                    force_default=False,
                    use_ssl=True,
                    base_url=None)

from talent_match import models, forms
from .views import auth, profile, index, invites, skills, categories, api, activity
from talent_match.startup import addTestData, testLoadFunction

app.createTestData = addTestData
app.testLoadFunction = testLoadFunction

app.register_blueprint(index.app)
app.register_blueprint(activity.app)
app.register_blueprint(auth.app)
app.register_blueprint(profile.app)
app.register_blueprint(invites.app)
app.register_blueprint(skills.app)
app.register_blueprint(categories.app)
app.register_blueprint(api.app)

# Provide the user loader to the login manager


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

# Preprocessing


@app.before_request
def before_request():
        # Set the current_user to the g.user global context variable for use in
        # templates
    g.user = current_user

from flask import Flask, g
from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.bcrypt import Bcrypt
from flask.ext.login import LoginManager, current_user

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt(app)

from talent_match import views, models, forms

def createTestData():
    models.addTestData()
app.createTestData = createTestData

# Provide the user loader to the login manager
@login_manager.user_loader
def user_loader(user_id):
    return models.User.query.get(int(user_id))

# Preprocessing
@app.before_request
def before_request():
	# Set the current_user to the g.user global context variable for use in templates
    g.user = current_user
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, EqualTo

class LoginForm(Form):
	email = TextField('email', validators=[Required()])
	password = PasswordField('password', validators=[Required()])

class RegisterForm(Form):
	username = TextField('username', validators=[Required()])
	email = TextField('email', validators=[Required()])
	password = PasswordField('password', validators=[Required(), EqualTo('confirm_password', message='Passwords must match')])
	confirm_password = PasswordField('confirm_password', validators=[Required()])

class AddCategoryForm(Form):
	category = TextField('category', validators=[Required()])

class AddTalentForm(Form):
	category = TextField('category', validators=[Required()])
	talent = TextField('talent', validators=[Required()])

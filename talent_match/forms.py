from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, IntegerField, SelectField, HiddenField
from wtforms.validators import Required, EqualTo, Length

class LoginForm(Form):
	email = TextField('email', validators=[Required()])
	password = PasswordField('password', validators=[Required()])

class RegisterForm(Form):
	firstName = TextField('firstName', validators=[Required()])
	lastName = TextField('lastName', validators=[Required()])
	username = TextField('username', validators=[Required()])
	email = TextField('email', validators=[Required()])
	password = PasswordField('password', validators=[Required(), EqualTo('confirm_password', message='Passwords must match')])
	confirm_password = PasswordField('confirm_password', validators=[Required()])

class EditCategoryForm(Form):
	name = TextField('Category Name', validators=[Required()])
	description = TextAreaField('Description', validators=[Required()])
	id = HiddenField('id')

class EditSkillForm(Form):
	#category = SelectField(u'Category', coerce=unicode, validators=[Required()])
	category = SelectField(u'Category', validators=[Required()])
	name = TextField('Category Name', validators=[Required()])
	description = TextAreaField('Description')
	id = HiddenField('id')

class EditProfileForm(Form):
	firstName = TextField('firstName')
	lastName = TextField('lastName')
	quickIntro = TextAreaField('quickIntro')
	background = TextAreaField('background')
	email = TextField('email')
	phoneNumber = TextField('phoneNumber', validators=[Length(max=10)])
	website = TextField('website')

class SearchForm(Form):
	query = TextField('query', validators=[Required()])

class CreateInviteForm(Form):
	activities = SelectField(u'Activities', validators=[Required()])
	skills = SelectField(u'Skills', validators=[Required()])
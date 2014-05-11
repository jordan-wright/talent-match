from datetime import date
from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, IntegerField, SelectField, HiddenField
from wtforms import TextField, PasswordField, TextAreaField, IntegerField, SelectField, HiddenField, BooleanField
# Project 5 - Steve - added one new validator for the advanced search.
from wtforms.validators import NumberRange

from wtforms_html5 import DateField #as Html5DateField, DateRange
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

## Project 5 - Steve - adding support for advanced searching.
class AdvancedSearchForm(Form):
	#query is being handled separately and has been removed from this.
	#query = TextField('query', validators=[Required()])
	originZip = IntegerField('originZip', validators=[Required(),NumberRange(1,99999)])
	distanceFrom = IntegerField('distanceFrom', validators=[Required(),NumberRange(1,5000)])
	volunteerOnly = BooleanField('volunteerOnly')
	## This is a placeholder based on peer feedback in class during the Project 4 review.
	## It may not make it into the project 5 release.
	filterOutPastRejections = BooleanField('filterOutPastRejections')
	sortByDistance = BooleanField('sortByDistance')
	sortByProviderRating = BooleanField('sortByProviderRating')

class CreateInviteForm(Form):
	activities = SelectField(u'Activities', validators=[Required()])
	skills = SelectField(u'Skills', validators=[Required()])
	inviteUserID = IntegerField('InviteUserID')

##
## Project 3 - Steve
##
## This is the input form for creating and editing (some) Activity-related data.
## Note that maintaining the skills is actually done with a client side JavaScript component.
##
class ActivityForm(Form):
	id = HiddenField('id')
	name = TextField('Name', validators=[Required()])
	description = TextAreaField('Description')
	beginDate = DateField('Date:', default=date.today()) # validators=[DateRange(date(2000,1,1), date(2050,1,15))])
	endDate = DateField()
	forZipCode = IntegerField('ZIP Code')
	distance = IntegerField('Within X miles')
	# Future candidate fields ...
	#hourDuration = db.Column(db.INTEGER, nullable=True)
    #dayDuration = db.Column(db.INTEGER, nullable=True)
    #monthDuration = db.Column(db.INTEGER, nullable=True)

class DeleteProfileForm(Form):
	pass

class PasswordResetForm(Form):
	current_password = PasswordField('current_password', validators=[Required()])
	new_password = PasswordField('new_password', validators=[Required(), EqualTo('confirm_password', message='Passwords must match')])
	confirm_password = PasswordField('confirm_password', validators=[Required()])

class FeedbackForm(Form):
	rating = SelectField(u'Rating', validators=[Required()])
	feedback = TextAreaField('Feedback', validators=[Required()])

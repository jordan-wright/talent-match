from datetime import date
from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, IntegerField, SelectField, HiddenField, FormField, FieldList
from wtforms_html5 import DateField #as Html5DateField, DateRange
from wtforms.widgets import TableWidget, ListWidget, SubmitInput
from wtforms.validators import Required, EqualTo, Length
from talent_match.models import Activity, ActivitySkill, User, Seeker, Skill, Category


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

"""
https://github.com/wtforms/wtforms/blob/master/tests/widgets.py

from sqlalchemy.ext.declarative import declarative_base
from wtforms_alchemy import ModelForm, ModelFormField, ModelFieldList
DeclarativeBase = declarative_base()

class SkillListForm(ModelForm):
    class Meta:
        model = ActivitySkill

    skill = ModelFormField(EditSkillForm)

"""

"""
class DummyField(object):
    def __init__(self, data, name='f', label='', id='', type='TextField'):
        self.data = data
        self.name = name
        self.label = label
        self.id = id
        self.type = type

    _value = lambda x: x.data
    __unicode__ = lambda x: x.data
    __str__ = lambda x: x.data
    __call__ = lambda x, **k: x.data
    __iter__ = lambda x: iter(x.data)
    iter_choices = lambda x: iter(x.data)

class TableWidgetTest(TestCase):
    def test(self):
        inner_fields = [
            DummyField('hidden1', type='HiddenField'),
            DummyField('foo', label='lfoo'),
            DummyField('bar', label='lbar'),
            DummyField('hidden2', type='HiddenField'),
        ]
        field = DummyField(inner_fields, id='hai')
        self.assertEqual(
            TableWidget()(field),
            '<table id="hai"><tr><th>lfoo</th><td>hidden1foo</td></tr><tr><th>lbar</th><td>bar</td></tr></table>hidden2'
        )
"""

class ActivitySkillRow(Form):
	#category = SelectField(u'Category', validators=[Required()])
	#skill = SelectField(u'Skill', validators=[Required()])
	id = HiddenField('id')
	category = TextField(u'Category', validators=[Required()])
	skill = TextField(u'Skill', validators=[Required()])
	quantity = TextField('Quantity', validators=[Required()])
	invitee =  TextField('Invitee', validators=[Required()])
	inviteeStatus =  TextField('Invitation Status', validators=[Required()])

class ActivityForm(Form):
	#def __init__(self, temp):
	#	self.temp = temp

	id = HiddenField('id')
	name = TextField('Name', validators=[Required()])
	description = TextAreaField('Description')
	beginDate = DateField('Date:', default=date.today()) # validators=[DateRange(date(2000,1,1), date(2050,1,15))])
	endDate = DateField()
	forZipCode = IntegerField('ZIP Code')
	distance = IntegerField('Within X miles')

	activitySkill = FormField(ActivitySkillRow)

	#hourDuration = db.Column(db.INTEGER, nullable=True)
    #dayDuration = db.Column(db.INTEGER, nullable=True)
    #monthDuration = db.Column(db.INTEGER, nullable=True)
	#activitySkill = FieldList(FormField(ActivitySkillRow))
	#activitySkill = FieldList(FormField(ActivitySkillRow))
	#activitySkill = FieldList(FormField(ActivitySkillRow))


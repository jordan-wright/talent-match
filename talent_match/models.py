from talent_match import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    pwd_hash = db.Column(db.String(120))
    is_admin = db.Column(db.Boolean, default=False)
    firstName = db.Column(db.String(80), nullable=True)
    lastName = db.Column(db.String(80), nullable=True)
    city = db.Column(db.String(80), nullable=True, index=True)
    state = db.Column(db.String(16), nullable=True, index=True)
    quickIntro = db.Column(db.String(200), nullable=True)
    background = db.Column(db.String(400), nullable=True)
    phoneNumber = db.Column(db.INTEGER, nullable=True)
    website = db.Column(db.String(120), nullable=True)

    def __init__(self, firstName=None, lastName=None, username=None, email=None, password=None):
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.email = email
        self.pwd_hash = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Provider(db.Model):
    __tablename__ = 'provider'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    is_available = db.Column(db.Boolean, nullable=False, index=True)
    userID = db.Column(db.INTEGER, db.ForeignKey('user.id'), nullable=False)
    skillList = db.relationship(
        'ProviderSkill',
        backref=db.backref('provider', lazy='joined'))
    def __init__(self, userID, is_available=True):
        self.userID = userID
        self.is_available = is_available
    def __repr__(self):
        return 'Talent Provider object'  # for now; should get the user object and return its name

class Seeker(db.Model):
    __tablename__ = 'seeker'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    userID = db.Column(db.INTEGER, db.ForeignKey('user.id'), nullable=True)
    companyID = db.Column(db.INTEGER, db.ForeignKey('company.id'), nullable=True)
    def __init__(self, userID):
        self.userID = userID
    def __repr__(self):
        return 'Talent Seeker object'  # for now; should get the user object and return its name

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    name = db.Column(db.String(80), nullable=False, index=True, unique=True)
    description = db.Column(db.String(256), nullable=True)
    def __init__(self, name, description):
        self.name = name
        self.description = description
    def __repr__(self):
        return 'Category %r' % self.name

# This model object provides additional information in the mapping from a talent Provider to
# a Skill.   Initially, this will include the 'will_volunteer' attribute which can vary
# from provider to provider
class ProviderSkill(db.Model):
    __tablename__ = 'provider_skill'
    # will_volunteer listed in model; however, this is a per individual skill, not the "universal" skill.
    # this needs to be added in the profile => skill mapping table.
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    will_volunteer = db.Column(db.Boolean, default=False)
    # for the one-to-one relationship from ProviderSkill to Skill
    skillID = db.Column(db.INTEGER, db.ForeignKey('skill.id'), nullable=False)
    # for the one-to-many relationship from provider to provider skill
    providerID = db.Column(db.INTEGER, db.ForeignKey('provider.id'), nullable=False)

class Skill(db.Model):
    __tablename__ = 'skill'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    categoryID = db.Column(db.INTEGER, db.ForeignKey('category.id'))
    name = db.Column(db.String(80), nullable=False, index=True, unique=True)
    description = db.Column(db.String(256), nullable=True)
    # will_volunteer listed in model; however, this is a per individual skill, not the "universal" skill.
    # this needs to be added in the profile => skill mapping table.
    def __init__(self, categoryID, name, description):
        self.categoryID = categoryID
        self.name = name
        self.description = description
    def __repr__(self):
        return 'Skill %r' % self.name

class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    name = db.Column(db.String(80), nullable=False, index=True, unique=True)
    description = db.Column(db.String(256), nullable=True)
    beginDate = db.Column(db.DateTime, nullable=True)
    endDate = db.Column(db.DateTime, nullable=True)
    hourDuration = db.Column(db.INTEGER, nullable=True)
    dayDuration = db.Column(db.INTEGER, nullable=True)
    monthDuration = db.Column(db.INTEGER, nullable=True)
    def __init__(self, name, description):
        self.name = name
        self.description = description
    def __repr__(self):
        return 'Activity %r' % self.name

class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    name = db.Column(db.String(80), nullable=False)
    pointOfContact = db.Column(db.String(120), nullable=False)
    is_available = db.Column(db.Boolean, nullable=False, default=False)






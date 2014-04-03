import sys
from talent_match import db

## Project 3:  Steve - adding relationships and navigation
## Adapted from: https://bitbucket.org/zzzeek/sqlalchemy/wiki/UsageRecipes/GenericOrmBaseClass
def modelToString(self) :
    ## changes: in the example, it was "self.c"; replaced "self.c" with an equivalent based on empirical
    ## debugging.
    atts = []
    ## This is not particularly ideal, but it will work for now.
    c = self._sa_class_manager
    for key in c.keys():
            if key in self.__dict__:

                # Steve: adding this safety check.
                keyInfo = c.get(key)
                if (hasattr(keyInfo, 'default')):

                    if not (hasattr(c.get(key).default, 'arg') and
                        getattr(c.get(key).default, 'arg') == getattr(self, key)):
                            atts.append( (key, getattr(self, key)) )

    return self.__class__.__name__ + '(' + ', '.join(x[0] + '=' + repr(x[1]) for x in atts) + ')'

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
    phoneNumber = db.Column(db.String(10), nullable=True)
    website = db.Column(db.String(120), nullable=True)

    ## Project 3:  Steve - adding relationships and navigation
    seekerProfile = db.relationship('Seeker', uselist=False, backref='user')
    ## Project 3:  Steve - adding relationships and navigation
    providerProfile = db.relationship('Provider', uselist=False, backref='user')

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

    ## Project 3:  Steve - adding relationships and navigation
    ## This is a convenience mechanism to avoid having to navigate thru the relationship graph quite as much.
    ## arguments:  the Skill instance, and extra association data
    ##             the extra association data is limited today to the "will_volunteer" flag.
    def addSkill(self, skill, will_volunteer=False):
        if (skill):
            seeker = self.providerProfile

            # delegate to the provider method of the same name.
            return self.providerProfile.addSkill(skill, will_volunteer)


    ## Project 3:  Steve - adding relationships and navigation
    ## This is a convenience mechanism to avoid having to navigate thru the relationship graph quite as much.
    def getProviderSkillList(self):
        result = []

        if (self.providerProfile):
            result = self.providerProfile.getProviderSkillList()

        return result


    ## Project 3:  Steve - adding relationships and navigation
    ## This is a convenience mechanism to avoid having to navigate thru the relationship graph quite as much.
    def addActivity(self, name, description):
        return self.seekerProfile.addActivity(name, description, self)

    ## Project 3:  Steve - adding relationships and navigation
    ## This is a convenience mechanism to avoid having to navigate thru the relationship graph quite as much.
    def getActivityList(self):
        result = []
        if (self.seekerProfile):
            # delegate to the seeker profile object the details of determining this information.
            result = self.seekerProfile.getActivityList()

        return result

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

    ## Project 3:  Steve - adding relationships and navigation
    def hasSkill(self, skill):
        ps = ProviderSkill.query.filter_by(providerID=self.id,skillID=skill.id).first()
        if (ps):
            return True
        else:
           return False

    ## Project 3:  Steve - adding relationships and navigation
    def getProviderSkillList(self):
        result = None
        if (self.skillList):
            result = self.skillList
        return result

    ## Project 3:  Steve - adding relationships and navigation
    ## arguments:  the Skill instance, and extra association data
    ##             the extra association data is limited today to the "will_volunteer" flag.
    def addSkill(self, skill, will_volunteer):
        result = False
        if (skill):

            try:
                # check to see if the skill already exists.
                if (self.hasSkill(skill)):
                    result = False
                else:
                    # set the association class extra attributes:
                    providerSkill = ProviderSkill(will_volunteer)

                    # set the association class keys:
                    providerSkill.providerID = self.id
                    providerSkill.skillID = skill.id

                    # add to database
                    db.session.add(providerSkill)

                    # save the change
                    db.session.commit()
            except:
                exception = sys.exc_info()[0]
                print "Unexpected exception: " + exception
                result = False

        return result

    def __init__(self, userID, is_available=True):
        self.userID = userID
        self.is_available = is_available
    def __repr__(self):
        #return 'Talent Provider object'  # for now; should get the user object and return its name
        return modelToString(self)


class Seeker(db.Model):
    __tablename__ = 'seeker'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    userID = db.Column(db.INTEGER, db.ForeignKey('user.id'), nullable=True)
    companyID = db.Column(db.INTEGER, db.ForeignKey('company.id'), nullable=True)

    ## Project 3:  Steve - adding relationships and navigation
    activityList = db.relationship(
        'Activity',
        backref=db.backref('activity', lazy='joined'))

    ## Project 3:  Steve - adding relationships and navigation
    def addActivity(self, name, description, user):
        result = None
        try:
            activity = Activity(name, description, user)
            db.session.add(activity)
            db.session.commit()
            return activity
        except:
            result = None

    ## Project 3:  Steve - adding relationships and navigation
    def getActivityList(self):
        result = None
        if (self.activityList):
            result = self.activityList
        return result

    def __init__(self, userID):
        self.userID = userID

    def __repr__(self):
        #return 'Talent Seeker object'  # for now; should get the user object and return its name
        return modelToString(self)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    name = db.Column(db.String(80), nullable=False, index=True, unique=True)
    description = db.Column(db.String(256), nullable=True)

    ## Project 3:  Steve - adding relationships and navigation
    skillList = db.relationship('Skill', lazy='joined')

    def __init__(self, name, description):
        self.name = name
        self.description = description
    def __repr__(self):
        if (self.skillList) and (len(self.skillList) > 0):
            return 'Category: ' + self.name + ', description=' + self.description + ', count=' + str(len(self.skillList))
        else:
            return 'Category: ' + self.name + ', description=' + self.description

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

    ## Project 3:  Steve - adding relationships and navigation
    skill = db.relationship('Skill', backref='provider_skill', uselist=False, lazy='joined')

    def __init__(self, will_volunteer=False):
        self.will_volunteer = will_volunteer
    def __repr__(self):
        return modelToString(self)

class Skill(db.Model):
    __tablename__ = 'skill'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    categoryID = db.Column(db.INTEGER, db.ForeignKey('category.id'))
    name = db.Column(db.String(80), nullable=False, index=True, unique=True)
    description = db.Column(db.String(256), nullable=True)

    ## Project 3:  Steve - adding relationships and navigation
    category = db.relationship('Category', backref='skill', uselist=False, lazy='joined')

    def __init__(self, categoryID, name, description):
        self.categoryID = categoryID
        self.name = name
        self.description = description
    def __repr__(self):
        if (self.category):
            return 'Skill: ' + self.name + ', description=' + self.description + ', category=' + self.category.name
        else:
            return 'Skill: ' + self.name + ', description=' + self.description
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description' : self.description
       }

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

    ## Project 3:  Steve - adding relationships and navigation
    seekerID = db.Column(db.INTEGER, db.ForeignKey('seeker.id'), nullable=False)
    """
    # Adding this next bit soon ....
    #
    # per SQL alchemy documentation :  ...  if it has any other columns, such as its own primary key, or foreign keys
    #  to other tables, SQLAlchemy requires a different usage pattern called the association object, described
    # at Association Object (see: http://docs.sqlalchemy.org/en/rel_0_9/orm/relationships.html#association-pattern)
    # activitySkillList = db.relationship("ActivitySkill", backref='activity', lazy='dynamic')
    """
    activitySkillList = db.relationship(
        'ActivitySkill',
        backref=db.backref('activity', lazy='joined'))

    def addSkill(self, skill, quantity = 1, exclusiveResource=True):
        try:
            activitySkill = ActivitySkill(self.id, skill.id, quantity, exclusiveResource)
            db.session.add(activitySkill)
            db.session.commit()
            return True
        except:
            return False

    def getActivitySkillList(self):
        return self.activitySkillList

    def __init__(self, name , description, user):
        self.name = name
        self.description = description
        ## Project 3:  Steve - adding relationships and navigation
        self.seekerID = user.seekerProfile.id
    def __repr__(self):
        return modelToString(self)

class ActivitySkill(db.Model):
    __tablename__ = 'activity_skill'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    activityID = db.Column(db.Integer, db.ForeignKey('activity.id'))
    skillID = db.Column(db.Integer, db.ForeignKey('skill.id'))
    quantity = db.Column(db.INTEGER, nullable=False)
    exclusivePerson = db.Column(db.Boolean, default=True)

    ## Project 3:  Steve - adding relationships and navigation
    ## Note: this is subject to change!
    skill =  db.relationship('Skill', backref='activity_skill', uselist=False, lazy='joined')

    def __init__(self, activityID, skillID, quantity = 1, exclusivePerson=True ):
        self.activityID = activityID
        self.skillID = skillID
        self.quantity = quantity
        self.exclusivePerson = exclusivePerson
        if (quantity == None):
            quantity = 1
    def __repr__(self):
        return modelToString(self)

class Invitation(db.Model):
    __tablename__ = 'invitation'


    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    invitingUserID = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    receivingUserID = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    activityID = db.Column(db.INTEGER, db.ForeignKey('activity.id'))
    skillID = db.Column(db.INTEGER, db.ForeignKey('skill.id'))

    ## Project 3:  Steve - adding relationships and navigation
    skill = db.relationship('Skill', backref='invitation', uselist=False, lazy='joined')
    activity = db.relationship('Activity', backref='invitation', uselist=False, lazy='joined')

    #invitingUser = db.relationship('User', backref='invitation', uselist=False, lazy='joined', foreign_keys=[invitingUserID])
    #receivingUser = db.relationship('User', backref='invitation', uselist=False, lazy='joined', foreign_keys=[receivingUserID])
    invitingUser = db.relationship('User', uselist=False, lazy='joined', foreign_keys=[invitingUserID])
    receivingUser = db.relationship('User', uselist=False, lazy='joined', foreign_keys=[receivingUserID])

    accepted = db.Column(db.Boolean)
    canceled = db.Column(db.Boolean, default=False)

    def __init__(self, activityID, skillID, invitingUserID, receivingUserID):
        self.activityID = invitingUserID
        self.invitingUserID = invitingUserID
        self.receivingUserID = receivingUserID
        self.skillID = skillID

    def __repr__(self):
        return modelToString(self)

class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    name = db.Column(db.String(80), nullable=False)
    pointOfContact = db.Column(db.String(120), nullable=False)
    is_available = db.Column(db.Boolean, nullable=False, default=False)
    def __init__(self):
        pass
    def __repr__(self):
        return modelToString(self)

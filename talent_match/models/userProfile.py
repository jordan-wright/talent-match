import sys
import logging
from talent_match import db
from .modelUtils import modelToString
from .activity import Activity, ActivityFeedback

logger = logging.getLogger(__name__)

##
# This class stores the login and other supporting data for our users.
# It also contains some convenience methods for navigation.
##
##


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
    # Steve - added in Project 4
    zipCode = db.Column(db.INTEGER, nullable=True)
    quickIntro = db.Column(db.String(200), nullable=True)
    background = db.Column(db.String(400), nullable=True)
    phoneNumber = db.Column(db.String(10), nullable=True)
    website = db.Column(db.String(120), nullable=True)

    # Project 5 - Steve - this is placeholder to store feedback summary information.
    # This information is not persisted directly in this model class; however, it may be
    # calculated and passed thru this data member for convenience to help display this information.
    feedbackSummary = dict()

    # Project 5 - Steve - this is placeholder to store distance information.
    # This information is not persisted directly in this model class; however, it may be
    # calculated and passed via this data member for convenience to help display this information.
    distance = 0

    # Project 3:  Steve - adding relationships and navigation
    seekerProfile = db.relationship('Seeker', uselist=False, backref='user')
    # Project 3:  Steve - adding relationships and navigation
    providerProfile = db.relationship(
        'Provider', uselist=False, backref='user')

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

    # Project 3:  Steve - adding relationships and navigation
    # This is a convenience mechanism to avoid having to navigate thru the relationship graph quite as much.
    # arguments:  the Skill instance, and extra association data
    # the extra association data is limited today to the "will_volunteer" flag.
    def addSkill(self, skill, will_volunteer=False):
        if (skill):
            seeker = self.providerProfile

            # delegate to the provider method of the same name.
            return self.providerProfile.addSkill(skill, will_volunteer)

    # Project 3:  Steve - adding relationships and navigation
    # This is a convenience mechanism to avoid having to navigate thru the
    # relationship graph quite as much.
    def getProviderSkillList(self):
        result = []

        if (self.providerProfile):
            result = self.providerProfile.getProviderSkillList()

        return result

    # Project 3:  Steve - adding relationships and navigation
    # This is a convenience mechanism to avoid having to navigate thru the
    # relationship graph quite as much.
    def addActivity(self, name, description):
        return self.seekerProfile.addActivity(name, description, self)

    # Project 3:  Steve - adding relationships and navigation
    # This is a convenience mechanism to avoid having to navigate thru the
    # relationship graph quite as much.
    def getActivityList(self):
        result = []
        if (self.seekerProfile):
            # delegate to the seeker profile object the details of determining
            # this information.
            result = self.seekerProfile.getActivityList()

        return result

    # Project 4: Steve - providing direct access from the user to feedback on
    # this user.
    def getFeedbackReceived(self):
        temp = ActivityFeedback.query.filter_by(reviewedUserID=self.id).all()
        return temp

    # Project 5 - Steve - providing convenience function to tabulate user's overall rating.
    #
    # Returns a dictionary object as a result with 'rating' and 'reviewCount' properties.
    # By default, rating = 0, and reviewCount=0 if no feedback has been provided.
    #
    def getFeedbackSummary(self):
        temp = self.getFeedbackReceived()
        result = dict(rating=0, reviewCount=0)
        if (temp):
            result['reviewCount'] = len(temp)
            if (result['reviewCount'] > 0):
                userRatingsList = [ x.rating for x in temp ]
                result['rating'] = reduce ( lambda x, y : x + y, userRatingsList ) / len (userRatingsList)
                logger.info('User ' + str(self) + ' feedback rating= ' + str(result['rating']))

        return result


    def __repr__(self):
        return '<User %r>' % (self.username)


class Seeker(db.Model):
    __tablename__ = 'seeker'
    id = db.Column(
        db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    userID = db.Column(db.INTEGER, db.ForeignKey('user.id'), nullable=True)
    companyID = db.Column(
        db.INTEGER, db.ForeignKey('company.id'), nullable=True)

    # Project 3:  Steve - adding relationships and navigation
    activityList = db.relationship(
        'Activity',
        backref=db.backref('activity', lazy='joined'))

    # Project 3:  Steve - adding relationships and navigation
    def addActivity(self, name, description, user):
        result = None
        try:
            activity = Activity(name, description, user)
            db.session.add(activity)
            db.session.commit()
            return activity
        except:
            result = None

    # Project 3:  Steve - adding relationships and navigation
    def getActivityList(self):
        result = None
        if (self.activityList):
            result = self.activityList
        return result

    def __init__(self, userID):
        self.userID = userID

    def __repr__(self):
        # return 'Talent Seeker object'  # for now; should get the user object
        # and return its name
        return modelToString(self)


class Provider(db.Model):
    __tablename__ = 'provider'
    id = db.Column(
        db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    is_available = db.Column(db.Boolean, nullable=False, index=True)
    userID = db.Column(db.INTEGER, db.ForeignKey('user.id'), nullable=False)

    skillList = db.relationship(
        'ProviderSkill',
        backref=db.backref('provider', lazy='joined'))

    # Project 3:  Steve - adding relationships and navigation
    def hasSkill(self, skill):
        ps = ProviderSkill.query.filter_by(
            providerID=self.id, skillID=skill.id).first()
        if (ps):
            return True
        else:
            return False

    # Project 3:  Steve - adding relationships and navigation
    def getProviderSkillList(self):
        result = None
        if (self.skillList):
            result = self.skillList
        return result

    # Project 3:  Steve - adding relationships and navigation
    # arguments:  the Skill instance, and extra association data
    # the extra association data is limited today to the "will_volunteer" flag.
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
                logger.info("Unexpected exception: " + exception)
                result = False

        return result

    def __init__(self, userID, is_available=True):
        self.userID = userID
        self.is_available = is_available

    def __repr__(self):
        # return 'Talent Provider object'  # for now; should get the user
        # object and return its name
        return modelToString(self)


class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(
        db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    name = db.Column(db.String(80), nullable=False)
    pointOfContact = db.Column(db.String(120), nullable=False)
    is_available = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self):
        pass

    def __repr__(self):
        return modelToString(self)


# This model object provides additional information in the mapping from a talent Provider to
# a Skill.   Initially, this will include the 'will_volunteer' attribute which can vary
# from provider to provider
##
# This class represents a particular skill or talent for a user or a person seeking talent for an activity.
##
class ProviderSkill(db.Model):
    __tablename__ = 'provider_skill'
    # will_volunteer listed in model; however, this is a per individual skill, not the "universal" skill.
    # this needs to be added in the profile => skill mapping table.
    id = db.Column(
        db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    will_volunteer = db.Column(db.Boolean, default=False)
    # for the one-to-one relationship from ProviderSkill to Skill
    skillID = db.Column(db.INTEGER, db.ForeignKey('skill.id'), nullable=False)
    # for the one-to-many relationship from provider to provider skill
    providerID = db.Column(
        db.INTEGER, db.ForeignKey('provider.id'), nullable=False)

    # Project 3:  Steve - adding relationships and navigation
    skill = db.relationship(
        'Skill', backref='provider_skill', uselist=False, lazy='joined')

    def __init__(self, will_volunteer=False):
        self.will_volunteer = will_volunteer

    def __repr__(self):
        return modelToString(self)

    # Project 4 - Steve - adapting the ActivitySkill serialize to the
    # ProviderSkill class, too.
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'will_volunteer': self.will_volunteer,
            'skillID': self.skill.id,
            'skill': self.skill.name,
            'categoryID': self.skill.categoryID,
            'category': self.skill.category.name,
        }

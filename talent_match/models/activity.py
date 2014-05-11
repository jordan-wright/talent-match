from talent_match import db
from talent_match.models.modelUtils import modelToString

__author__ = 'Steve'


class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column(
        db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    name = db.Column(db.String(80), nullable=False, index=True, unique=True)
    description = db.Column(db.String(256), nullable=True)
    beginDate = db.Column(db.Date, nullable=True)
    endDate = db.Column(db.Date, nullable=True)
    hourDuration = db.Column(db.INTEGER, nullable=True)
    dayDuration = db.Column(db.INTEGER, nullable=True)
    monthDuration = db.Column(db.INTEGER, nullable=True)
    # This may not be used yet.
    seekerStatus = db.Column(db.Boolean)
    # Project 3:  Steve - adding relationships and navigation
    seekerID = db.Column(
        db.INTEGER, db.ForeignKey('seeker.id'), nullable=False)

    # Project 3:  Steve - adding relationships and navigation
    activitySkillList = db.relationship(
        'ActivitySkill',
        backref=db.backref('activity', lazy='joined'))

    # Project 4: Steve - adding preferred ZIP code
    # Note: we could change the default to something based on their current
    # location.
    forZipCode = db.Column(db.INTEGER, default=79401, nullable=False)

    # Project 4: Steve - adding preferred radius in miles
    distanceInMiles = db.Column(db.INTEGER, default=100, nullable=False)

    # Project 4: Steve - adding completion status (boolean)
    completionStatus = db.Column(db.Boolean, default=False, nullable=False)

    def addSkill(self, skill, quantity=1, exclusiveResource=True):
        try:
            activitySkill = ActivitySkill(
                self.id, skill.id, quantity, exclusiveResource)
            db.session.add(activitySkill)
            db.session.commit()
            return True
        except:
            return False

    def getActivitySkillList(self):
        return self.activitySkillList

    def __init__(self, name, description, user):
        self.name = name
        self.description = description
        # Project 3:  Steve - adding relationships and navigation
        self.seekerID = user.seekerProfile.id

    def __repr__(self):
        return modelToString(self)


class ActivityFeedback(db.Model):
    __tablename__ = 'activity_feedback'
    id = db.Column(
        db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    activityID = db.Column(db.INTEGER, db.ForeignKey('activity.id'))
    reviewedUserID = db.Column(db.INTEGER, db.ForeignKey('user.id'))

    # User role is still to be determined; it should track whether the user
    # was a provider or a seeker
    reviewedUserRole = db.Column(db.String, nullable=True)
    feedbackUserID = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    feedbackUserRole = db.Column(db.String, nullable=True)

    # if we use numeric - 1 .. 5 for now?
    rating = db.Column(db.INTEGER, nullable=False)
    review_comments = db.Column(db.String(500), nullable=False)

    reviewedUser = db.relationship(
        'User', uselist=False, lazy='joined', foreign_keys=[reviewedUserID])
    feedbackUser = db.relationship(
        'User', uselist=False, lazy='joined', foreign_keys=[feedbackUserID])
    activity = db.relationship('Activity', uselist=False, lazy='joined')

    def __init__(self, activityID, reviewedUserID, feedbackUserID, review_comments, rating):
        self.activityID = activityID
        self.reviewedUserID = reviewedUserID
        self.feedbackUserID = feedbackUserID
        self.review_comments = review_comments
        self.rating = rating

    def __repr__(self):
        return modelToString(self)


class ActivitySkill(db.Model):
    __tablename__ = 'activity_skill'
    id = db.Column(
        db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    activityID = db.Column(db.Integer, db.ForeignKey('activity.id'))
    skillID = db.Column(db.Integer, db.ForeignKey('skill.id'))
    quantity = db.Column(db.INTEGER, nullable=False)

    # This is being included for now; however, we have made a simplifying assumption for the moment
    # that one person=one activity skill.  This assumption may be changed at a
    # later point in time.
    exclusivePerson = db.Column(db.Boolean, default=True)

    # Project 3:  Steve - adding relationships and navigation
    # Note: this is subject to change!
    skill = db.relationship(
        'Skill', backref='activity_skill', uselist=False, lazy='joined')

    def __init__(self, activityID, skillID, quantity=1, exclusivePerson=True):
        self.activityID = activityID
        self.skillID = skillID
        self.quantity = quantity
        self.exclusivePerson = exclusivePerson
        if (quantity == None):
            quantity = 1

    def __repr__(self):
        return modelToString(self)

    # Project 3: adapting the serialize method from Jordan for the activity
    # list, too.
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'activityID': self.activityID,
            'skillID': self.skill.id,
            'skill': self.skill.name,
            'categoryID': self.skill.categoryID,
            'category': self.skill.category.name,
            'quantity': self.quantity,
            'exclusivePerson': self.exclusivePerson
        }

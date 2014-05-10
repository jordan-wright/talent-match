from talent_match import db
from modelUtils import modelToString

__author__ = 'Steve'

##
## This class represents an invitation from a talent seeker to a talent provider in order to fill the need for a
## a given skill that the provider possesses and the seeker needs for an activity.
##

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
    invitingUser = db.relationship('User', uselist=False, lazy='joined', foreign_keys=[invitingUserID])
    receivingUser = db.relationship('User', uselist=False, lazy='joined', foreign_keys=[receivingUserID])

    accepted = db.Column(db.Boolean)
    canceled = db.Column(db.Boolean, default=False)

    ## Project 4 - Steve - adding a completed column as well.
    completed = db.Column(db.Boolean, default=False, nullable=False)

    ## Project 4 - Steve for Nick, I think - adding a requestSent column as well.
    requestSent = db.Column(db.Boolean, default=False, nullable=True)

    def __init__(self, activityID, skillID, invitingUserID, receivingUserID):

        self.activityID = activityID
        self.invitingUserID = invitingUserID
        self.receivingUserID = receivingUserID
        self.skillID = skillID

    def __repr__(self):
        return modelToString(self)


class InvitationRequest(db.Model):
    __tablename__ = 'invitation_request'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    requesterUserID = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    activityUserID = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    activityID = db.Column(db.INTEGER, db.ForeignKey('activity.id'))
    accepted = db.Column(db.Boolean)


    requesterUser = db.relationship('User', uselist=False, lazy='joined', foreign_keys=[requesterUserID])
    activityUser = db.relationship('User', uselist=False, lazy='joined', foreign_keys=[activityUserID])

    def __init__(self, activityID, requesterUserID, activityUserID):

        self.activityID = activityID
        self.requesterUserID = requesterUserID
        self.activityUserID = activityUserID

    def __repr__(self):
        return modelToString(self)
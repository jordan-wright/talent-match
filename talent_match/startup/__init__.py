
import re
import time
import logging

from talent_match import db

from ..models.talentInfo import Category, Skill
from ..models.userProfile import  Seeker
from ..models.activity import  Activity, ActivityFeedback
from ..models.invitation import Invitation
from ..models.zipCode import USZipCodeToLatitudeLongitude

from talent_match.models.userProfile import User, Provider

logger = logging.getLogger(__name__)

__author__ = 'Steve'

initialized = False

def testLoadFunction():
    addZipCodeData('zipCodeData.txt')
    addInternalTestData()

def addZipCodeData(fileName):
    testZip = USZipCodeToLatitudeLongitude.query.limit(1).all()

    if not testZip:
        #pnotrint (time.strftime("%H:%M:%S"))
        logger.info("DB initialization - adding ZIP code entries.")
        commitInterval = 25
        count = 0

        with open(fileName, "r") as zipCodeFile:
            for zipCodeLine in zipCodeFile:
                # parse the line
                zipCodeEntry = re.split('\t|\n', zipCodeLine)

                # create the new Zip code entry.
                zip = USZipCodeToLatitudeLongitude()
                zip.zipCode= int(zipCodeEntry[0])

                latitude = float(zipCodeEntry[1])
                longitude = float(zipCodeEntry[2])

                # As a reminder, the sql lite database does not natively support numeric SQL data types
                # So, we're using a fixed exponent integer approach to avoid SQL Alchemy complaints.
                # As a side note, it looks like SQL Alchemy will convert values to
                zip.latitudeTimes1000 = (latitude * 1000)
                zip.longitudeTimes1000 = (longitude * 1000)

                zip.latitude = latitude
                zip.longitude = longitude
                zip.locationName = zipCodeEntry[3]
                zip.stateAbbreviation = zipCodeEntry[4]

                db.session.add(zip)

                # Only commit once every commit interval
                #if ((count > 0) and (count % commitInterval == 0)):
                #    db.session.commit()
                #count += 1


            db.session.commit() # last save
            logger.info (time.strftime("%H:%M:%S"))

def addTestData() :
    logger.info('This should not be called anymore.')

def addInternalTestData() :
    userList = None
    userList = User.query.filter_by(is_admin=True)

    categoryList = Category.query.order_by(Category.name)
    skillList = Skill.query.order_by(Skill.name)

    if (userList == None) or (userList.count() < 1):
        logger.info("Adding default user(s)")

        logger.info("Adding user='admin'")
        admin = User()
        admin.is_admin = True; admin.username = 'admin'; admin.email = 'admin@talent-match.us'
        admin.pwd_hash ='$2a$12$5XpK1rXasJv1Zdz7ABxMN.EyHERZ7WqMUjmRQeFALP7LEbrNB8tb2' # admin!
        db.session.add(admin)
        db.session.commit()
        seeker = Seeker(admin.id)
        provider = Provider(admin.id)
        db.session.add(seeker)
        db.session.add(provider)
        db.session.commit()

        logger.info("Adding user='sally'")
        sally = User()
        sally.is_admin = True; sally.username = 'sally'; sally.email = 'sally@talent-match.us'
        sally.pwd_hash ='$2a$12$onbU2C6cjWs16m1RLDOjrObCpP8tLb28RAQeiYAbqE/JjPsGJiDOa' # sally!
        sally.firstName = 'Sally'
        sally.lastName = 'Struthers'
        sally.phoneNumber = '806-555-1212'
        sally.website = 'sallystruthers.com'
        db.session.add(sally)
        db.session.commit()
        sallySeeker = Seeker(sally.id)
        sallyProvider = Provider(sally.id)
        db.session.add(sallySeeker)
        db.session.add(sallyProvider)
        db.session.commit()

        logger.info("Adding user='sally.smith'")
        sally = User()
        sally.is_admin = False; sally.username = 'sally.smith'; sally.email = 'sally.smith@talent-match.us'
        sally.pwd_hash ='$2a$12$onbU2C6cjWs16m1RLDOjrObCpP8tLb28RAQeiYAbqE/JjPsGJiDOa' # sally!
        sally.firstName = 'Sally'
        sally.lastName = 'Smith'
        sally.phoneNumber = '806-555-1212'
        sally.website = 'sally-smith-realty.com'
        db.session.add(sally)
        db.session.commit()

        sallySeeker = Seeker(sally.id)
        sallyProvider = Provider(sally.id)
        db.session.add(sallySeeker)
        db.session.add(sallyProvider)
        db.session.commit()

        logger.info("Adding user='steve'")
        steve = User()
        steve.is_admin = True
        steve.username = 'steve'
        steve.email = 'steve@talent-match.us'
        steve.pwd_hash ='$2a$12$5XpK1rXasJv1Zdz7ABxMN.EyHERZ7WqMUjmRQeFALP7LEbrNB8tb2'  # admin!
        steve.firstName = 'Steve'
        steve.lastName = 'Smith'
        steve.phoneNumber = '806-555-1212'
        steve.website = 'steves-world.com'
        db.session.add(steve)
        db.session.commit()
        steveSeeker = Seeker(steve.id)
        steveProvider = Provider(steve.id)
        db.session.add(steveSeeker)
        db.session.add(steveProvider)
        db.session.commit()


        logger.info("Adding user='sam.smith'")
        sam = User()
        sam.is_admin = False; sam.username = 'sam.smith'; sam.email = 'sam.smith@talent-match.us'
        sam.pwd_hash ='$2a$12$onbU2C6cjWs16m1RLDOjrObCpP8tLb28RAQeiYAbqE/JjPsGJiDOa' 
        sam.firstName = 'Sam'
        sam.lastName = 'Smith'
        sam.phoneNumber = '806-555-1212'
        sam.website = 'sam-smith-realty.com'
        db.session.add(sam)
        db.session.commit()
        samSeeker = Seeker(sam.id)
        samProvider = Provider(sam.id)
        db.session.add(samSeeker)
        db.session.add(samProvider)
        db.session.commit()

        logger.info("Adding user='sammy.smith'")
        sammy = User()
        sammy.is_admin = False; sammy.username = 'sammy.smith'; sammy.email = 'sammy.smith@talent-match.us'
        sammy.pwd_hash ='$2a$12$onbU2C6cjWs16m1RLDOjrObCpP8tLb28RAQeiYAbqE/JjPsGJiDOa' 
        sammy.firstName = 'Sammy'
        sammy.lastName = 'Smith'
        sammy.phoneNumber = '806-555-1212'
        sammy.website = 'sammy-smith-realty.com'
        db.session.add(sammy)
        db.session.commit()
        sammySeeker = Seeker(sammy.id)
        sammyProvider = Provider(sammy.id)
        db.session.add(sammySeeker)
        db.session.add(sammyProvider)
        db.session.commit()


        logger.info("Adding user='mike.smith'")
        mike = User()
        mike.is_admin = False; mike.username = 'mike.smith'; mike.email = 'mike.smith@talent-match.us'
        mike.pwd_hash ='$2a$12$onbU2C6cjWs16m1RLDOjrObCpP8tLb28RAQeiYAbqE/JjPsGJiDOa' 
        mike.firstName = 'Mike'
        mike.lastName = 'Smith'
        mike.phoneNumber = '806-555-1212'
        mike.website = 'mike-smith-realty.com'
        db.session.add(mike)
        db.session.commit()
        mikeSeeker = Seeker(mike.id)
        mikeProvider = Provider(mike.id)
        db.session.add(mikeSeeker)
        db.session.add(mikeProvider)
        db.session.commit()

        logger.info("Adding user='mikey.smith'")
        mikey = User()
        mikey.is_admin = False; mikey.username = 'mikey.smith'; mikey.email = 'mikey.smith@talent-match.us'
        mikey.pwd_hash ='$2a$12$onbU2C6cjWs16m1RLDOjrObCpP8tLb28RAQeiYAbqE/JjPsGJiDOa' 
        mikey.firstName = 'Mikey'
        mikey.lastName = 'Smith'
        mikey.phoneNumber = '806-555-1212'
        mikey.website = 'mikey-smith-realty.com'
        db.session.add(mikey)
        db.session.commit()
        mikeySeeker = Seeker(mikey.id)
        mikeyProvider = Provider(mikey.id)
        db.session.add(mikeySeeker)
        db.session.add(mikeyProvider)
        db.session.commit()
        
    else:
        pass

    if (categoryList == None) or (categoryList.count() < 1):
        categoryList = \
            {
              'Music' :
                  ['Harp', 'Flute', 'Violin', 'Viola', 'Cello', 'Bass', 'Conductor', 'Arranger', 'Composer'],
              'Software' :
                  ['C#', 'F#', 'C++', 'Java', 'User Interface', 'HTML5', 'CSS3', 'Node.js', 'Python', 'Django',
                   'JavaScript', 'ASP.NET', 'SQL'],
              'Graphic Design' :
                  ['Drawing', 'Painting', 'Mixed Media', 'Illustration', 'Adobe Illustrator', 'Typography', 'Adobe Photoshop'],
              'Planning' : # need more details here
                  ['PMP'],
              # partially per wikipedia: http://en.wikipedia.org/wiki/List_of_engineering_branches#Mechanical_engineering
              'Mechanical Engineering' :
                  ['Acoustical', 'Manufacturing', 'Thermal', 'Vehicle', 'Oil/Petroleum', 'Fluid dynamics'],
              'EmptyCategoryTest' : [],
            }
        logger.info("Adding default categories")
        for categoryName in categoryList:
            skillList = categoryList[categoryName]
            category = Category(categoryName, 'no description available')
            db.session.add(category)
            db.session.commit()
            for skillName in skillList:
                skill = Skill(category.id, skillName, 'no skill description available')
                db.session.add(skill)
            # at the end of the skills ... one last commit
            db.session.commit()

        logger.info("Adding a couple of existing skills to our sample users ... ")

        mechEngrCategory = None
        mechSkill = None
        mechEngrCategory = Category.query.filter_by(name = 'Mechanical Engineering').first()
        if (mechEngrCategory != None):
            mechSkill = Skill.query.filter_by(name = 'Thermal').first()

        softwareCategory = None
        softwareSkillHtml5 = None
        softwareSkillCSharp = None
        softwareSkillJava = None
        softwareSkillPython = None
        softwareCategory = Category.query.filter_by(name = 'Software').first()
        if (softwareCategory != None):
            softwareSkillHtml5 = Skill.query.filter_by(name = 'HTML5').first()
            softwareSkillCSharp = Skill.query.filter_by(name = 'C#').first()
            softwareSkillJava = Skill.query.filter_by(name = 'Java').first()
            softwareSkillPython = Skill.query.filter_by(name = 'Python').first()

        logger.info("Checking the new category -> skill relationship ... ")
        if (softwareCategory != None):
            mySkillList = softwareCategory.skillList
            for skill in mySkillList:
                logger.info( skill )
        logger.info("Checking the new skill -> category relationship ... ")
        if (softwareSkillCSharp != None):
            myCategory = softwareSkillCSharp.category
            logger.info(myCategory)

        logger.info("Checking out the sally user ... ")
        user = User.query.filter_by(username='sally.smith').first()
        if (user != None):
            logger.info(user)
            if (user.seekerProfile):
                logger.info(user.seekerProfile)
            else:
                logger.info("No seeker profile found.")
            if (user.providerProfile):
                logger.info(user.providerProfile)
            else:
                logger.info("No provider profile found.")
            if (mechSkill != None):
                # Let's add this skill to our user.
                user.addSkill(mechSkill)

                # Let's add this skill to our user again.   The second time should fail
                if (user.addSkill(mechSkill)):
                    logger.info("Fail - cannot add a skill to the same user twice.")
                else:
                    logger.info("Success - cannot add a skill to the same user twice.")

            if (softwareSkillHtml5 != None):
                # Let's add this skill to our user.
                user.addSkill(softwareSkillHtml5)

        logger.info("Checking out the sam user ... ")
        user = User.query.filter_by(username='sam.smith').first()
        if (user != None):
            logger.info(user)
            if (user.seekerProfile):
                logger.info(user.seekerProfile)
            else:
                logger.info("No seeker profile found.")
            if (user.providerProfile):
                logger.info(user.providerProfile)
            else:
                logger.info("No provider profile found.")
            if (mechSkill != None):
                # Let's add this skill to our user.
                user.addSkill(mechSkill)

                # Let's add this skill to our user again.   The second time should fail
                if (user.addSkill(mechSkill)):
                    logger.info("Fail - cannot add a skill to the same user twice.")
                else:
                    logger.info("Success - cannot add a skill to the same user twice.")

            if (softwareSkillHtml5 != None):
                # Let's add this skill to our user.
                user.addSkill(softwareSkillHtml5)

        logger.info("Checking out the sammy user ... ")
        user = User.query.filter_by(username='sammy.smith').first()
        if (user != None):
            logger.info(user)
            if (user.seekerProfile):
                logger.info(user.seekerProfile)
            else:
                logger.info("No seeker profile found.")
            if (user.providerProfile):
                logger.info(user.providerProfile)
            else:
                logger.info("No provider profile found.")
            if (mechSkill != None):
                # Let's add this skill to our user.
                user.addSkill(mechSkill)

                # Let's add this skill to our user again.   The second time should fail
                if (user.addSkill(mechSkill)):
                    logger.info("Fail - cannot add a skill to the same user twice.")
                else:
                    logger.info("Success - cannot add a skill to the same user twice.")

            if (softwareSkillHtml5 != None):
                # Let's add this skill to our user.
                user.addSkill(softwareSkillHtml5)


        logger.info("Checking out the mike user ... ")
        user = User.query.filter_by(username='mike.smith').first()
        if (user != None):
            logger.info(user)
            if (user.seekerProfile):
                logger.info(user.seekerProfile)
            else:
                logger.info("No seeker profile found.")
            if (user.providerProfile):
                logger.info(user.providerProfile)
            else:
                logger.info("No provider profile found.")
            if (mechSkill != None):
                # Let's add this skill to our user.
                user.addSkill(mechSkill)

                # Let's add this skill to our user again.   The second time should fail
                if (user.addSkill(mechSkill)):
                    logger.info("Fail - cannot add a skill to the same user twice.")
                else:
                    logger.info("Success - cannot add a skill to the same user twice.")

            if (softwareSkillHtml5 != None):
                # Let's add this skill to our user.
                user.addSkill(softwareSkillHtml5)


        logger.info("Checking out the mikey user ... ")
        user = User.query.filter_by(username='mikey.smith').first()
        if (user != None):
            logger.info(user)
            if (user.seekerProfile):
                logger.info(user.seekerProfile)
            else:
                logger.info("No seeker profile found.")
            if (user.providerProfile):
                logger.info(user.providerProfile)
            else:
                logger.info("No provider profile found.")
            if (mechSkill != None):
                # Let's add this skill to our user.
                user.addSkill(mechSkill)

                # Let's add this skill to our user again.   The second time should fail
                if (user.addSkill(mechSkill)):
                    logger.info("Fail - cannot add a skill to the same user twice.")
                else:
                    logger.info("Success - cannot add a skill to the same user twice.")

            if (softwareSkillHtml5 != None):
                # Let's add this skill to our user.
                user.addSkill(softwareSkillHtml5)


        logger.info("Checking out the sally user skill navigation ... ")

        user = User.query.filter_by(username='sally.smith').first()
        sallySkillList = user.getProviderSkillList()
        if (sallySkillList):
            for sallySkill in sallySkillList:
                # This is the provider skill object (association class)
                logger.info(sallySkill)
                skill = sallySkill.skill
                # This is the common/shared skill object.
                logger.info(skill)


        logger.info("Checking out the steve user ... ")
        user = User.query.filter_by(username='steve').first()
        if (user != None):
            logger.info(user)
            if (user.seekerProfile):
                logger.info(user.seekerProfile)
            else:
                logger.info("No seeker profile found.")
            if (user.providerProfile):
                logger.info(user.providerProfile)
            else:
                logger.info("No provider profile found.")
            if (softwareSkillCSharp != None):
                # Let's add this skill to our user.
                user.addSkill(softwareSkillHtml5, False)
            if (softwareSkillJava != None):
                # Let's add this skill to our user.
                user.addSkill(softwareSkillJava, True)

        logger.info("Creating an activity for user='steve'")

        user = User.query.filter_by(username='steve').first()
        activity = user.addActivity('Flask-based Coding Activity', "Need some help for Project 4 in Dr. Mengel's class!")
        if (activity):
            activity.hourDuration = 20
            # activity.beginDate =
            # activity.endDate =
            db.session.commit()

            ## Important Note: we need to look at overlapping skills
            ## so that we can differentiate between 1 person with Python, HTML5 and
            ## 2 people (one with Python, one with HTML5).
            activity.addSkill(softwareSkillPython, 1)
            activity.addSkill(softwareSkillHtml5, 1)

        user = User.query.filter_by(username='steve').first()
        activity = user.addActivity('Flask-based Coding Activity 2', "Need some help for Project 5")
        if (activity):
            activity.hourDuration = 20
            # activity.beginDate =
            # activity.endDate =
            db.session.commit()

            ## Important Note: we need to look at overlapping skills
            ## so that we can differentiate between 1 person with Python, HTML5 and
            ## 2 people (one with Python, one with HTML5).
            activity.addSkill(softwareSkillPython, 1)
            activity.addSkill(softwareSkillHtml5, 1)


        logger.info("Creating an activity for user='sally.smith'")

        user = User.query.filter_by(username='sally.smith').first()
        activity = user.addActivity('Advance Coding Activity', "Need some help for a Coding Project")
        if (activity):
            activity.hourDuration = 20
            # activity.beginDate =
            # activity.endDate =
            db.session.commit()

            ## Important Note: we need to look at overlapping skills
            ## so that we can differentiate between 1 person with Python, HTML5 and
            ## 2 people (one with Python, one with HTML5).
            activity.addSkill(softwareSkillPython, 1)
            activity.addSkill(softwareSkillHtml5, 1)


        user = User.query.filter_by(username='sally.smith').first()
        activity = user.addActivity('Website Coding Activity', "Need some help for coding a website")
        if (activity):
            activity.hourDuration = 20
            # activity.beginDate =
            # activity.endDate =
            db.session.commit()

            ## Important Note: we need to look at overlapping skills
            ## so that we can differentiate between 1 person with Python, HTML5 and
            ## 2 people (one with Python, one with HTML5).
            activity.addSkill(softwareSkillPython, 1)
            activity.addSkill(softwareSkillHtml5, 1)


        user = User.query.filter_by(username='sally.smith').first()
        activity = user.addActivity('Web Page Maintenance', "Need some help for maintaining and updating a web page")
        if (activity):
            activity.hourDuration = 20
            # activity.beginDate =
            # activity.endDate =
            db.session.commit()

            ## Important Note: we need to look at overlapping skills
            ## so that we can differentiate between 1 person with Python, HTML5 and
            ## 2 people (one with Python, one with HTML5).
            activity.addSkill(softwareSkillPython, 1)
            activity.addSkill(softwareSkillHtml5, 1)


        logger.info("Checking the activity navigation ... ")

        user = User.query.filter_by(username='steve').first()
        activityList = user.getActivityList()
        if (activityList):
            # The activity list
            for act in activityList:
                logger.info(act)
                activitySkillList = act.activitySkillList
                if (activitySkillList):
                    for activitySkill in activitySkillList:
                        logger.info(activitySkill)
                        logger.info(activitySkill.skill)
                else:
                    logger.info("Error - activity skill list is empty.")

        # create a test invitation
        #softwareSkillHtml5
        logger.info('Creating a sample invitation')
        invitedUser = User.query.filter_by(username = 'mike.smith').first()
        invitingUser = User.query.filter_by(username='steve').first()
        activity = Activity.query.filter_by(seekerID='4').first()
        invitation = Invitation(activity.id, softwareSkillHtml5.id, invitingUser.id, invitedUser.id)
        db.session.add(invitation)
        db.session.commit()
        invitationID = invitation.id

        invitation = Invitation.query.get(invitationID)
        invitedUser = None
        invitingUser = None
        invitedUser = invitation.receivingUser
        invitingUser = invitation.invitingUser


        invitedUser = User.query.filter_by(username = 'sally.smith').first()
        invitingUser = User.query.filter_by(username='steve').first()
        activity = Activity.query.filter_by(seekerID='4').first()
        invitation = Invitation(activity.id, softwareSkillHtml5.id, invitingUser.id, invitedUser.id)
        db.session.add(invitation)
        db.session.commit()
        invitationID = invitation.id

        invitation = Invitation.query.get(invitationID)
        invitedUser = None
        invitingUser = None
        invitedUser = invitation.receivingUser
        invitingUser = invitation.invitingUser

        logger.info("Checking invitation navigation:")
        if (invitingUser):
            logger.info(invitingUser)
        else:
            logger.info("Invitation navigation failed.")
        if (invitedUser):
            logger.info(invitedUser)
        else:
            logger.info("Invitation navigation failed.")

        ##
        ## Project 4: Adding some test loading for the ActivityFeedback
        ##
        logger.info("Testing feedback creation - reusing last used activity users" )
        logger.info("Trying to create a feedback item - reviewing a talent provider" )
        feedback = ActivityFeedback()
        feedback.activityID = activity.id
        feedback.reviewedUserID = invitedUser.id
        feedback.feedbackUserID = invitingUser.id
        feedback.reviewedUserRole = "seeker"
        feedback.feedbackUserRole = "provider"
        feedback.rating = 5
        feedback.review_comments = "Sally did a great job!"
        db.session.add(feedback)
        db.session.commit()

        logger.info("Trying to create a feedback item - reviewing a talent seeker")
        feedback = ActivityFeedback()
        feedback.activityID = activity.id
        feedback.reviewedUserID = invitingUser.id
        feedback.feedbackUserID = invitedUser.id
        feedback.feedbackUserRole = "seeker"
        feedback.reviewedUserRole = "provider"
        feedback.rating = 3
        feedback.review_comments = "Steve did an okay job; we were paid a little late for our work."
        db.session.add(feedback)
        db.session.commit()

        logger.info("Checking feedback lookup(s) for each user ... ")
        feedbackList = invitingUser.getFeedbackReceived()
        if (feedbackList):
            for feedback in feedbackList:
                logger.info(feedback)

        logger.info("Checking feedback lookup(s) for each user ... ")
        feedbackList = invitedUser.getFeedbackReceived()
        if (feedbackList):
            for feedback in feedbackList:
                logger.info(feedback)











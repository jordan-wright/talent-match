
from talent_match.models import User,Skill,Category,Seeker,Provider,ProviderSkill,Invitation,Activity,ActivitySkill
from talent_match import db

__author__ = 'Steve'

def addTestData() :
    userList = None
    userList = User.query.filter_by(is_admin=True)

    categoryList = Category.query.order_by(Category.name)
    skillList = Skill.query.order_by(Skill.name)

    if (userList == None) or (userList.count() < 1):
        print("Adding default user(s)")

        print("Adding user='admin'")
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

        print("Adding user='sally'")
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

        print("Adding user='sally.smith'")
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

        print("Adding user='steve'")
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


        print("Adding user='sam.smith'")
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

        print("Adding user='sammy.smith'")
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


        print("Adding user='mike.smith'")
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

        print("Adding user='mikey.smith'")
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
        print("Adding default categories")
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

        print("Adding a couple of existing skills to our sample users ... ")

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

        print("Checking the new category -> skill relationship ... ")
        if (softwareCategory != None):
            mySkillList = softwareCategory.skillList
            for skill in mySkillList:
                print( skill )
        print("Checking the new skill -> category relationship ... ")
        if (softwareSkillCSharp != None):
            myCategory = softwareSkillCSharp.category
            print myCategory

        print("Checking out the sally user ... ")
        user = User.query.filter_by(username='sally.smith').first()
        if (user != None):
            print(user)
            if (user.seekerProfile):
                print(user.seekerProfile)
            else:
                print("No seeker profile found.")
            if (user.providerProfile):
                print(user.providerProfile)
            else:
                print("No provider profile found.")
            if (mechSkill != None):
                # Let's add this skill to our user.
                user.addSkill(mechSkill)

                # Let's add this skill to our user again.   The second time should fail
                if (user.addSkill(mechSkill)):
                    print "Fail - cannot add a skill to the same user twice."
                else:
                    print "Success - cannot add a skill to the same user twice."

            if (softwareSkillHtml5 != None):
                # Let's add this skill to our user.
                user.addSkill(softwareSkillHtml5)

        print("Checking out the sam user ... ")
        user = User.query.filter_by(username='sam.smith').first()
        if (user != None):
            print(user)
            if (user.seekerProfile):
                print(user.seekerProfile)
            else:
                print("No seeker profile found.")
            if (user.providerProfile):
                print(user.providerProfile)
            else:
                print("No provider profile found.")
            if (mechSkill != None):
                # Let's add this skill to our user.
                user.addSkill(mechSkill)

                # Let's add this skill to our user again.   The second time should fail
                if (user.addSkill(mechSkill)):
                    print "Fail - cannot add a skill to the same user twice."
                else:
                    print "Success - cannot add a skill to the same user twice."

            if (softwareSkillHtml5 != None):
                # Let's add this skill to our user.
                user.addSkill(softwareSkillHtml5)

        print("Checking out the sammy user ... ")
        user = User.query.filter_by(username='sammy.smith').first()
        if (user != None):
            print(user)
            if (user.seekerProfile):
                print(user.seekerProfile)
            else:
                print("No seeker profile found.")
            if (user.providerProfile):
                print(user.providerProfile)
            else:
                print("No provider profile found.")
            if (mechSkill != None):
                # Let's add this skill to our user.
                user.addSkill(mechSkill)

                # Let's add this skill to our user again.   The second time should fail
                if (user.addSkill(mechSkill)):
                    print "Fail - cannot add a skill to the same user twice."
                else:
                    print "Success - cannot add a skill to the same user twice."

            if (softwareSkillHtml5 != None):
                # Let's add this skill to our user.
                user.addSkill(softwareSkillHtml5)


        print("Checking out the mike user ... ")
        user = User.query.filter_by(username='mike.smith').first()
        if (user != None):
            print(user)
            if (user.seekerProfile):
                print(user.seekerProfile)
            else:
                print("No seeker profile found.")
            if (user.providerProfile):
                print(user.providerProfile)
            else:
                print("No provider profile found.")
            if (mechSkill != None):
                # Let's add this skill to our user.
                user.addSkill(mechSkill)

                # Let's add this skill to our user again.   The second time should fail
                if (user.addSkill(mechSkill)):
                    print "Fail - cannot add a skill to the same user twice."
                else:
                    print "Success - cannot add a skill to the same user twice."

            if (softwareSkillHtml5 != None):
                # Let's add this skill to our user.
                user.addSkill(softwareSkillHtml5)


        print("Checking out the mikey user ... ")
        user = User.query.filter_by(username='mikey.smith').first()
        if (user != None):
            print(user)
            if (user.seekerProfile):
                print(user.seekerProfile)
            else:
                print("No seeker profile found.")
            if (user.providerProfile):
                print(user.providerProfile)
            else:
                print("No provider profile found.")
            if (mechSkill != None):
                # Let's add this skill to our user.
                user.addSkill(mechSkill)

                # Let's add this skill to our user again.   The second time should fail
                if (user.addSkill(mechSkill)):
                    print "Fail - cannot add a skill to the same user twice."
                else:
                    print "Success - cannot add a skill to the same user twice."

            if (softwareSkillHtml5 != None):
                # Let's add this skill to our user.
                user.addSkill(softwareSkillHtml5)


        print("Checking out the sally user skill navigation ... ")

        user = User.query.filter_by(username='sally.smith').first()
        sallySkillList = user.getProviderSkillList()
        if (sallySkillList):
            for sallySkill in sallySkillList:
                # This is the provider skill object (association class)
                print(sallySkill)
                skill = sallySkill.skill
                # This is the common/shared skill object.
                print(skill)


        print("Checking out the steve user ... ")
        user = User.query.filter_by(username='steve').first()
        if (user != None):
            print(user)
            if (user.seekerProfile):
                print(user.seekerProfile)
            else:
                print("No seeker profile found.")
            if (user.providerProfile):
                print(user.providerProfile)
            else:
                print("No provider profile found.")
            if (softwareSkillCSharp != None):
                # Let's add this skill to our user.
                user.addSkill(softwareSkillHtml5, False)
            if (softwareSkillJava != None):
                # Let's add this skill to our user.
                user.addSkill(softwareSkillJava, True)

        print("Creating an activity for user='steve'")

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


        print("Creating an activity for user='sally.smith'")

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


        print("Checking the activity navigation ... ")

        user = User.query.filter_by(username='steve').first()
        activityList = user.getActivityList()
        if (activityList):
            # The activity list
            for act in activityList:
                print(act)
                activitySkillList = act.activitySkillList
                if (activitySkillList):
                    for activitySkill in activitySkillList:
                        print activitySkill
                        print activitySkill.skill
                else:
                    print "Error - activity skill list is empty."

        # create a test invitation
        #softwareSkillHtml5
        print 'Creating a sample invitation'
        invitedUser = User.query.filter_by(username = 'mike.smith').first()
        invitingUser = User.query.filter_by(username='steve').first()
        activity = user.getActivityList()[0] # dangerous
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
        activity = user.getActivityList()[0] # dangerous
        invitation = Invitation(activity.id, softwareSkillHtml5.id, invitingUser.id, invitedUser.id)
        db.session.add(invitation)
        db.session.commit()
        invitationID = invitation.id

        invitation = Invitation.query.get(invitationID)
        invitedUser = None
        invitingUser = None
        invitedUser = invitation.receivingUser
        invitingUser = invitation.invitingUser

        print "Checking invitation navigation:"
        if (invitingUser):
            print(invitingUser)
        else:
            print("Invitation navigation failed.")
        if (invitedUser):
            print(invitedUser)
        else:
            print("Invitation navigation failed.")
















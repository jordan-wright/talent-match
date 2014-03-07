
from talent_match.models import User,Skill,Category
from talent_match import db

__author__ = 'Steve'

def addTestData() :
    userList = None
    userList = User.query.filter_by(is_admin=True)

    categoryList = Category.query.order_by(Category.name)
    skillList = Skill.query.order_by(Skill.name)

    if (userList == None) or (userList.count() < 1):
        print("Adding default user(s)")
        admin = User()
        admin.is_admin = True; admin.username = 'admin'; admin.email = 'admin@talent-match.us'
        admin.pwd_hash ='$2a$12$5XpK1rXasJv1Zdz7ABxMN.EyHERZ7WqMUjmRQeFALP7LEbrNB8tb2'
        db.session.add(admin)

        sally = User()
        sally.is_admin = True; sally.username = 'sally'; sally.email = 'sally@talent-match.us'
        sally.pwd_hash ='$2a$12$onbU2C6cjWs16m1RLDOjrObCpP8tLb28RAQeiYAbqE/JjPsGJiDOa'
        sally.firstName = 'Sally'
        sally.lastName = 'Struthers'
        sally.phoneNumber = '806-555-1212'
        sally.website = 'sallystruthers.com'
        db.session.add(sally)
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







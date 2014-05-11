from talent_match import db


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(
        db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    name = db.Column(db.String(80), nullable=False, index=True, unique=True)
    description = db.Column(db.String(256), nullable=True)

    # Project 3:  Steve - adding relationships and navigation
    skillList = db.relationship('Skill', lazy='joined')

    # Project 4: Steve/Nick - adding deleted flag.
    deleted = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        if (self.skillList) and (len(self.skillList) > 0):
            return 'Category: ' + self.name + ', description=' + self.description + ', count=' + str(len(self.skillList))
        else:
            return 'Category: ' + self.name + ', description=' + self.description

    # Project 3: adapting the serialize method from Jordan for the category
    # list, too.
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


class Skill(db.Model):
    __tablename__ = 'skill'
    id = db.Column(
        db.INTEGER, primary_key=True, autoincrement=True, nullable=False, index=True)
    categoryID = db.Column(db.INTEGER, db.ForeignKey('category.id'))
    name = db.Column(db.String(80), nullable=False, index=True, unique=True)
    description = db.Column(db.String(256), nullable=True)

    # Project 3:  Steve - adding relationships and navigation
    category = db.relationship(
        'Category', backref='skill', uselist=False, lazy='joined')

    # Project 4: Steve/Nick - adding deleted flag.
    deleted = db.Column(db.Boolean, default=False, nullable=False)

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
            'id': self.id,
            'categoryID': self.categoryID,
            'name': self.name,
            'description': self.description
        }

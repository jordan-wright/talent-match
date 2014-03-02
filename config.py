import os

basedir = os.path.dirname(os.path.abspath(__file__))

# SQLAlchemy Settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    os.path.join(basedir, 'talent-match.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repo')

SECRET_KEY = "Secret Key Here"
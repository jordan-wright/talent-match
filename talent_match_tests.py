import os
from talent_match import app, db
from config import basedir
import unittest

class TalentMatchTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        print 'Creating database'
        db.create_all()
        app.createTestData()

    def tearDown(self):
        os.unlink(os.path.join(basedir, 'talent-match.db'))

    def test_index(self):
        rv = self.app.get('/')
        assert 'Find Talent.' in rv.data

if __name__ == '__main__':
    unittest.main()
#!/usr/bin/env python

import os
from talent_match import app, db
from config import basedir
import unittest

class TalentMatchTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        print 'Creating database'
        db.create_all()
        app.testLoadFunction()

    def tearDown(self):
        os.unlink(os.path.join(basedir, 'talent-match.db'))

    def test_index(self):
        rv = self.app.get('/')
        assert 'Find Talent.' in rv.data

    def test_admin_login(self):
    	rv = self.login('admin@talent-match.us', 'admin!')
    	assert 'Admin: Categories' in rv.data
    	rv = self.logout()
    	assert 'Successfully logged out' in rv.data

    def login(self, email, password):
    	return self.app.post('/login', data=dict(
    		email=email,
    		password=password
    	), follow_redirects=True)

    def logout(self):
    	return self.app.get('/logout', follow_redirects=True)

if __name__ == '__main__':
    unittest.main()
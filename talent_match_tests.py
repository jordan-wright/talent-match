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

    def tearDown(self):
        rv = self.logout()
        assert 'Successfully logged out' in rv.data

    def test_index(self):
        rv = self.app.get('/')
        assert 'Find Talent.' in rv.data

    def test_admin_login(self):
    	rv = self.login('admin@talent-match.us', 'admin!')
    	assert 'Admin: Categories' in rv.data

    def test_user_login(self):
        rv = self.login('sally.smith@talent-match.us', 'sally!')
        assert 'Admin: Categories' not in rv.data

    def test_register(self):
        rv = self.app.post('/register', data=dict(
            firstName='Test',
            lastName='User',
            username='test_user',
            email='test@example.com',
            password='testing!',
            confirm_password='testing!'
        ), follow_redirects=True)
        assert 'Registration Successful!' in rv.data

    def test_search(self):
        self.login('sally.smith@talent-match.us', 'sally!')
        rv = self.app.post('/search', data=dict(
            query='HTML5'
            ), follow_redirects=True)
        assert 'Results for' in rv.data
        assert 'Sam Smith' in rv.data
        assert 'Next' in rv.data
        assert 'invites/create?id=5' in rv.data

    def test_invites(self):
        self.login('sally.smith@talent-match.us', 'sally!')
        # Create an invite for Sam Smith
        rv = self.app.post('http://localhost:5000/invites/create', data=dict(
            id="5"), follow_redirects=True)
        assert 'Sam Smith' in rv.data
        assert 'Advance Coding Activity' in rv.data
        assert 'Thermal' in rv.data
        # Send an invite to Sam Smith
        rv = self.app.post('http://localhost:5000/invites/create', data=dict(
            id="5",
            activities='Advance Coding Activity',
            skills='Thermal'
            ), follow_redirects=True)
        assert 'Invitation Has Been Sent!' in rv.data
        self.logout()
        # Login as Sam to check that the invite was received
        self.login('sam.smith@talent-match.us', 'sally!')
        rv = self.app.get('/invites', follow_redirects=True)
        assert 'Advance Coding' in rv.data
        assert 'Accept' in rv.data and 'Reject' in rv.data
        rv = self.app.get('/invites/submit?id=3&status=1', follow_redirects=True)
        assert 'Status Has Been Updated!' in rv.data
        assert 'Accepted' in rv.data

    def activity_list(self):
        self.login('sally.smith@talent-match', 'sally!')
        rv = self.app.get('/activity/list', follow_redirects=True)
        assert 'Advance Coding' in rv.data

    def login(self, email, password):
    	return self.app.post('/login', data=dict(
    		email=email,
    		password=password
    	), follow_redirects=True)

    def logout(self):
    	return self.app.get('/logout', follow_redirects=True)

def setupDB():
    print 'Creating database'
    db.create_all()
    app.testLoadFunction()

def destroyDB():
    os.unlink(os.path.join(basedir, 'talent-match.db'))

if __name__ == '__main__':
    setupDB()
    unittest.main()
    destroyDB()
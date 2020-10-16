import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from src import create_app
from src.models import User
class FlatTutorialsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'flat-tutorials'
        self.database_path = 'postgresql://{}/{}'.format('localhost:5432',
                self.database_name)
        

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
        with open('auth.json') as f:
            self.tokens = json.loads(f.read())
            
            #get a user that exists for testing purposes
            user = User.query.first()
            self.user_id = user.id

    def tearDown(self):
        pass

    ###############
    # admin tests #
    ###############

    def test_admin_list_users(self):
        res = self.client().get('/admin/users',
                headers={'Authorization':self.tokens['administrator']})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_admin_delete_tutorial(self):
        res = self.client().delete('/admin/tutorial/<int:tutorial_id>')
        pass

    def test_admin_unpublish_tutorial(self):
        res = self.client().patch('unpublish_tutorial')
        pass

    ###################
    # moderator tests #
    ###################
    def test_moderator_get_submitted_list(self):
        res = self.client().get('/submitted')
        pass

    def test_moderator_get_submitted_tutorial(self):
        res = self.client().get('/submitted<int:tutorial_id>')
        pass

    def test_moderator_get_unpublished_list(self):
        res = self.client().get('/unpublished')
        pass

    def test_moderator_get_unpublished_tutorial(self):
        res = self.client().get('/unpublished/<int:tutorial_id>')
        pass

    def test_moderator_publish(self):
        res = self.client().get('/publish/<int:tutorial_id>')
        pass

    def test_moderator_deny(self):
        res = self.client().patch('/deny/<int:tutorial_id>')
        pass

    def test_moderator_list_users(self):
        res = self.client().get('/admin/users')
        pass

    def test_moderator_delete_tutorial(self):
        res = self.client().delete('/admin/tutorial/<int:tutorial_id>')
        pass

    def test_moderator_unpublish_tutorial(self):
        res = self.client().patch('unpublish_tutorial')
        pass

    ##################
    # end_user tests #
    ##################
    def test_end_user_submit(self):
        res = self.client().post('/submit')
        pass

    def test_end_user_edit(self):
        res = self.client().patch('/edit/<int:tutorial_id>')
        pass

    def test_end_user_get_submitted_list(self):
        res = self.client().get('/submitted')
        pass

    def test_end_user_get_submitted_tutorial(self):
        res = self.client().get('/submitted<int:tutorial_id>')
        pass

    def test_end_user_get_unpublished_list(self):
        res = self.client().get('/unpublished')
        pass

    def test_end_user_get_unpublished_tutorial(self):
        res = self.client().get('/unpublished/<int:tutorial_id>')
        pass
    ################
    # public tests #
    ################

    def test_public_get_published_list(self):
        res = self.client().get('/published')
        pass

    def test_public_get_published_tutorial(self):
        res = self.client().get('/published/<int:tutorial_id>')
        pass

    def test_public_get_published_list_by_author(self):
        res = self.client().get('/published/by-author/<int:author_id>')
        pass

    def test_public_get_published_by_tag(self):
        res = self.client().get('/published/tags/<string:tag>')
        pass

    def test_public_get_published_by_tags(self):
        res = self.client().get('/published/tags/<string:tag1>/<string:tag2>')
        pass
    def test_public_get_unpublished_list(self):
        res = self.client().get('/unpublished')
        pass

    def test_public_get_unpublished_tutorial(self):
        res = self.client().get('/unpublished/<int:tutorial_id>')
        pass

    def test_public_publish(self):
        res = self.client().get('/publish/<int:tutorial_id>')
        pass

    def test_public_deny(self):
        res = self.client().patch('/deny/<int:tutorial_id>')
        pass

    def test_public_list_users(self):
        res = self.client().get('/admin/users')
        pass

if __name__ == '__main__':
    unittest.main()

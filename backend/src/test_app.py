import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from src import create_app
from src.models import User, Published_Tutorial, Unpublished_Tutorial
class FlatTutorialsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(test_config=True)
        self.client = self.app.test_client 
        database_name = 'flat-tutorials-test'
        database_path = "postgres://{}@{}/{}".format('postgres',
                'localhost:5432', database_name)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        
       
        with open('auth.json') as f:
            self.tokens = json.loads(f.read())
            
            #get a user that exists for testing purposes
            user = User.query.first()
            self.user_id = user.id

            #article placeholder
            self.tutorial_id = None
    
    def addTutorial(self):
        tutorial = Unpublished_Tutorial(title='title',text='text',under_review=True,
                author_id=self.user_id)
        tutorial.insert()
        self.tutorial_id = tutorial.id
    

    def tearDown(self):
        pass

    ###############
    # admin tests #
    ###############

    def test_admin_list_users(self):
        res = self.client().get('/admin/users',
                headers={'Authorization':self.tokens['administrator']})
        data = json.loads(res.data)
        self.assertTrue(len(data['users']))
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_admin_delete_tutorial(self):
        tutorial = Unpublished_Tutorial(title='title',text='text',under_review=False,
                author_id=self.user_id)
        tutorial.insert()
        self.tutorial_id = tutorial.id
        tutorial = Published_Tutorial(id=self.tutorial_id,
                title='title',text='text',author_id=self.user_id)
        tutorial.insert()
        self.tutorial_id = tutorial.id
        res = self.client().delete('/admin/tutorial/{}'.format(self.tutorial_id),
                headers={'Authorization':self.tokens['administrator']})
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted_id'], self.tutorial_id)
        
    def test_admin_unpublish_tutorial(self):
        tutorial = Unpublished_Tutorial(title='title',text='text',under_review=False,
                author_id=self.user_id)
        tutorial.insert()
        self.tutorial_id = tutorial.id
        tutorial = Published_Tutorial(id=self.tutorial_id,
                title='title',text='text',author_id=self.user_id)
        tutorial.insert()
        submit_data = {
                'reviewer_notes': 'notes'
                }
        self.tutorial_id = tutorial.id
        res = self.client().patch('/admin/unpublish/{}'.format(self.tutorial_id),
                json = submit_data,
                headers={'Authorization':self.tokens['administrator']})
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['unpublished_id'], self.tutorial_id)
    


    ###################
    # moderator tests #
    ###################
    def test_moderator_get_unpublished_list(self):
        self.addTutorial()
        
        res = self.client().get('/unpublished',
                headers={'Authorization': self.tokens['moderator']})
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['tutorials']))

    
    def test_moderator_get_unpublished_tutorial(self):
        
        self.addTutorial()
        
        res = self.client().get('/unpublished/{}'.format(self.tutorial_id),
                headers={'Authorization': self.tokens['moderator']})
        data = json.loads(res.data)
       
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['tutorial']['id'], self.tutorial_id) 
    
    def test_moderator_publish(self):
        self.addTutorial()
        
        res = self.client().get('/unpublished/{}'.format(self.tutorial_id),
                headers={'Authorization': self.tokens['moderator']})
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['tutorial']['id'], self.tutorial_id)
        
        
    
    def test_moderator_deny(self):
        self.addTutorial()
        submit_data = {'review_notes': 'notes'}
        res = self.client().patch('/deny/{}'.format(self.tutorial_id),
                json = submit_data,
                headers={'Authorization': self.tokens['moderator']})
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['denied_id'], self.tutorial_id)
        
    
    def test_moderator_list_users(self):
        res = self.client().get('/admin/users')
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 401)

    def test_moderator_delete_tutorial(self):
        self.addTutorial()
        
        res = self.client().delete('/admin/tutorial/{}'.format(self.tutorial_id),
                headers={'Authorization': self.tokens['moderator']})
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 401)

    def test_moderator_unpublish_tutorial(self):
        self.addTutorial()
        res = self.client().patch('/admin/unpublish/{}'.format(self.tutorial_id),
                headers={'Authorization': self.tokens['moderator']})
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 401)

    
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

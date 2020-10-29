import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from src import create_app
from src.models import User, Published_Tutorial, Unpublished_Tutorial
from pathlib import Path
from dotenv import load_dotenv
load_dotenv('../flaskenv')

class FlatTutorialsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(test_config=True)
        self.client = self.app.test_client 
        TEST_DATABASE_NAME = os.environ.get('TEST_DATABASE_NAME')
        DATABASE_LOCATION = os.environ.get('DATABASE_LOCATION')
        DATABASE_USER = os.environ.get('DATABASE_USER')
        database_path = "postgres://{}@{}/{}".format(DATABASE_USER,
                DATABASE_LOCATION, TEST_DATABASE_NAME)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        
        filepath = Path(__file__).parent.absolute() / 'auth.json'
        with open(filepath) as f:
            self.tokens = json.loads(f.read())
            
            #submit a tutorial from registered user
            self.tutorial_id = self.makeSubmission()['tutorial']['author_id']
            
            #publish one
            self.publish()
        
    # Submit a tutorial to return the id of current JWT's user
    def makeSubmission(self):
        submit_data = {
                'title': 'title',
                'text': 'text',
                'tags': ['tech1', 'tech2', 'tech3']
                }
        res = self.client().post('/submit',
                json=submit_data,
                headers={'Authorization': self.tokens['registered_user']}
                )
        data = json.loads(res.data)
        self.tutorial_id = data['tutorial']['id']
        return data

    def publish(self):
        self.client().get('/publish/{}'.format(self.tutorial_id),
            headers={'Authorization': self.tokens['moderator']})


    

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
        self.makeSubmission()
        self.publish()
        res = self.client().delete('/admin/tutorial/{}'.format(self.tutorial_id),
                headers={'Authorization':self.tokens['administrator']})
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted_id'], self.tutorial_id)
   
    def test_admin_unpublish_tutorial(self):
        self.makeSubmission()
        self.publish()
        submit_data = {
                'reviewer_notes': 'notes'
                }
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
        self.makeSubmission()
        
        res = self.client().get('/unpublished',
                headers={'Authorization': self.tokens['moderator']})
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['tutorials']))

    
    def test_moderator_get_unpublished_tutorial(self):
        
        self.makeSubmission()
        
        res = self.client().get('/unpublished/{}'.format(self.tutorial_id),
                headers={'Authorization': self.tokens['moderator']})
        data = json.loads(res.data)
       
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['tutorial']['id'], self.tutorial_id) 
   
    def test_moderator_publish(self):
        self.makeSubmission()
        
        res = self.client().get('/unpublished/{}'.format(self.tutorial_id),
                headers={'Authorization': self.tokens['moderator']})
        data = json.loads(res.data)

        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['tutorial']['id'], self.tutorial_id)
        
        
    
    def test_moderator_deny(self):
        self.makeSubmission()
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
        self.makeSubmission()
        self.publish()
        res = self.client().delete('/admin/tutorial/{}'.format(self.tutorial_id),
                headers={'Authorization': self.tokens['moderator']})
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 401)

    def test_moderator_unpublish_tutorial(self):
        self.makeSubmission()
        self.publish()
        res = self.client().patch('/admin/unpublish/{}'.format(self.tutorial_id),
                headers={'Authorization': self.tokens['moderator']})
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 401)

    
    #################
    # end_user tests #
    ##################
    def test_end_user_submit(self):
        submit_data = {
                'title': 'title',
                'text': 'text',
                'tags': ['tech1','tech2','tech3']
                }
        res = self.client().post('/submit',
                json=submit_data,
                headers={'Authorization': self.tokens['registered_user']}
                )
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['user_id'])

    def test_end_user_edit(self):
        previous_submission = self.makeSubmission()
        submit_data = {
                'title': 'title',
                'text': 'text',
                'tags': ['tech4','tech5','tech6']
                }
        res = self.client().patch('/edit/{}'.format(previous_submission['tutorial']['id']),
                json=submit_data,
                headers={'Authorization': self.tokens['registered_user']}
                )
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(previous_submission['tutorial']['id'], data['tutorial']['id'])
    
    def test_end_user_edit_WRONG_USER(self):
        previous_submission = self.makeSubmission()
        submit_data = {
                'title': 'title',
                'text': 'text',
                'tags': ['tech4','tech5','tech6']
                }
        res = self.client().patch('/edit/{}'.format(previous_submission['tutorial']['id']),
                json=submit_data,
                headers={'Authorization': self.tokens['administrator']}
                )
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 403)

    def test_end_user_get_submitted_list(self):
        previous_submission = self.makeSubmission()
        res = self.client().get('/submitted',
                headers={'Authorization': self.tokens['registered_user']}
                )
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['tutorials']))

    def test_end_user_get_submitted_tutorial(self):
        previous_submission = self.makeSubmission()
        res = self.client().get('/submitted/{}'.format(previous_submission['tutorial']['id']),
            headers={'Authorization': self.tokens['registered_user']}
            )
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
     
    def test_end_user_get_submitted_tutorial_WRONG_USER(self):
        previous_submission = self.makeSubmission()
        res = self.client().get('/submitted/{}'.format(previous_submission['tutorial']['id']),
            headers={'Authorization': self.tokens['administrator']}
            )
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 403)

    ################
    # public tests #
    ################

    def test_public_get_published_list(self):
        self.makeSubmission()
        self.publish()
        res = self.client().get('/published')
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['tutorials']))
        

    def test_public_get_published_tutorial(self):
        self.makeSubmission()
        self.publish()
        tutorial = Published_Tutorial.query.first()
        res = self.client().get('/published/{}'.format(tutorial.id))
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['tutorial']['id'], tutorial.id)
       
    def test_public_get_published_list_by_author(self):
        self.makeSubmission()
        self.publish()
        tutorial = Published_Tutorial.query.first()
        res = self.client().get('/published/by-author/{}'.format(tutorial.author_id))
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['tutorials']))
  
    def test_public_get_published_by_tag(self):
        self.makeSubmission()
        self.publish()
        tutorial = Published_Tutorial.query.first() 
        tag = tutorial.tags[0].name
        res = self.client().get('/published/tags/{}'.format(tag))
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['tutorials']))
  
    def test_public_get_published_by_tags(self):
        self.makeSubmission()
        self.publish()
        tutorial = Published_Tutorial.query.first() 
        tag1 = tutorial.tags[0].name
        tag2 = tutorial.tags[1].name
        res = self.client().get('/published/tags/{}/{}'.format(tag1,tag2))
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['tutorials'])) 
    
    def test_public_get_unpublished_list(self):
        res = self.client().get('/unpublished')
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 401)

    def test_public_get_unpublished_tutorial(self):
        self.makeSubmission()
        tutorial = Unpublished_Tutorial.query.first()
        res = self.client().get('/unpublished/{}'.format(tutorial.id))
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 401)

    def test_public_publish(self):
        self.makeSubmission()
        tutorial = Unpublished_Tutorial.query.first()
        res = self.client().get('/publish/{}'.format(tutorial.id))
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 401)

    def test_public_deny(self):
        self.makeSubmission()
        tutorial = Unpublished_Tutorial.query.first()
        submit_data = {
                'reviewer_notes': 'notes'
                }
        res = self.client().patch('/deny/{}'.format(tutorial.id),
                json=submit_data)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 401)

    def test_public_list_users(self):
        res = self.client().get('/admin/users')
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code, 401)

if __name__ == '__main__':
    unittest.main()

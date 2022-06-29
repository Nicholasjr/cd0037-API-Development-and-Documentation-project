import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path ="postgres://{}:{}@{}/{}".format('student', 'student','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        self.new_question ={
            'question': 'Are you okay?',
            'answer': 'No, not at all',
            'difficulty': 2,
            'category': '2'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    def test_get_categories(self):
        """Test categories success"""
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
        
    def test_404_on_categories(self):
        """Test categories error"""
        res = self.client().get('/categories/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        
    def test_get_questions(self):
        """Test questions success"""
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        
    def test_404_on_questions(self):
        """Test questions success"""
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        
        
    def test_delete_questions(self):
        """Test delete question success"""
        res = self.client().delete('/questions/6')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 6).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(question, None)
        
    def test_400_on_delete_questions(self):
        """Test delete question error"""
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

        
    def test_create_question(self):
        """Test create question success"""
        res = self.client().post('/question', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_422_on_create_question(self):
        """Test create question error"""
        res = self.client().post('/question', json={})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
    
    def test_search_questions(self):
        """Test search success"""
        res = self.client().post('/questions', json={'searchTerm': 'in'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['total_questions'], 0)  
        
    def test_422_on_search_question(self):
        """Test search failure"""
        res = self.client().post('/questions', json={'searchTerm': 'Noneomagro'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'cannot be processed')
        

    def test_get_question_by_category(self):
        """Test get question by category success"""
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])  
        
    def test_422_on_get_question_by_category(self):
        """Test get question by category error"""
        res = self.client().get('/categories/9/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'cannot be processed')

    def test_create_quiz(self):
        """Test create quiz success"""
        res = self.client().post('/quizzes', json={'quiz_category': {'id': 1, 'type': 'Science'}, 'previous_questions': []})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])  
        
    def test_422_create_quiz(self):
        """Test create quiz error"""
        res = self.client().post('/quizzes', json={'quiz_category': {'id': 100, 'type': 'Sciencesjdh'}, 'previous_questions': []})
        data = json.loads(res.data)
        
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        
        
        
        
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
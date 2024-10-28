
import unittest
from app import app, db, User
import json

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.post('/api/register', 
                                    data=json.dumps({'username': 'testuser', 'password': 'testpass'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', response.get_json()['message'])

    def test_chat_unauthorized(self):
        response = self.client.post('/api/chat',
                                    data=json.dumps({'prompt': 'Hello'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_execute_unauthorized(self):
        response = self.client.post('/api/execute',
                                    data=json.dumps({'code': 'print("Hello")'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()

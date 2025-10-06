from app import create_app
from app.models import db, Mechanics
from datetime import date, datetime
import unittest

# python -m unittest discover tests - use to run tests

class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.mechanic = Mechanics(name="test", email="test@email.com", phone="123-456-7890", salary="99999.99")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
        self.client = self.app.test_client()

    def test_create_mech(self):
        mech_payload = {
            "name": "test2",
            "email": "test2@email.com",
            "phone": "098-765-4321",
            "salary": "66666.99"
        }
        response = self.client.post("/mechanics", json=mech_payload)
        print(response.json)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'test2')

    def test_read_mech(self):
        response = self.client.get('/mechanics')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], 'test')

    def test_update_mech(self):
        update_payload = {
            "name": "test2",
            "email": "NEWtest2@email.com",
            "phone": "098-765-4321",
            "salary": "66966.99"
        }
        response = self.client.put('/mechanics/1', json=update_payload)
        print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['salary'], 66966.99)

    def test_delete_mech(self):
        response = self.client.delete('/mechanics/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Successfully deleted mechanic 1')

    def test_get_pop_mech(self):
        response = self.client.get('/mechanics/popularity')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['mech'], {})

    def test_search_mech(self):
        response = self.client.get('/mechanics/search?name=test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], 'test')

    def test_search_invalid_mech(self):
        response = self.client.get('/mechanics/search?name=Skai')
        self.assertEqual(response.status_code, 400)
        self.assertIn(response.json['message'], 'Invalid search, no mechanics with that name')
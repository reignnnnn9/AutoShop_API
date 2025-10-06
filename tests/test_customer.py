from app import create_app
from app.models import db, Customers
from app.utils.util import encode_token
from datetime import date, datetime
from werkzeug.security import check_password_hash, generate_password_hash
import unittest

# python -m unittest discover tests - use to run tests

class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        date_format = "%Y-%m-%d" 
        date1 = datetime.strptime("1993-11-09", date_format)
        self.customer = Customers(name="test", email="test@email.com", password=generate_password_hash('123'), phone="123-456-7890", DOB=date1)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
        self.token = encode_token(1)
        self.client = self.app.test_client()

    def test_create_customer(self):
        customer_payload = {
            "name": "test_customer",
            "email": "test_cust@email.com",
            "password": "123",
            "phone": "123-456-7891",
            "address": " ",
            "DOB": "1996-03-06"
        }
        response = self.client.post("/customers", json=customer_payload) # Sending a test POST request using out test_client, and including the JSON body
        print(response.json)
        self.assertEqual(response.status_code, 201) # Checking if we got a 201 status code back from creating customer
        self.assertEqual(response.json['name'], 'test_customer') # Checking to make sure the username is equal to test_customer, as it is set in the testcase
        self.assertTrue(check_password_hash(response.json['password'], "123"))

    def test_invalid_customer(self):
        customer_payload = { # Missing email which is a required field
            "name": "test_customer",
            "password": "123",
            "phone": "123-456-7891",
            "address": " ",
            "DOB": "1996-03-06"
        }
        response = self.client.post("/customers", json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.json) # Membership check that email is in the response json

    def test_login(self):
        login_creds = {
            "email": "test@email.com",
            "password": "123"
        }
        response = self.client.post("/customers/login", json=login_creds)
        self.assertEqual(response.status_code, 200)
        self.assertIn('auth_token', response.json)

    def test_read_cust(self):
        response = self.client.get('/customers')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], 'test')

    def test_delete_customer(self):
        headers = {'Authorization': "Bearer " + self.token}
        response = self.client.delete('/customers', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Successfully deleted customer 1')

    def test_unauthorized_delete(self):
        response = self.client.delete('/customers')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'Token is missing!')

    def test_update_customer(self):
        headers = {'Authorization': "Bearer " + self.token}
        update_payload = {
            "name": "Test Cust",
            "email": "tc@email.com",
            "password": "123",
            "phone": "123-456-7891",
            "address": "123 Main St",
            "DOB": "1996-03-06"
        }
        response = self.client.put('/customers', headers=headers, json=update_payload)
        print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], 'tc@email.com')
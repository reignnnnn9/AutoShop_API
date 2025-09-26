from app import create_app
from app.models import db, Customers
from app.utils.util import encode_token
from werkzeug.security import check_password_hash, generate_password_hash
import unittest

class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.customer = Customers(email='')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
        self.token = encode_token(1, 'customer')
        self.client = self.app.test_client()

    def test_create_customer(self):
        customer_payload = {
            "name": "test",
            "email": "test@email.com",
            "password": "123",
            "phone": "123-456-7890",
            "address": " ",
            "DOB": "1995-03-06"
        }
        response = self.client.post("/users", json=customer_payload) # Sending a test POST request using out test_client, and including the JSON body
        print(response.json)
        self.assertEqual(response.status_code, 201) # Checking if we got a 201 status code back from creating customer
        self.assertEqual(response.json['name'], 'test') # Checking to make sure the username is equal to test_customer, as it is set in the testcase

    # def test_invalid_user(self):

    # def test_login(self):
    #     login_creds = {

    #     }
from app import create_app
from app.models import db, Customer, Service_Ticket
from datetime import date
from app.utils.util import encode_token
import unittest


class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestConfig")
        self.customer = Customer(
            name="test_user", 
            email="test@email.com",
            phone="123-456-7890",
            password="test"                     
        )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
            #self.token = encode_token(self.customer.id)
            self.customer_id = self.customer.id

        self.token = encode_token(1)
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()


    #----------Create Customer-------------------------------------
    def test_create_customer(self):
        customer_payload = {
            "name": "Jon Doe",
            "email": "jd@email.com",
            "phone": "123-456-7890",
            "password": "123abcde"
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Jon Doe")
        
    def test_invalid_creation(self):
        customer_payload = {
            "name": "Jon Doe",
            "phone": "123-456-7890",
            "password": "123abcde" 
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])


    #---------Customer Login------------------------------------------
    def test_login_customer(self):
        credentials = {
            "email": "test@email.com",
            "password": "test"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        return response.json['token']

    def test_invalid_login(self):
        credentials = {
            "email": "bad_email@email.com",
            "password": "bad_pw"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Invalid email or password')


    #--------Token Authenticated Route (Update Customer)-------------
    def test_update_customer(self):
        update_payload = {
            "name": "Peter"             
        }

        headers = {'Authorization': "Bearer " + self.test_login_customer()}

        response = self.client.put('/customers/', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Peter')
        self.assertEqual(response.json['email'], 'test@email.com')


    #---------Get All Customers--------------------------------------
    def test_get_all_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], 'test_user')


    #---------Get Specific Customer----------------------------------
    def test_get_specific_customer(self):
        response = self.client.get('/customers/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'test_user')       


    #--------Delete Customer-----------------------------------------
    def test_delete_customer(self):
        headers = {'Authorization': "Bearer " + self.test_login_customer()}
        response = self.client.delete('/customers/', headers=headers)
        self.assertEqual(response.status_code, 200)


    #--------Get Customer Service Ticket(s)--------------------------
    def test_get_service_ticket(self):
        with self.app.app_context():
            ticket = Service_Ticket(
                vin = "123465789ABCDEFG",
                service_desc = "Oil change",
                service_date = date.today(),
                customer_id = self.customer_id
            )

            db.session.add(ticket)
            db.session.commit()

        headers = {'Authorization': "Bearer " + self.test_login_customer()}
        
        response = self.client.get('/customers/my-tickets', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['service_desc'], "Oil change")




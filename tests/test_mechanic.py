from app import create_app
from app.models import db, Mechanic
import unittest


class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestConfig")
        self.mechanic = Mechanic(
            name= "test_mechanic",
            email= "testm@email.com",
            phone= "123-456-7891",
            salary= "45000.0"
        )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()

            self.mechanic_id = self.mechanic.id

        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()


    #------------Create Mechanic----------------------------------
    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "Bob Doe",
            "email": "bd@email.com",
            "phone": "123-456-7890",
            "salary": "46000"           
        }

        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Bob Doe")

    def test_invalid_mechanic(self):
        mechanic_payload = {
            "name": "Bob Doe",
            "phone": "123-456-7890",
            "salary": "46000"           
        }   

        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])


    #--------Get All Mechanics-----------------------------------
    def test_get_all_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], 'test_mechanic')


    #--------Get Specific Mechanic--------------------------------
    def test_get_specific_mechanic(self):
        response = self.client.get('mechanics/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'test_mechanic')


    #---------Update Mechanic-------------------------------------
    def test_update_mechanic(self):
        updatem_payload = {
            "name": "Bart"
        }

        response = self.client.put('/mechanics/1', json=updatem_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Bart')
        self.assertEqual(response.json['email'], 'testm@email.com')


    #---------Delete Mechanic-------------------------------------
    def test_delete_mechanic(self):
        response = self.client.delete(f'/mechanics/{self.mechanic_id}')
        self.assertEqual(response.status_code, 200)

        # test to make sure mechanic was deleted
        response = self.client.get(f'/mechanics/{self.mechanic_id}')
        self.assertEqual(response.status_code, 404)


    #---------Get Mechanic Workload--------------------------------=
    def test_workload(self):
        response = self.client.get('/mechanics/workload')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], 'test_mechanic')




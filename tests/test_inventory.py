from app import create_app
from app.models import db, Inventory
import unittest


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestConfig")
        self.item = Inventory(
            name= "test_item",
            price= 40.0
        )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.item)
            db.session.commit()

            self.item_id = self.item.id

        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()


    #---------Create Inventory Item---------------------------------
    def test_create_item(self):
        inventory_payload = {
            "name": "Tire",
            "price": 130.0
        }

        response = self.client.post('/inventories/', json=inventory_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Tire")

    def test_invalid_item(self):
        inventory_payload = {
            "name": "Tire"
        }

        response = self.client.post('/inventories/', json=inventory_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['price'], ['Missing data for required field.'])


    #---------Get All Inventory Items----------------------------------
    def test_get_all_items(self):
        response = self.client.get('/inventories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], 'test_item')


    #---------Get Specific Inventory Item------------------------------
    def test_get_specific_item(self):
        response = self.client.get('/inventories/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'test_item')


    #---------Update Inventory item------------------------------------
    def test_update_item(self):
        updatei_payload = {
            "name": "Oil"
        }

        response = self.client.put('/inventories/1', json=updatei_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Oil')
        self.assertEqual(response.json['price'], 40.0)


    #---------Delete Inventory Item------------------------------------    
    def test_delete_item(self):
        response = self.client.delete(f'/inventories/{self.item_id}')
        self.assertEqual(response.status_code, 200)

        # test to make sure item was deleted
        response = self.client.get(f'/inventories/{self.item_id}')
        self.assertEqual(response.status_code, 404)


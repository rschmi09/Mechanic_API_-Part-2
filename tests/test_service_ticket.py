from app import create_app
from app.models import db, Service_Ticket, Mechanic, Inventory
from datetime import date
import unittest


class TestServiceTicket(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestConfig")
        self.ticket = Service_Ticket(
            vin = "123456789ABCDE",
            service_date = date(2026, 1, 1),
            service_desc = "Oil change",
            customer_id = "1"
        )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.ticket)
            db.session.commit()

            self.ticket_id = self.ticket.id

        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()


    #--------Create Service Ticket-------------------------
    def test_create_ticket(self):
        ticket_payload = {
            "vin": "123456789ABCDE",
            "service_date": "2026-01-01",
            "service_desc": "Oil change",
            "customer_id" : "1"            
        }

        response = self.client.post('/service_tickets/', json=ticket_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['vin'], "123456789ABCDE")

    def test_invalid_ticket(self):
        ticket_payload = {
            "vin": "123456789ABCDE",
            "service_date": "2026-01-01",
            "customer_id" : "1"            
        }         

        response = self.client.post('/service_tickets/', json=ticket_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['service_desc'], ['Missing data for required field.'])


    #--------Get All Service Tickets------------------------
    def test_get_all_tickets(self):
        response = self.client.get('/service_tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['vin'], '123456789ABCDE')


    #--------Get Specific Service Ticket--------------------
    def test_get_specific_ticket(self):
        response = self.client.get('service_tickets/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['vin'], '123456789ABCDE')


    #--------Update Service Ticket--------------------------
    def test_update_ticket(self):
        updatet_payload = {
            "service_desc": "Oil change and tire rotation"
        }

        response = self.client.put('/service_tickets/1', json=updatet_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['service_desc'], 'Oil change and tire rotation')
        self.assertEqual(response.json['vin'], '123456789ABCDE')


    #--------Delete Service Ticket--------------------------
    def test_delete_ticket(self):
        response = self.client.delete(f'service_tickets/{self.ticket_id}')
        self.assertEqual(response.status_code, 200)

        # test to make sure the service ticket was deleted
        response = self.client.get(f'/service_tickets/{self.ticket_id}')
        self.assertEqual(response.status_code, 404)


    #--------Assign/Remove Mechanic-------------------------
    
    #--------Assign Mechanic----------------------
    def test_assign_mechanic(self):
        with self.app.app_context():

            mechanic = Mechanic(
                name= "Bob",
                email= "bob@email.com",
                phone= "123-456-7890",
                salary= 45000
            )

            ticket = Service_Ticket(
                vin= "123456789ABCDE",
                service_date=date(2026, 1, 1),
                service_desc= "Oil change",
                customer_id= 1
            )

            db.session.add(mechanic)
            db.session.add(ticket)
            db.session.commit()

            mechanic_id = mechanic.id
            ticket_id = ticket.id  

        assign_payload = {
            "add_mechanic_ids": [mechanic_id],
            "remove_mechanic_ids": []
        }

        response = self.client.put(f'service_tickets/{ticket_id}/edit', json=assign_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["mechanics"][0]["id"], mechanic_id)

    #--------Remove Mechanic----------------------
    def test_remove_mechanic(self):
        with self.app.app_context():

            mechanic = Mechanic(
                name= "Bob",
                email= "bob@email.com",
                phone= "123-456-7890",
                salary= 45000
            )

            ticket = Service_Ticket(
                vin= "123456789ABCDE",
                service_date=date(2026, 1, 1),
                service_desc= "Oil change",
                customer_id= 1
            )

            db.session.add(mechanic)
            db.session.add(ticket)
            db.session.commit()

            mechanic_id = mechanic.id
            ticket_id = ticket.id  

        remove_payload = {
            "add_mechanic_ids": [],
            "remove_mechanic_ids": [mechanic_id]
        }

        response = self.client.put(f'service_tickets/{ticket_id}/edit', json=remove_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["mechanics"]), 0)


    #--------Add Inventory Item to Service Ticket-----------
    def test_add_item(self):
        with self.app.app_context():

            item = Inventory(
                name= "test_item",
                price= 40.0                
            )

            ticket = Service_Ticket(
                vin= "123456789ABCDE",
                service_date=date(2026, 1, 1),
                service_desc= "Oil change",
                customer_id= 1
            )

            db.session.add(item)
            db.session.add(ticket)
            db.session.commit()

            item_id = item.id
            ticket_id = ticket.id  

            #add_payload = {
                #"add_inventory_ids": [item_id]
            #}
            
            response = self.client.put(f'/service_tickets/{ticket_id}/edit/{item_id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn("added to Service Ticket", response.json["message"])


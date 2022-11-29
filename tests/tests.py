from django.test import TestCase
from shipapp.models import Shipment
from Services.CourierServices.Aramex import Aramex
import json

class TestShipment(TestCase):
    
    def setUp(self) -> None:
        self.shipment = Shipment.objects.create(
            title='title',
            description='description',
            provider=Shipment.ARAMEX,
            length=5,
            width=5,
            height=5,
            weight=7,
            number_of_pieces=1,
            product_country='EG',
            sender_name='Ahmed',
            sender_mobile='011111',
            sender_email='mhmdsamir@gmail.com',
            sender_full_address='address',
            sender_country='EG',
            receiver_name='Mohamed',
            receiver_mobile='01111111',
            receiver_email='mhmdsamir@gmail.com',
            receiver_full_address='address',
            receiver_country='EG',
            shipping_date='2022-12-07',
            tracking_id='123456789'
        )
    
    def tearDown(self) -> None:
        Shipment.objects.all().delete()

    def test_print_label(self):
        response = self.client.get(f'/api/shipment/{self.shipment.id}/print')
        self.assertEqual(response.get('Content-Disposition'), f"attachment; filename=\"{self.shipment.id}.pdf\"")

    def test_cancel_shipment(self):
        response = self.client.post(f'/api/shipment/cancel',
                                    data=json.dumps({
                                        'id': self.shipment.id
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['id'], self.shipment.id)
        self.assertEqual(result['status'], Shipment.CANCELLED)
    
    def test_cancel_shipment_unsupported_courier(self):
        old_status = self.shipment.status
        self.shipment.provider = Shipment.SMSA
        self.shipment.save()
        response = self.client.post(f'/api/shipment/cancel',
                                    data=json.dumps({
                                        'id': self.shipment.id
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        result = response.json()
        self.assertEqual(result['details'], "The courier doesn't support cancel operation")
        self.assertEqual(self.shipment.status, old_status)
    
    def test_cancel_shipment_unexisted_shipment(self):
        response = self.client.post(f'/api/shipment/cancel',
                                    data=json.dumps({
                                        'id': -1
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_cancel_shipment_by_tracking_id(self):
        response = self.client.post(f'/api/shipment/cancel',
                                    data=json.dumps({
                                        'tracking_id': self.shipment.tracking_id
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['id'], self.shipment.id)
        self.assertEqual(result['status'], Shipment.CANCELLED)
    
    def test_get_shipments(self):
        response = self.client.get(f'/api/shipment/?tracking_id={self.shipment.tracking_id}')
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result[0]['id'], self.shipment.id)
    
    def test_update_shipment_status(self):
        response = self.client.post(f'/api/shipment/update',
                                    data=json.dumps({
                                        'id': self.shipment.id,
                                        'status': Shipment.TRANSIT
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['id'], self.shipment.id)
        self.assertEqual(result['status'], Shipment.TRANSIT)
    
    def test_update_shipment_unsupported_state(self):
        old_status = self.shipment.status
        self.shipment.provider = Shipment.SMSA
        self.shipment.save()
        response = self.client.post(f'/api/shipment/update',
                                    data=json.dumps({
                                        'id': self.shipment.id,
                                        'status': 'SCHEDULUED' # Not system state or supported in SMSA
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        result = response.json()
        self.assertEqual(result['details'], "Requested status is not supported by the system or the courier")
        self.assertEqual(self.shipment.status, old_status)
    
    def test_update_shipment_unexisted_shipment(self):
        response = self.client.post(f'/api/shipment/update',
                                    data=json.dumps({
                                        'id': -1,
                                        'status': Shipment.TRANSIT
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_update_shipment_by_tracking_id(self):
        response = self.client.post(f'/api/shipment/update',
                                    data=json.dumps({
                                        'tracking_id': self.shipment.tracking_id,
                                        'status': 'RECEIVED' # Supported only in ARAMEX, equals to DELIVERED
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['id'], self.shipment.id)
        self.assertEqual(result['status'], Shipment.DELIVERED)
    
    def test_update_shipment_by_id_courier_state(self):
        response = self.client.post(f'/api/shipment/update',
                                    data=json.dumps({
                                        'id': self.shipment.id,
                                        'status': 'RECEIVED' # Supported only in ARAMEX, equals to DELIVERED
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['id'], self.shipment.id)
        self.assertEqual(result['status'], Shipment.DELIVERED)
    
    def test_create_shipment(self):
        response = self.client.post(f'/api/shipment/create',
                                    data=json.dumps({
                                        "title": "title",
                                        "description": "description",
                                        "provider": "ARAMEX",
                                        "length": 5,
                                        "width": 5,
                                        "height": 5,
                                        "weight": 7,
                                        "number_of_pieces": 1,
                                        "product_country": "EG",
                                        "sender_name": "Ahmed",
                                        "sender_mobile": "011111",
                                        "sender_email": "mhmdsamir@gmail.com",
                                        "sender_full_address": "address",
                                        "sender_country": "EG",
                                        "receiver_name": "Mohamed",
                                        "receiver_mobile": "01111111",
                                        "receiver_email": "mhmdsamir@gmail.com",
                                        "receiver_full_address": "address",
                                        "receiver_country": "EG",
                                        "shipping_date": "2022-12-07"
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        result = response.json()
        self.assertEqual(result['status'], Shipment.REGISTERED)
        self.assertIsNotNone(result['tracking_id']) # to make sure that courier has been called

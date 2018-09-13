from api.app import app
import unittest
import json

class TestApiEndpoints(unittest.TestCase):
    	
	def setUp(self):
		self.tester = app.test_client(self)
		#a typical order
		self.data = json.dumps(
				{
                    "id":1,
                    "content":"shuwarma",
                    "price":100,
                    'date': '12-9-18',
					"completed":False
                }
				            )
	def test_if_all_orders_returned(self):
		response = self.tester.get('/api/v1/orders')
		self.assertEqual(response.status_code, 200)
	
	def test_for_error_returned_when_no_content_in_order(self):
		dummy_data = json.dumps(
			{
				"id":1,
				"content":" ",
				"price":100,
				'date': '5-6-8',
				"completed":False
				}
			)
		response = self.tester.post('/api/v1/orders', data=dummy_data, content_type = 'application/json')
		self.assertEqual(response.status_code, 400)	
		self.assertIn(b"No order made,please add order and try again", response.data)   	

	def test_for_error_when_no_price_in_order(self):
		dummy_data = json.dumps(
		{
			"id":1,
			"content":"Chicken",
			"price":" ",
			'date': '5-6-8',
			"completed":False
			}
		)
		response = self.tester.post('/api/v1/orders', data=dummy_data, content_type = 'application/json')
		self.assertEqual(response.status_code, 400)	
		self.assertIn(b"This order has no price, please verify the price and try again", response.data)

	def test_for_error_if_type_price_not_interger(self):
		dummy_data = json.dumps(
		{
		"content":"Beef",
		"price":"iops"
		}
		)	
		response = self.tester.post('/api/v1/orders', data=dummy_data, content_type = 'application/json')
		self.assertEqual(response.status_code, 400)	
		self.assertIn(b"please add a valid unit price", response.data)	

	def test_for_error_when_no_content_in_keys(self):	
		dummy_data = json.dumps(
			{
			"id":1,
			"price":100,
			'date': '5-6-8',
			"completed":False
			}
		)	
		response = self.tester.post('/api/v1/orders', data=dummy_data, content_type = 'application/json')
		self.assertEqual(response.status_code, 400)	
		self.assertIn(b"No order made,please add order and try again", response.data)

	def test_if_single_order_returned(self):
		response = self.tester.get('/api/v1/orders/1')
		self.assertEqual(response.status_code, 200)	

	def test_for_error_if_order_id_not_in_all_orders(self):
		response = self.tester.get('/api/v1/orders/8')
		self.assertEqual(response.status_code, 404)	
		self.assertIn(b"no order with the given id, please try again", response.data)

	def test_for_error_if_type_status_not_boolean(self):
		dummy_data = json.dumps(
			{
			"completed":" "
			}
		)	
		response = self.tester.put('/api/v1/orders/1', data=dummy_data, content_type = 'application/json')
		self.assertEqual(response.status_code, 400)	
		self.assertIn(b"please add a boolean value to change the status", response.data)

	def test_for_error_if_completed_not_in_input(self):
		dummy_data = json.dumps(
				{

				}
			)	
		response = self.tester.put('/api/v1/orders/1', data=dummy_data, content_type = 'application/json')
		self.assertEqual(response.status_code, 400)
		self.assertIn(b"please add a new status", response.data)

	def test_for_successful_update_of_status(self):
		dummy_data = json.dumps(
		{
		"completed":True
		}
		)	
		response = self.tester.put('/api/v1/orders/1', data=dummy_data, content_type = 'application/json')
		self.assertEqual(response.status_code, 200)	
	
		
if __name__ == "__main__":
    unittest.main()

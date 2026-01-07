from django.conf import settings
import requests

class CashfreePaymentService:
    base_url='https://sandbox.cashfree.com'
    client_key=settings.CASHFREE_CLIENT_ID
    client_secret=settings.CASHFREE_CLIENT_SECRET

    def __init__(self):
        self.headers = {
            "x-api-version": "2025-01-01",
            "x-client-id": self.client_key,
            "x-client-secret": self.client_secret,
            "Content-Type": "application/json"
        }

    def create_customer(self, email, first_name, last_name, phone_number):
        request_url=f'{self.base_url}/pg/customers'
        payload = {
            "customer_phone": phone_number,
            "customer_email": email,
            "customer_name": f'{first_name} {last_name}'
        }

        response = requests.post(request_url, json=payload, headers=self.headers)
        return response.json()

    def create_order(self, customer_id, customer_phone, amount, description, currency="INR"):
        request_url=f'{self.base_url}/pg/orders'
        payload = {
            "order_currency": currency,
            "order_amount": amount,
            "order_note":description,
            "order_meta":{
                "return_url": "http://localhost:8000/dashboard",
                "payment_methods": "cc,dc,upi"
            },
            "customer_details": {
                "customer_id": customer_id,
                "customer_phone": customer_phone
            }
        }
        response = requests.post(request_url, json=payload, headers=self.headers)
        return response.json()
# tests/test_serializers.py

from django.test import TestCase
from django.contrib.auth.models import User
from commission.models import Client, Transaction, Product
from commission.serializers import ClientSerializer, TransactionSerializer

class SerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'display_name': 'John Doe',
            'email': 'john@example.com'
        }
        self.client_obj = Client.objects.create(**self.client_data)
        self.product = Product.objects.create(name='Test Product', category='INSURANCE')

    def test_client_serializer(self):
        serializer = ClientSerializer(instance=self.client_obj)
        for key, value in self.client_data.items():
            self.assertEqual(serializer.data[key], value)

    def test_transaction_serializer(self):
        transaction = Transaction.objects.create(
            agent=self.user,
            client=self.client_obj,
            product=self.product,
            metadata={'amount': 1000}
        )
        serializer = TransactionSerializer(instance=transaction)
        self.assertEqual(serializer.data['agent'], self.user.id)
        self.assertEqual(serializer.data['client']['id'], self.client_obj.id)
        self.assertEqual(serializer.data['product'], self.product.id)
        self.assertEqual(serializer.data['metadata'], {'amount': 1000})
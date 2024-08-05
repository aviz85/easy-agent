# tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from commission.models import Transaction, Agreement, Client, Product, InsuranceCompany, PaymentTerms, CommissionStructure
import json

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)
        self.test_client = Client.objects.create(display_name="Test Client")
        self.test_product = Product.objects.create(name="Test Product", category="INSURANCE")
        self.insurance_company = InsuranceCompany.objects.create(name="Test Insurance Company")
        self.payment_terms = PaymentTerms.objects.create(payment_type='DAY_OF_MONTH', day_of_month=1)
        self.agreement = Agreement.objects.create(agent=self.user, company=self.insurance_company)

    def test_agreement_list(self):
        url = reverse('agreement-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_calculate_commission(self):
        url = reverse('calculate-commission')
        commission_structure = CommissionStructure.objects.create(
            agent=self.user,
            product=self.test_product,
            commission_type='SCOPE',
            rate=10,
            payment_terms=self.payment_terms,
            agreement=self.agreement
        )
        transaction = Transaction.objects.create(
            agent=self.user,
            client=self.test_client,
            product=self.test_product,
            metadata={'amount': 1000}
        )
        data = {'transaction_id': transaction.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('commissions', response.data)
        self.assertEqual(len(response.data['commissions']), 1)
        self.assertEqual(response.data['commissions'][0]['amount'], '100.00')  # 10% of 1000

    def test_submit_meeting_summary(self):
        url = reverse('submit-meeting-summary')
        data = {'content': 'Test meeting summary'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('summary', response.data)
        self.assertIn('transaction', response.data)

    def test_transaction_list(self):
        url = reverse('transaction-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_transaction_create(self):
        url = reverse('transaction-list')
        data = {
            'client_id': self.test_client.id,
            'product': self.test_product.id,
            'metadata': json.dumps({'some_key': 'some_value'})
        }
        response = self.client.post(url, data, format='json')
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.first().agent, self.user)

    def test_logout(self):
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_profile(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password(self):
        url = reverse('change-password')
        data = {'old_password': '12345', 'new_password': 'newpassword123'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
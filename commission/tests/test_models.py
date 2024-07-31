# commission/tests/test_models.py

from django.test import TestCase
from django.contrib.auth.models import User
from commission.models import InsuranceCompany, Product, Agreement, PaymentTerms, CommissionStructure, Transaction, Commission
from django.utils import timezone

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.company = InsuranceCompany.objects.create(name='Test Insurance Co', contact_info='Contact Info')
        self.product = Product.objects.create(name='Test Product', category='INSURANCE', type='Life', description='Test Description')
        self.agreement = Agreement.objects.create(
            agent=self.user,
            company=self.company,
            start_date=timezone.now().date(),
            terms={'test': 'terms'}
        )
        self.payment_terms = PaymentTerms.objects.create(
            payment_type='DAY_OF_MONTH',
            day_of_month=15
        )
        self.commission_structure = CommissionStructure.objects.create(
            agreement=self.agreement,
            product=self.product,
            commission_type='SCOPE',
            rate=10.00,
            payment_terms=self.payment_terms
        )

    def test_insurance_company_creation(self):
        self.assertTrue(isinstance(self.company, InsuranceCompany))
        self.assertEqual(self.company.__str__(), self.company.name)

    def test_product_creation(self):
        self.assertTrue(isinstance(self.product, Product))
        self.assertEqual(self.product.__str__(), f"{self.product.name} (Insurance)")

    def test_agreement_creation(self):
        self.assertTrue(isinstance(self.agreement, Agreement))
        self.assertEqual(self.agreement.__str__(), f"Agreement between testuser and Test Insurance Co")

    def test_commission_structure_creation(self):
        self.assertTrue(isinstance(self.commission_structure, CommissionStructure))
        self.assertEqual(self.commission_structure.__str__(), "Scope Commission for Test Product")

    def test_transaction_creation(self):
        transaction = Transaction.objects.create(
            agent=self.user,
            client_name='Test Client',
            product=self.product,
            date=timezone.now().date(),
            status='COMPLETED',
            details={'amount': 1000}
        )
        self.assertTrue(isinstance(transaction, Transaction))
        self.assertEqual(transaction.__str__(), "Transaction for Test Client - Test Product")

    def test_commission_creation(self):
        transaction = Transaction.objects.create(
            agent=self.user,
            client_name='Test Client',
            product=self.product,
            date=timezone.now().date(),
            status='COMPLETED',
            details={'amount': 1000}
        )
        commission = Commission.objects.create(
            transaction=transaction,
            commission_structure=self.commission_structure,
            amount=100.00,
            expected_payment_date=timezone.now().date(),
            status='PENDING'
        )
        self.assertTrue(isinstance(commission, Commission))
        self.assertEqual(commission.__str__(), f"Commission for {transaction}")

# commission/tests/test_services.py

from django.test import TestCase
from django.contrib.auth.models import User
from commission.models import InsuranceCompany, Product, Agreement, PaymentTerms, CommissionStructure, Transaction
from commission.services import calculate_commission
from django.utils import timezone

class CalculateCommissionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.company = InsuranceCompany.objects.create(name='Test Insurance Co', contact_info='Contact Info')
        self.product = Product.objects.create(name='Test Product', category='INSURANCE', type='Life', description='Test Description')
        self.agreement = Agreement.objects.create(
            agent=self.user,
            company=self.company,
            start_date=timezone.now().date(),
            terms={'test': 'terms'}
        )
        self.payment_terms = PaymentTerms.objects.create(
            payment_type='DAY_OF_MONTH',
            day_of_month=15
        )
        self.commission_structure = CommissionStructure.objects.create(
            agreement=self.agreement,
            product=self.product,
            commission_type='SCOPE',
            rate=10.00,
            payment_terms=self.payment_terms
        )
        self.transaction = Transaction.objects.create(
            agent=self.user,
            client_name='Test Client',
            product=self.product,
            date=timezone.now().date(),
            status='COMPLETED',
            details={'amount': 1000}
        )

    def test_calculate_commission(self):
        commissions = calculate_commission(self.transaction)
        self.assertEqual(len(commissions), 1)
        commission = commissions[0]
        self.assertEqual(commission.amount, 100.00)  # 10% of 1000
        self.assertEqual(commission.status, 'PENDING')
        self.assertEqual(commission.commission_structure, self.commission_structure)

# commission/tests/test_views.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from commission.models import InsuranceCompany, Product, Transaction

class APIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.company = InsuranceCompany.objects.create(name='Test Insurance Co', contact_info='Contact Info')
        self.product = Product.objects.create(name='Test Product', category='INSURANCE', type='Life', description='Test Description')

    def test_create_transaction(self):
        url = reverse('transaction-list')
        data = {
            'agent': self.user.id,
            'client_name': 'Test Client',
            'product': self.product.id,
            'date': '2023-05-01',
            'status': 'COMPLETED',
            'details': {'amount': 1000}
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get().client_name, 'Test Client')

    def test_calculate_commission(self):
        transaction = Transaction.objects.create(
            agent=self.user,
            client_name='Test Client',
            product=self.product,
            date='2023-05-01',
            status='COMPLETED',
            details={'amount': 1000}
        )
        url = reverse('calculate-commission')
        data = {'transaction_id': transaction.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Add more assertions based on your expected response

    def test_list_transactions(self):
        Transaction.objects.create(
            agent=self.user,
            client_name='Test Client 1',
            product=self.product,
            date='2023-05-01',
            status='COMPLETED',
            details={'amount': 1000}
        )
        Transaction.objects.create(
            agent=self.user,
            client_name='Test Client 2',
            product=self.product,
            date='2023-05-02',
            status='PENDING',
            details={'amount': 2000}
        )
        url = reverse('transaction-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_transactions(self):
        Transaction.objects.create(
            agent=self.user,
            client_name='Test Client 1',
            product=self.product,
            date='2023-05-01',
            status='COMPLETED',
            details={'amount': 1000}
        )
        Transaction.objects.create(
            agent=self.user,
            client_name='Test Client 2',
            product=self.product,
            date='2023-05-02',
            status='PENDING',
            details={'amount': 2000}
        )
        url = reverse('transaction-list')
        response = self.client.get(f"{url}?status=COMPLETED", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['client_name'], 'Test Client 1')
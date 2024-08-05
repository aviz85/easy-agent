# tests/test_models.py

from django.test import TestCase
from django.contrib.auth.models import User
from commission.models import Agreement, InsuranceCompany, CommissionStructure, Product, PaymentTerms, Transaction, Client

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.insurance_company = InsuranceCompany.objects.create(name='Test Insurance Company')
        self.product = Product.objects.create(name='Test Product', category='INSURANCE')
        self.payment_terms = PaymentTerms.objects.create(payment_type='DAY_OF_MONTH', day_of_month=1)
        self.agreement = Agreement.objects.create(agent=self.user, company=self.insurance_company)
        self.commission_structure = CommissionStructure.objects.create(
            agent=self.user,
            product=self.product,
            commission_type='SCOPE',
            rate=10.00,
            payment_terms=self.payment_terms,
            agreement=self.agreement
        )
        self.client = Client.objects.create(
            first_name='Test',
            last_name='Client',
            display_name='Test Client'
        )

    def test_agreement_creation(self):
        self.assertEqual(str(self.agreement), f"Agreement between {self.user.username} and {self.insurance_company.name}")

    def test_client_creation(self):
        self.assertEqual(str(self.client), 'Test Client')

    def test_transaction_creation(self):
        transaction = Transaction.objects.create(
            agent=self.user,
            client=self.client,
            product=self.product,
            metadata={'amount': 1000}
        )
        self.assertEqual(str(transaction), f"Transaction for {self.client.display_name} - {self.product.name}")
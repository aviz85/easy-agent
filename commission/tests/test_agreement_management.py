# commission/tests/test_agreement_management.py

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import InsuranceCompany, Product, PaymentTerms, Agreement, CommissionStructure


class AgreementManagementTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.client.force_authenticate(user=self.user)
        self.company = InsuranceCompany.objects.create(name='Test Insurance Co', contact_info='Contact Info')
        self.product = Product.objects.create(name='Test Product', category='INSURANCE', type='Life', description='Test Description')

    def test_create_agreement(self):
        url = reverse('agreement-list')
        data = {
            'company': {
                'name': 'New Insurance Co',
                'contact_info': 'New Contact Info'
            },
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'terms': {'some': 'terms'},
            'status': 'ACTIVE',
            'commission_structures': [
                {
                    'product': self.product.id,
                    'commission_type': 'SCOPE',
                    'rate': '10.00',
                    'payment_terms': {
                        'payment_type': 'DAY_OF_MONTH',
                        'day_of_month': 15
                    }
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Agreement.objects.count(), 1)
        self.assertEqual(CommissionStructure.objects.count(), 1)
        self.assertEqual(PaymentTerms.objects.count(), 1)
        
        # Check if the agreement is associated with the correct user
        agreement = Agreement.objects.first()
        self.assertEqual(agreement.agent, self.user)
        
        # Check if the nested objects are created correctly
        self.assertEqual(agreement.company.name, 'New Insurance Co')
        self.assertEqual(agreement.commission_structures.count(), 1)
        commission_structure = agreement.commission_structures.first()
        self.assertEqual(commission_structure.product, self.product)
        self.assertEqual(commission_structure.payment_terms.payment_type, 'DAY_OF_MONTH')

    def test_list_active_agreements(self):
        # Create an active agreement
        Agreement.objects.create(
            agent=self.user,
            company=self.company,
            start_date='2023-01-01',
            end_date='2023-12-31',
            terms={'some': 'terms'},
            status='ACTIVE'
        )
        # Create an inactive agreement
        Agreement.objects.create(
            agent=self.user,
            company=self.company,
            start_date='2023-01-01',
            end_date='2023-12-31',
            terms={'some': 'terms'},
            status='INACTIVE'
        )
        # Create an active agreement for another user
        other_user = User.objects.create_user(username='otheruser', password='testpassword123')
        Agreement.objects.create(
            agent=other_user,
            company=self.company,
            start_date='2023-01-01',
            end_date='2023-12-31',
            terms={'some': 'terms'},
            status='ACTIVE'
        )
        
        url = reverse('agreement-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only the active agreement for the current user should be listed

    def test_create_agreement_with_existing_company(self):
        url = reverse('agreement-list')
        data = {
            'company': {
                'name': 'Test Insurance Co',
                'contact_info': 'Updated Contact Info'
            },
            'start_date': '2023-01-01',
            'end_date': '2023-12-31',
            'terms': {'some': 'terms'},
            'status': 'ACTIVE',
            'commission_structures': [
                {
                    'product': self.product.id,
                    'commission_type': 'SCOPE',
                    'rate': '10.00',
                    'payment_terms': {
                        'payment_type': 'DAY_OF_MONTH',
                        'day_of_month': 15
                    }
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InsuranceCompany.objects.count(), 1)  # The existing company should be used
        self.assertEqual(Agreement.objects.count(), 1)
 
    def test_create_agreement_invalid_data(self):
        url = reverse('agreement-list')
        data = {
            'company': {
                'name': 'New Insurance Co',
                'contact_info': 'New Contact Info'
            },
            'start_date': '2023-01-01',
            'end_date': '2022-12-31',  # End date before start date
            'terms': {'some': 'terms'},
            'status': 'ACTIVE',
            'commission_structures': []  # No commission structures
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('end_date', response.data)
        self.assertIn('commission_structures', response.data)
        self.assertEqual(Agreement.objects.count(), 0)

class ComplexAgreementTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.client.force_authenticate(user=self.user)
        
        # Create multiple companies
        self.company1 = InsuranceCompany.objects.create(name='Insurance Co 1', contact_info='Contact 1')
        self.company2 = InsuranceCompany.objects.create(name='Insurance Co 2', contact_info='Contact 2')
        
        # Create multiple products
        self.product1 = Product.objects.create(name='Life Insurance', category='INSURANCE', type='Life', description='Life insurance product')
        self.product2 = Product.objects.create(name='Health Insurance', category='INSURANCE', type='Health', description='Health insurance product')
        self.product3 = Product.objects.create(name='Pension Plan', category='PENSION', type='Retirement', description='Pension plan product')

    def create_complex_agreement(self, company):
        url = reverse('agreement-list')
        data = {
            'company': {
                'name': company.name,
                'contact_info': company.contact_info
            },
            'start_date': '2023-01-01',
            'end_date': '2024-12-31',
            'terms': {'some': 'complex terms'},
            'status': 'ACTIVE',
            'commission_structures': [
                {
                    'product': self.product1.id,
                    'commission_type': 'SCOPE',
                    'rate': '10.00',
                    'payment_terms': {
                        'payment_type': 'DAY_OF_MONTH',
                        'day_of_month': 15
                    }
                },
                {
                    'product': self.product1.id,
                    'commission_type': 'RECURRING',
                    'rate': '2.00',
                    'payment_terms': {
                        'payment_type': 'SPECIFIC_DATE',
                        'specific_date': '2023-12-31'
                    }
                },
                {
                    'product': self.product2.id,
                    'commission_type': 'SCOPE',
                    'rate': '15.00',
                    'payment_terms': {
                        'payment_type': 'DAY_OF_MONTH',
                        'day_of_month': 1
                    }
                },
                {
                    'product': self.product3.id,
                    'commission_type': 'TRAIL',
                    'rate': '0.50',
                    'payment_terms': {
                        'payment_type': 'DAY_OF_MONTH',
                        'day_of_month': 30
                    }
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        return response

    def test_create_complex_agreements(self):
        # Create complex agreement for company 1
        response1 = self.create_complex_agreement(self.company1)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Create complex agreement for company 2
        response2 = self.create_complex_agreement(self.company2)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        
        # Verify the number of created objects
        self.assertEqual(Agreement.objects.count(), 2)
        self.assertEqual(CommissionStructure.objects.count(), 8)  # 4 per agreement
        self.assertEqual(PaymentTerms.objects.count(), 8)  # 1 per commission structure

    def test_retrieve_complex_agreements(self):
        # Create complex agreements
        self.create_complex_agreement(self.company1)
        self.create_complex_agreement(self.company2)
        
        # Retrieve all agreements
        url = reverse('agreement-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Verify the structure of the first agreement
        agreement = response.data[0]
        self.assertEqual(len(agreement['commission_structures']), 4)
        
        # Verify that each product has the correct number of commission structures
        product_commission_count = {}
        for structure in agreement['commission_structures']:
            product_id = structure['product']
            product_commission_count[product_id] = product_commission_count.get(product_id, 0) + 1
        
        self.assertEqual(product_commission_count[self.product1.id], 2)
        self.assertEqual(product_commission_count[self.product2.id], 1)
        self.assertEqual(product_commission_count[self.product3.id], 1)

    def test_filter_agreements_by_company(self):
        # Create complex agreements
        self.create_complex_agreement(self.company1)
        self.create_complex_agreement(self.company2)
        
        # Retrieve agreements for company 1
        url = reverse('agreement-list')
        response = self.client.get(url, {'company': self.company1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['company']['name'], self.company1.name)

    def test_update_complex_agreement(self):
        # Create a complex agreement
        response = self.create_complex_agreement(self.company1)
        agreement_id = response.data['id']
        
        # Update the agreement
        url = reverse('agreement-detail', args=[agreement_id])
        update_data = {
            'company': {
                'name': self.company1.name,
                'contact_info': 'Updated Contact Info'
            },
            'start_date': '2023-02-01',
            'end_date': '2025-01-31',
            'terms': {'updated': 'terms'},
            'status': 'ACTIVE',
            'commission_structures': [
                {
                    'product': self.product1.id,
                    'commission_type': 'SCOPE',
                    'rate': '12.00',
                    'payment_terms': {
                        'payment_type': 'DAY_OF_MONTH',
                        'day_of_month': 20
                    }
                },
                {
                    'product': self.product2.id,
                    'commission_type': 'RECURRING',
                    'rate': '3.00',
                    'payment_terms': {
                        'payment_type': 'SPECIFIC_DATE',
                        'specific_date': '2024-06-30'
                    }
                }
            ]
        }
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the updated agreement
        updated_agreement = Agreement.objects.get(id=agreement_id)
        self.assertEqual(updated_agreement.start_date.isoformat(), '2023-02-01')
        self.assertEqual(updated_agreement.end_date.isoformat(), '2025-01-31')
        self.assertEqual(updated_agreement.terms, {'updated': 'terms'})
        self.assertEqual(updated_agreement.commission_structures.count(), 2)

    def test_delete_agreement(self):
        # Create a complex agreement
        response = self.create_complex_agreement(self.company1)
        agreement_id = response.data['id']
        
        # Delete the agreement
        url = reverse('agreement-detail', args=[agreement_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify the agreement is deleted
        self.assertEqual(Agreement.objects.count(), 0)
        self.assertEqual(CommissionStructure.objects.count(), 0)
        # Note: We might want to keep PaymentTerms, as they could be shared across agreements
        # self.assertEqual(PaymentTerms.objects.count(), 0)

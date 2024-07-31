from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from commission.models import MeetingSummary, Transaction
from unittest.mock import patch

class SubmitMeetingSummaryViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)

    @patch('commission.gateways.GroqGateway.extract_meeting_summary_info')
    def test_submit_meeting_summary(self, mock_extract):
        # Mock the GroqGateway response
        mock_extract.return_value = {
            "client_name": "Jane Smith",
            "product_name": "Term Insurance",
            "product_category": "INSURANCE",
            "product_type": "Term",
            "amount": 10000.00
        }

        url = reverse('submit-meeting-summary')
        data = {
            'content': """
            Meeting Summary:
            Met with Jane Smith today. She's looking for short-term coverage.
            We discussed our Term Insurance product with a coverage of $10,000.00.
            Jane is considering this option for the next few years.
            """
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('summary', response.data)
        self.assertIn('transaction', response.data)
        
        self.assertEqual(MeetingSummary.objects.count(), 1)
        self.assertEqual(Transaction.objects.count(), 1)
        
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.client_name, 'Jane Smith')
        self.assertEqual(transaction.product.name, 'Term Insurance')
        self.assertEqual(transaction.details['amount'], 10000.00)

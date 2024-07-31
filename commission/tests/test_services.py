# commission/tests/test_services.py

from django.test import TestCase
from django.contrib.auth.models import User
from commission.services import process_meeting_summary
from commission.models import MeetingSummary, Transaction
from unittest.mock import patch
import json

class MeetingSummaryTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    @patch('commission.gateways.GroqGateway.extract_meeting_summary_info')
    def test_process_meeting_summary(self, mock_extract):
        # Mock the GroqGateway response
        mock_extract.return_value = {
            "client_name": "John Doe",
            "product_name": "Life Insurance",
            "product_category": "INSURANCE",
            "product_type": "Life",
            "amount": 5000.00
        }

        content = """
        Meeting Summary:
        Had a great meeting with John Doe today. He's interested in our Life Insurance product.
        We discussed a coverage amount of $5,000.00. John seems very keen on long-term protection for his family.
        """

        summary, transaction = process_meeting_summary(self.user, content)

        self.assertIsNotNone(summary)
        self.assertEqual(summary.processed_status, 'SUCCESS')
        
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.client_name, 'John Doe')
        self.assertEqual(transaction.product.name, 'Life Insurance')
        self.assertEqual(transaction.product.category, 'INSURANCE')
        self.assertEqual(transaction.product.type, 'Life')
        self.assertEqual(transaction.details['amount'], 5000.00)

# commission/tests/test_views.py
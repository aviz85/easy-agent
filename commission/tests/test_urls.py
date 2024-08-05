# tests/test_urls.py

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User

class URLTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)

    def test_transaction_url(self):
        url = reverse('transaction-list')
        self.assertEqual(url, '/api/transactions/')

    def test_agreement_url(self):
        url = reverse('agreement-list')
        self.assertEqual(url, '/api/agreements/')

    def test_register_url(self):
        url = reverse('register')
        self.assertEqual(url, '/api/register/')

    def test_profile_url(self):
        url = reverse('profile')
        self.assertEqual(url, '/api/profile/')

    def test_change_password_url(self):
        url = reverse('change-password')
        self.assertEqual(url, '/api/change-password/')

    def test_submit_meeting_summary_url(self):
        url = reverse('submit-meeting-summary')
        self.assertEqual(url, '/api/submit-meeting-summary/')

    def test_calculate_commission_url(self):
        url = reverse('calculate-commission')
        self.assertEqual(url, '/api/calculate-commission/')

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(url, '/api/login/')

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(url, '/api/logout/')
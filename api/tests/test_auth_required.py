#test- auth required (401 without token)

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class AuthRequiredTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_requires_auth(self):
        r = self.client.get("/api/tasks/")
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

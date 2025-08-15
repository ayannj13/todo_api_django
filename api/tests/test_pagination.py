#test for pagination

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.models import Task

User = get_user_model()

class PaginationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="p", password="Pass12345")
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        # creates more than one page of tasks
        self.total = settings.REST_FRAMEWORK.get("PAGE_SIZE", 10) + 3
        for i in range(self.total):
            Task.objects.create(title=f"t{i}", status=Task.Status.NEW, user=self.user)

        self.list_url = reverse("task-list")  # /api/tasks/

    def test_first_page_limited_to_page_size(self):
        r = self.client.get(self.list_url)  # page 1 by default
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["count"], self.total)
        self.assertEqual(len(r.data["results"]), settings.REST_FRAMEWORK["PAGE_SIZE"])
        self.assertIsNotNone(r.data["next"])
        self.assertIsNone(r.data["previous"])

    def test_second_page_has_remaining_items(self):
        r = self.client.get(self.list_url, {"page": 2})
        self.assertEqual(r.status_code, status.HTTP_200_OK)

        remaining = self.total - settings.REST_FRAMEWORK["PAGE_SIZE"]
        self.assertEqual(len(r.data["results"]), remaining)
        self.assertIsNone(r.data["next"])
        self.assertIsNotNone(r.data["previous"])

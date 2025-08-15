#test for getting task details

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.models import Task

User = get_user_model()

class RetrieveTaskTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="Pass12345")
        self.other = User.objects.create_user(username="other", password="Pass12345")

        self.task = Task.objects.create(
            title="See me",
            description="detail test",
            status=Task.Status.NEW, 
            user=self.owner,
        )
        self.detail_url = reverse("task-detail", args=[self.task.id])

        self.client = APIClient()

    def test_owner_can_view_task_detail(self):
        self.client.force_authenticate(self.owner)
        r = self.client.get(self.detail_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["id"], self.task.id)
        self.assertEqual(r.data["title"], "See me")
        self.assertEqual(r.data["user"], self.owner.username)

    def test_other_authenticated_user_can_view_task_detail(self):
        # allows any authenticated user to see details
        self.client.force_authenticate(self.other)
        r = self.client.get(self.detail_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["id"], self.task.id)

    def test_unauthenticated_user_cannot_view_task_detail(self):
        # no authentication
        r = self.client.get(self.detail_url)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

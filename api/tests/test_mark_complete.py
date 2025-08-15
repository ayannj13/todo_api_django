#test for marking task as completed

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.models import Task

User = get_user_model()

class MarkCompleteTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="me", password="Pass12345")
        self.other = User.objects.create_user(username="you", password="Pass12345")
        self.task = Task.objects.create(
            title="finish me",
            status=Task.Status.NEW,  
            user=self.owner,
        )
        self.client = APIClient()
        self.url = reverse("task-complete", args=[self.task.id])  # /api/tasks/<id>/complete/

    def test_owner_can_mark_completed(self):
        self.client.force_authenticate(self.owner)
        r = self.client.post(self.url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, Task.Status.COMPLETED)

    def test_non_owner_cannot_mark_completed(self):
        self.client.force_authenticate(self.other)
        r = self.client.post(self.url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, Task.Status.NEW)

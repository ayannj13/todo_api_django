#test updating

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.models import Task

User = get_user_model()

class UpdateTaskTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="u1", password="p@ssw0rd1")
        self.other = User.objects.create_user(username="u2", password="p@ssw0rd2")
        self.task = Task.objects.create(
            title="Original",
            description="d",
            status=Task.Status.NEW,  
            user=self.owner,
        )
        self.client = APIClient()
        self.url = reverse("task-detail", args=[self.task.id])  # /api/tasks/<id>/

    def test_owner_can_update_title(self):
        self.client.force_authenticate(self.owner)
        r = self.client.patch(self.url, {"title": "Updated"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated")

    def test_non_owner_cannot_update(self):
        self.client.force_authenticate(self.other)
        r = self.client.patch(self.url, {"title": "Hack"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Original")
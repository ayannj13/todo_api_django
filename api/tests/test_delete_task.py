#test for delete permissions 

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.models import Task

User = get_user_model()

class DeleteTaskTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="p@ss1Aaa")
        self.other = User.objects.create_user(username="other", password="p@ss1Bbb")
        self.task = Task.objects.create(
            title="Delete-me",
            status=Task.Status.NEW,  
            user=self.owner,
        )
        self.client = APIClient()
        self.url = reverse("task-detail", args=[self.task.id])  # /api/tasks/<id>/

    def test_owner_can_delete(self):
        self.client.force_authenticate(self.owner)
        r = self.client.delete(self.url)
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_non_owner_cannot_delete(self):
        self.client.force_authenticate(self.other)
        r = self.client.delete(self.url)
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

        self.assertTrue(Task.objects.filter(id=self.task.id).exists())
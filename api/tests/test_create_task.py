#test for task creation

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.models import Task

User = get_user_model()

class CreateTaskTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="u1", password="pass12345", first_name="U", last_name="One"
        )
        self.client.force_authenticate(self.user)

    def test_create_task_sets_owner(self):
        url = reverse("task-list")  
        payload = {
            "title": "Write README",
            "description": "Add install + run steps",
            "status": "NEW"
        }

        res = self.client.post(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # 1 task created
        self.assertEqual(Task.objects.count(), 1)

        task = Task.objects.get()
        # owner is the authenticated user
        self.assertEqual(task.user, self.user)

        #response body
        self.assertEqual(res.data["title"], "Write README")
        self.assertEqual(res.data["status"], "NEW")
        self.assertEqual(res.data["user"], self.user.username)

    def test_title_is_required(self):
        url = reverse("task-list")
        res = self.client.post(url, {"description": "no title"}, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        # DRF should alert if there's missing title
        self.assertIn("title", res.data)

# test for task listing, my tasks, status filtering

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.models import Task

User = get_user_model()

class ListAndFilterTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # two users
        self.u1 = User.objects.create_user(
            username="ann", password="pass12345", first_name="Ann"
        )
        self.u2 = User.objects.create_user(
            username="bob", password="pass12345", first_name="Bob"
        )

        # tasks 
        Task.objects.create(title="t1", description="", status="NEW",         user=self.u1)
        Task.objects.create(title="t2", description="", status="IN_PROGRESS", user=self.u1)
        Task.objects.create(title="t3", description="", status="COMPLETED",   user=self.u2)

        # authenticate 
        self.client.force_authenticate(self.u1)

    def test_list_all_tasks(self):
        url = reverse("task-list")  # tasks
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # pagination response
        self.assertEqual(res.data["count"], 3)
        titles = [item["title"] for item in res.data["results"]]
        self.assertCountEqual(titles, ["t1", "t2", "t3"])

    def test_list_my_tasks_only(self):
        url = reverse("task-my")  # my tasks
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 2)
        owners = {item["user"] for item in res.data["results"]}
        self.assertEqual(owners, {"ann"})

    def test_filter_by_status(self):
        url = reverse("task-list")  # filtering tasks by status
        res = self.client.get(url, {"status": "IN_PROGRESS"})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 1)
        self.assertEqual(res.data["results"][0]["title"], "t2")
        self.assertEqual(res.data["results"][0]["status"], "IN_PROGRESS")

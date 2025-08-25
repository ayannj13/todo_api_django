from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()

class RegistrationTests(APITestCase):
    def test_user_can_register_and_get_token(self):
        #register
        res = self.client.post(
            "/api/register/",
            {
                "username": "newuser",
                "first_name": "New",
                "last_name": "User",
                "password": "secret1",
            },
            format="json",
        )
        self.assertEqual(res.status_code, 201)
        self.assertTrue(User.objects.filter(username="newuser").exists())
        # get JWT
        res2 = self.client.post(
            "/api/token/",
            {"username": "newuser", "password": "secret1"},
            format="json",
        )
        self.assertEqual(res2.status_code, 200)
        self.assertIn("access", res2.data)

    def test_min_password_length(self):
        res = self.client.post(
            "/api/register/",
            {"username": "shortpass", "password": "123"},
            format="json",
        )
        self.assertEqual(res.status_code, 400)
    def test_duplicate_username_rejected(self):
        User.objects.create_user(username="dupe", password="secret1")
        res = self.client.post(
            "/api/register/",
            {"username": "dupe", "password": "secret1"},
            format="json",
        )
        self.assertEqual(res.status_code, 400)
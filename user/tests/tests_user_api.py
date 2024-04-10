from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model

USER_URL = reverse("users:register")

DEFAULT_USER = {
    "email": "test@gmail.com",
    "password": "test1"
}


def get_url(part: str):
    return f"{USER_URL}{part}"


class UnauthenticatedUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        res = self.client.post(USER_URL, DEFAULT_USER)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


class AuthenticatedOrAdminUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="auth@gmail.com",
            password="test"
        )
        self.client.force_authenticate(self.user)

    def test_create_user(self):
        res = self.client.post(USER_URL, DEFAULT_USER)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_get_profile(self):
        res = self.client.get(get_url("me/"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_profile(self):
        res = self.client.patch(get_url("me/"), {"email": "updated@gamail.com"})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_token(self):
        res = self.client.post(get_url("token/"), {
            "email": "auth@gmail.com", "password": "test"
        })
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_refresh_token(self):
        get_token = self.client.post(get_url("token/"), {
            "email": "auth@gmail.com", "password": "test"
        })
        token = get_token.data["refresh"]

        res = self.client.post(get_url("token/refresh/"), {"refresh": str(token)})

        self.assertEqual(res.status_code, status.HTTP_200_OK)


class AdminBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@gmail.com",
            password="admin",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_update_profile(self):
        res = self.client.patch(get_url("me/"), {"email": "updated@gamail.com"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, "updated@gamail.com")

    def test_delite_profile(self):
        res = self.client.delete(get_url("me/"))
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

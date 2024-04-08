from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from books_service.models import Book
from books_service.serializers import BookSerializer

BOOK_URL = reverse("books:book-list")
DEFAULT_BOOK = {
    "title": "test",
    "author": "ya",
    "cover": "HARD",
    "inventory": 1,
    "daily_fee": 10,
}


def detail_book_url(book_id: int):
    return BOOK_URL + f"{book_id}/"


def create_book(
    title: str = "title",
    author: str = "author",
    cover: str = "HARD",
    inventory: int = "1",
    daily_fee: int = 10,
):
    return Book.objects.create(
        title=title,
        author=author,
        cover=cover,
        inventory=inventory,
        daily_fee=daily_fee,
    )


class UnauthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get(self):
        create_book()
        create_book()
        res = self.client.get(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_get_detail(self):
        book1 = create_book()
        create_book()
        res = self.client.get(detail_book_url(book1.id))
        serializer_book = BookSerializer(book1)

        self.assertEqual(res.data, serializer_book.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create(self):
        res = self.client.post(
            BOOK_URL,
            DEFAULT_BOOK,
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="auth@gmail.com",
            password="test"
        )
        self.client.force_authenticate(self.user)

    def test_get(self):
        create_book()
        create_book()
        create_book()
        res = self.client.get(BOOK_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

    def test_create(self):
        res = self.client.post(
            BOOK_URL,
            DEFAULT_BOOK,
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        book1 = create_book()
        res = self.client.delete(detail_book_url(book1.id))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@gmail.com",
            password="admin",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create(self):
        res = self.client.post(
            BOOK_URL,
            DEFAULT_BOOK,
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_delete(self):
        book1 = create_book()
        res = self.client.delete(detail_book_url(book1.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

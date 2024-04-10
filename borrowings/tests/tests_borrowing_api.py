from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model

from borrowings.models import Borrowing
from books_service.models import Book
from books_service.tests.tests_book_api import create_book

BORROWING_URL = reverse("borrowings:borrowings-list")


def borrowing_return_page(_id: int):
    return reverse("borrowings:borrowings-return", kwargs={"pk": _id})


def create_borrowing(
    borrow_date: str = "2020-02-02",
    expected_return_date: str = "2020-02-02",
    actual_return_date: str = "2020-02-02",
    user_email: str = "test@gmail.com",
):
    book = create_book()
    user = get_user_model().objects.create_user(
            email=user_email,
            password="test"
        )
    return Borrowing.objects.create(
        borrow_date=borrow_date,
        expected_return_date=expected_return_date,
        actual_return_date=actual_return_date,
        book=book,
        user=user,
    )


class UnauthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_all_borrowings(self):
        create_borrowing()
        create_borrowing(user_email="test2@gmail.com")
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_add_new_borrowing(self):
        res = self.client.post(BORROWING_URL, {})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="auth@gmail.com",
            password="test"
        )
        self.client.force_authenticate(self.user)

    def test_get_all_borrowings(self):
        create_borrowing()
        create_borrowing(user_email="test2@gmail.com")
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_get_by_user_id(self):
        borrowing = create_borrowing()
        create_borrowing(user_email="test12@gamil.com")
        res = self.client.get(BORROWING_URL,  {"user_id": borrowing.user.id})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        returned_borrowing_user_id = res.data[0]["user"]
        self.assertEqual(returned_borrowing_user_id, borrowing.user.id)

    def test_add_new_borrowing(self):
        res = self.client.post(BORROWING_URL, {})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        borrowing = create_borrowing()
        res = self.client.delete(borrowing_return_page(borrowing.id))
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

    def test_add_new_borrowing(self):
        book = create_book(inventory=1)
        user = get_user_model().objects.create_user(
            email="test@create.com",
            password="test"
        )
        current_books = book.inventory
        res = self.client.post(BORROWING_URL, {
            "borrow_date": "2020-02-02",
            "expected_return_date": "2020-02-02",
            "actual_return_date": "2020-02-02",
            "book": book.id,
            "user": user,
        })

        self.assertEqual(current_books - 1, Book.objects.get(id=res.data["book"]).inventory)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_return_borrowed_book(self):
        book = create_book(inventory=1)
        user = get_user_model().objects.create_user(
            email="test@create.com",
            password="test"
        )
        res = self.client.post(BORROWING_URL, {
            "borrow_date": "2020-02-02",
            "expected_return_date": "2020-02-02",
            "actual_return_date": "2020-02-02",
            "book": book.id,
            "user": user,
        })

        inventory_before_return = Book.objects.get(id=res.data["book"]).inventory

        return_res = self.client.delete(borrowing_return_page(res.data["id"]))
        inventory_after_return = Book.objects.get(id=res.data["book"]).inventory
        self.assertEqual(return_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(inventory_before_return + 1, inventory_after_return)



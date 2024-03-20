from django.db import models
from django.contrib.auth import get_user_model

from books_service.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="borrowings")

    def __str__(self):
        return f"book: {self.book}, user: {self.user}"

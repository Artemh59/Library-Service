from rest_framework import serializers

from borrowings.models import Borrowing
from books_service.serializers import BookSerializer


class BorrowingListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "user",
            "book",
        )

        read_only_fields = ("id", "user")


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True, many=False)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "user_id",
            "book",
        )

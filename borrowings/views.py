from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from borrowings.serializers import BorrowingListCreateSerializer, BorrowingDetailSerializer
from borrowings.models import Borrowing
from books_service.models import Book


class BorrowingListCreateView(ListCreateAPIView):
    serializer_class = BorrowingListCreateSerializer
    queryset = Borrowing.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()

        book_id = request.data.get("book")
        book = Book.objects.get(pk=book_id)

        self.perform_create(serializer)

        book.inventory -= 1
        book.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BorrowingDetailView(RetrieveAPIView):
    serializer_class = BorrowingDetailSerializer
    queryset = Borrowing.objects.all()

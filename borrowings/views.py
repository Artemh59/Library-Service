from rest_framework.generics import RetrieveAPIView, ListCreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status

from borrowings.serializers import BorrowingListCreateSerializer, BorrowingDetailSerializer
from borrowings.models import Borrowing
from books_service.models import Book


class BorrowingListCreateView(ListCreateAPIView):
    serializer_class = BorrowingListCreateSerializer
    queryset = Borrowing.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()

        user = request.user
        serializer.save(user=user)

        book_id = request.data.get("book")
        book = Book.objects.get(pk=book_id)

        self.perform_create(serializer)

        book.inventory -= 1
        book.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BorrowingDetailView(RetrieveAPIView):
    serializer_class = BorrowingDetailSerializer
    queryset = Borrowing.objects.all()


class BorrowingDestroyView(DestroyAPIView):
    serializer_class = BorrowingListCreateSerializer
    queryset = Borrowing.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        book = instance.book

        self.perform_destroy(instance)

        book.inventory += 1
        book.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

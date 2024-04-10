from rest_framework.generics import RetrieveAPIView, ListCreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
import asyncio
from drf_spectacular.utils import extend_schema, OpenApiParameter

from telegram_notifications.send_notifications import notification
from borrowings.serializers import (
    BorrowingListCreateSerializer,
    BorrowingDetailSerializer,
)
from borrowings.models import Borrowing
from books_service.models import Book


class BorrowingListCreateView(ListCreateAPIView):
    serializer_class = BorrowingListCreateSerializer
    queryset = Borrowing.objects.all()

    def get_queryset(self):
        queryset = Borrowing.objects.all()
        user_id = self.request.query_params.get("user_id")

        if user_id:
            queryset = queryset.filter(user__id=user_id)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="user_id",
                description="Filter by user",
                required=False,
                type=int,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        """
        Get a list of borrowings.
        """
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        serializer.save(user=user)

        book_id = request.data.get("book")
        book = Book.objects.get(pk=book_id)

        self.perform_create(serializer)

        book.inventory -= 1
        book.save()

        asyncio.run(
            notification(
                f"book '{book.title}' has been borrowed by user: {request.user.email}"
            )
        )

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

        asyncio.run(
            notification(
                f"book '{book.title}' has been returned by user: {request.user.email}"
            )
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

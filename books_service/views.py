from rest_framework import viewsets

from books_service.serializers import BookSerializer
from books_service.models import Book
from books_service.permissions import IsAdminOrReadOnly


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = (IsAdminOrReadOnly,)

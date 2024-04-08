from rest_framework import viewsets

from books_service.serializers import BookSerializer
from books_service.models import Book


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

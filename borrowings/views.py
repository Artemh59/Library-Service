from rest_framework.generics import ListAPIView, RetrieveAPIView

from borrowings.serializers import BorrowingListSerializer, BorrowingDetailSerializer
from borrowings.models import Borrowing


class BorrowingListView(ListAPIView):
    serializer_class = BorrowingListSerializer
    queryset = Borrowing.objects.all()


class BorrowingDetailView(RetrieveAPIView):
    serializer_class = BorrowingDetailSerializer
    queryset = Borrowing.objects.all()

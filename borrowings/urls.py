from django.urls import path

from borrowings.views import BorrowingListCreateView, BorrowingDetailView

urlpatterns = [
    path("borrowings/", BorrowingListCreateView.as_view(), name="borrowings-list"),
    path("borrowings/<int:pk>/", BorrowingDetailView.as_view(), name="borrowings-detail"),
]

app_name = "borrowings"

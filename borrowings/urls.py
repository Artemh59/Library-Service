from django.urls import path

from borrowings.views import BorrowingListView, BorrowingDetailView

urlpatterns = [
    path("borrowings/", BorrowingListView.as_view(), name="borrowings-list"),
    path("borrowings/<int:pk>/", BorrowingDetailView.as_view(), name="borrowings-detail"),
]

app_name = "borrowings"

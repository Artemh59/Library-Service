from django.urls import path

from borrowings.views import (
    BorrowingListCreateView,
    BorrowingDetailView,
    BorrowingDestroyView,
)

urlpatterns = [
    path("borrowings/", BorrowingListCreateView.as_view(), name="borrowings-list"),
    path(
        "borrowings/<int:pk>/", BorrowingDetailView.as_view(), name="borrowings-detail"
    ),
    path(
        "borrowings/<int:pk>/return",
        BorrowingDestroyView.as_view(),
        name="borrowings-return",
    ),
]

app_name = "borrowings"

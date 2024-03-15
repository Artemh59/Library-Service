from books_service.views import BookViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("books", BookViewSet, basename="book")
urlpatterns = router.urls

app_name = "books"

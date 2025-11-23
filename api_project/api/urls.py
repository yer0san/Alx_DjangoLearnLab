from .views import BookList
from .views import BookViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('book/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),
]
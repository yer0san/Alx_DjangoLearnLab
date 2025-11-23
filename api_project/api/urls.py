from .views import BookList
from django.urls import path

urlpatterns = [
    path('book/', BookList.as_view(), name='book-list'),
]
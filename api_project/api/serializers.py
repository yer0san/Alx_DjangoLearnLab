from rest_framework.serializers import ModelSerializer
from .models import Book

class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fiels = '__all__'
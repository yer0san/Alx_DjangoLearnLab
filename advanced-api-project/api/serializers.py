from rest_framework import serializers
from .models import Book, Author
from datetime import datetime

class BookSerializer(serializers.Serializer):
    class Meta:
        model = Book
        fields = '__all__'
    
    def validate_publication_year(self, val):
        cur_year = datetime.now().year
        if val > cur_year:
            raise serializers.ValidationError('Publication year cannot be in the future.')
        return val

class AuthorSerializer(serializers.Serializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fiels = ['name', 'books']
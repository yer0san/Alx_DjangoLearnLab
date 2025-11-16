from django.shortcuts import render
from .models import Book
from django.views.generic import DetailView
from django.views.generic import ListView
from .models import Library

def list_books(request):
    """
    Function-based view to display all books in the database.
    """
    books = Book.objects.all()  # Query all books
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView, ListView):
    """
    Class-based view to display details of a specific library
    including all books available in it.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library' 
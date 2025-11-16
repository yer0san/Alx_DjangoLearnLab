from models import Author, Book, Library, Librarian

# Query all books by a specific author.
author = Author.objects.get(name="your mom")
books_by_author = Book.objects.filter(author=author)

# List all books in a library.
library = Library.objects.get(name="your mom's library")
books_in_library = library.books.all()

# Retrieve the librarian for a library.
librarian = Librarian.objects.get(library__name="your mom's library")
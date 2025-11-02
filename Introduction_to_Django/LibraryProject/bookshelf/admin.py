from django.contrib import admin

from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Columns shown in list view
    list_filter = ('author', 'publication_year')            # Filter sidebar
    search_fields = ('title', 'author')                     # Search box fields

# Register the model with the custom admin class
admin.site.register(Book, BookAdmin)


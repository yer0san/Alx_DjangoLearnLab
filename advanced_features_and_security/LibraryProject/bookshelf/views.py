from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import ExampleForm

@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    form = ExampleForm(request.GET or None)
    books = Book.objects.all()

    if form.is_valid():
        q = form.cleaned_data.get('q')
        if q:
            books = books.filter(title__icontains=q)

    return render(request, "bookshelf/book_list.html", {'books': books, 'form' : form})

@permission_required("bookshelf.can_create", raise_exception=True)
def create_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        Book.objecs.create(title=title, author=author)
        return redirect("book_list")
    return render(request, "bookshelf/create_book.html")

@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.save()
        return redirect("book_list")
    render(request, "bookshelf/edit_book.html", {"book" : book})

@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_book(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")
    return render(request, "bookshelf/delete_book.html", {"book" : book})



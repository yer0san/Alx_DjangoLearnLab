from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Book, Author


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a user and authenticate
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpass')

        # Create authors and books
        self.author = Author.objects.create(name='J.K. Rowling')
        self.book1 = Book.objects.create(title='Harry Potter 1', publication_year=1997, author=self.author)
        self.book2 = Book.objects.create(title='Harry Potter 2', publication_year=1998, author=self.author)

        # URL references
        self.list_url = reverse('book-list')  # ListView
        self.create_url = reverse('book-create')  # CreateView
        self.detail_url = lambda pk: reverse('book-detail', args=[pk])  # Detail, Update, Delete views

    # ------------------- CRUD Tests -------------------

    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        response = self.client.get(self.detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_create_book(self):
        data = {
            'title': 'Harry Potter 3',
            'publication_year': 1999,
            'author': self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.last().title, 'Harry Potter 3')

    def test_update_book(self):
        data = {'title': 'Updated Title'}
        response = self.client.patch(self.detail_url(self.book1.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')

    def test_delete_book(self):
        response = self.client.delete(self.detail_url(self.book2.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # ------------------- Filtering / Searching / Ordering Tests -------------------

    def test_filter_books_by_title(self):
        response = self.client.get(self.list_url, {'title': 'Harry Potter 1'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter 1')

    def test_search_books(self):
        response = self.client.get(self.list_url, {'search': 'Harry Potter 2'})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter 2')

    def test_order_books(self):
        response = self.client.get(self.list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.data[0]['publication_year'], 1998)

    # ------------------- Permission / Authentication Tests -------------------

    def test_create_book_requires_authentication(self):
        self.client.logout()  # unauthenticated
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2025,
            'author': self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_update_book_requires_authentication(self):
        self.client.logout()
        data = {'title': 'Hacked Title'}
        response = self.client.patch(self.detail_url(self.book1.id), data)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_delete_book_requires_authentication(self):
        self.client.logout()
        response = self.client.delete(self.detail_url(self.book1.id))
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

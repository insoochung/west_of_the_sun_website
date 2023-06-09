from django.urls import reverse, resolve
# 'reverse' is used to generate a URL for a given view
# 'resolve' is used to match a requested URL with a list of URLs listed in the urls.py module
from django.test import TestCase
from django.contrib.auth.models import User

from ..views import book_detail, new_book
from ..models import Book

class NewBookTests(TestCase):
    def setUp(self):
        admin = self.user = User.objects.create_user(username='admin', password='12345', is_superuser=True)

        Book.objects.create(title="Test book",
                            meta_prompt="You can help me",
                            initial_prompt="Create a description about a book object that is used for django testing",
                            created_by=admin)

    def test_new_book_view_success_status_code(self):
        url = reverse('new_book')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    
    def test_new_book_url_resolves_new_book_view(self):
        view = resolve('/books/new')
        self.assertEquals(view.func, new_book)


class BookDetailViewTests(TestCase):
    def setUp(self):
        # use setUp to create an instance to use in the tests (needs revision)
        admin = self.user = User.objects.create_user(username='admin', password='12345', is_superuser=True)

        self.book = Book.objects.create(title="Test book",
                                        meta_prompt="You can help me",
                                        initial_prompt="Create a description about a book object that is used for django testing",
                                        created_by=admin)

    # Returns a status code 200 (success) for an existing Book

    def test_book_detail_view_success_status_code(self):
        # Returns a status code 200 (success) for an existing Book
        url = reverse('book_detail', kwargs={'id': self.book.id }) #kwargs meaning key arguments
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    # Returns a status code 404 (page not found) for a Book that does not exist in the DB

    def test_book_detail_view_not_found_status_code(self):
        # Returns a status code 404 (page not found) for a Book that does not exist in the DB
        non_existing_book_id = self.book.id + 1
        url = reverse('book_detail', kwargs={'id':non_existing_book_id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    # Test if Django is using the correct view function to render the Chapters in a Book

    def test_book_detail_url_resolves_book_chapters_view(self):
        # Test if Django is using the correct view function to render the Chapters in a Book
        view = resolve(f'/book_detail/{self.book.id}') # Use f-string to include the book ID
        self.assertEquals(view.func, book_detail)

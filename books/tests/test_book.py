from django.urls import reverse, resolve
# 'reverse' is used to generate a URL for a given view
# 'resolve' is used to match a requested URL with a list of URLs listed in the urls.py module
from django.test import TestCase

from ..views import book_detail
from ..models import Book

class BookDetailTests(TestCase):
    def setUp(self):
        # use setUp to create an instance to use in the tests (needs revision)
        self.book = Book.objects.create(title='Django', description='Django book.')

    # Returns a status code 200 (success) for an existing Book

    def test_book_detail_view_success_status_code(self):
        # Returns a status code 200 (success) for an existing Book
        url = reverse('book_detail', kwargs={'id': self.book.id}) #kwargs meaning key arguments
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

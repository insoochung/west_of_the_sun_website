from django.urls import reverse, resolve
# 'reverse' is used to generate a URL for a given view
# 'resolve' is used to match a requested URL with a list of URLs listed in the urls.py module
from django.test import TestCase
from .views import home, book_chapters, new_chapter
from .models import Book

# Create your tests here.

class HomeTests(TestCase):

    def setUp(self):
        self.book = Book.objects.create(title='Django', description= 'Django Book')
        url = reverse('home')
        self.response = self.client.get(url)
        
    def test_home_view_status_code(self):
        url = reverse('home')   #to generate the URL for the 'home' view
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolves_home_view(self): # for testing that the root URL ("/") leads to the home view.
        view = resolve('/')        
        self.assertEquals(view.func, home)  # for checking if the function associated with the view (view.func) is the home function.
    
    def test_home_view_contains_link_to_book_page(self):
        book_chapters_url = reverse('book_chapters', kwargs={'id' : self.book.id})
        self.assertContains(self.response, 'href="{0}"'.format(book_chapters_url))    #using assertContains to test if the response body contains a given text href="/books/1/"

class BookChaptersTests(TestCase):

# Use setUp to create an instance to use in the tests (needs revision)

    def setUp(self):
        self.book = Book.objects.create(title='Django', description='Django Book')

# Returns a status code 200 (success) for an existing Book

    def test_book_chapters_view_success_status_code(self):
        url = reverse('book_chapters', kwargs={'id': self.book.id}) #kwargs meaning key arguments
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

# Returns a status code 404 (page not found) for a Book that does not exist in the DB

    def test_book_chapters_view_not_found_status_code(self):
        non_existing_book_id = self.book.id + 1
        url = reverse('book_chapters', kwargs={'id':non_existing_book_id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

# Test if Django is using the correct view function to render the Chapters in a Book

    def test_book_chapters_url_resolves_book_chapters_view(self):
        view = resolve(f'/book_chapters/{self.book.id}') # Use f-string to include the book ID
        self.assertEquals(view.func, book_chapters)

# Ensure the navigation back to the homepage

    def test_book_chapters_view_contains_link_back_to_hompage(self):
        book_chapters_url = reverse('book_chapters', kwargs={'id':1})
        response = self.client.get(book_chapters_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))

class NewChapterTests(TestCase):

# Create a Book instance to be used during the tests
    def setUp(self):
        self.book = Book.objects.create(title='Django', description='Django Book')

# Check if the request to the view is successful

    def test_new_chapter_view_success_status_code(self):
        url = reverse('new_chapter', kwargs={'id': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

# Check if the view is raising a 404 error when the book's new chapter does not exist

    def test_new_chapter_view_not_found_status_code(self):
        url = reverse('new_chapter', kwargs={'id': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

# Check if the right view is being used

    def test_new_chapter_url_resolves_new_chapter_view(self):
        view = resolve('/books/1/new/')
        self.assertEquals(view.func, new_chapter)
    
# Ensure the navigation back to the list of a book's chapters

    def test_new_chapter_view_contains_link_back_to_chapter_view(self):
        new_chapter_url = reverse('new_chapter', kwargs={'id': 1})
        chapter_url = reverse('chapter', kwargs={'id': 1})
        response = self.client.get(new_chapter_url)
        self.assertContains(response, 'href="{0}"'.format(chapter_url))

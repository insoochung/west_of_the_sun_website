from django.urls import reverse, resolve
# 'reverse' is used to generate a URL for a given view
# 'resolve' is used to match a requested URL with a list of URLs listed in the urls.py module
from django.test import TestCase

from .views import home, book_detail
from .gpt_calls import call_gpt
from .models import Book
# Create your tests here.

RUN_GPT_TESTS = False  # Set to True if you want to run GPT tests


class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')   #to generate the URL for the 'home' view
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolves_home_view(self): # for testing that the root URL ("/") leads to the home view.
        view = resolve('/')        
        self.assertEquals(view.func, home)  # for checking if the function associated with the view (view.func) is the home function.

        
class GptTests(TestCase):
    def test_gpt_call(self):
        if not RUN_GPT_TESTS:
            return
        system_prompt = "You are a helpful assistant."
        conv_init_role = "user"
        dialog = ["Who won the world series in 2020?",
                  "The Los Angeles Dodgers won the World Series in 2020.",
                  "Where was it played?"]
        model = "gpt-3.5-turbo"
        ret = call_gpt(system_prompt, conv_init_role, dialog, model)
        # e.g. ret["model"] can be "gpt-3.5-turbo-0301"
        self.assertTrue(ret["model"].startswith(model))
        # e.g. message can be "The 2020 World Series was played at Globe Life Field in Arlington, Texas."
        self.assertTrue("Arlington" in ret["choices"][0]["message"]["content"])


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

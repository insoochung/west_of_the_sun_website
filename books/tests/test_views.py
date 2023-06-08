from django.urls import reverse, resolve
# 'reverse' is used to generate a URL for a given view
# 'resolve' is used to match a requested URL with a list of URLs listed in the urls.py module
from django.test import TestCase

from ..views import home

# Create your tests here.

class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')   #to generate the URL for the 'home' view
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolves_home_view(self): # for testing that the root URL ("/") leads to the home view.
        view = resolve('/')        
        self.assertEquals(view.func, home)  # for checking if the function associated with the view (view.func) is the home function.

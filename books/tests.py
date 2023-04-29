from django.urls import reverse, resolve
from django.test import TestCase
from .views import home
from .gpt_calls import call_gpt
# Create your tests here.

RUN_GPT_TESTS = False  # Set to True if you want to run GPT tests


class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)


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

from django.urls import reverse, reverse_lazy
from django.test import TestCase
from django.http import HttpResponseNotAllowed

from .views import generate_lights_data
from .models import Article


class TestCalls(TestCase):
    def setUp(self):
        self.create_url = 'create'
        self.list_view = 'main'

    def test_generating_data(self):
        ligths_test_value = 400

        response = generate_lights_data(
            f'2019-11-13T12:55:53.612598 {ligths_test_value}')

        expected_response = {
            'lights': [1, 1, 1, 1, 0, 0, 0, 0],
            'lightning_value': ligths_test_value
        }

        self.assertDictEqual(response, expected_response)

    def test_call_view_loads(self):
        for url in [self.create_url, self.list_view]:
            path = str(reverse_lazy(url))
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, f"blog/{url}.html")

    def test_call_view_fails_blank(self):
        path = str(reverse_lazy(self.create_url))
        response = self.client.post(path, {})

        self.assertFormError(
            response,
            'form',
            'title',
            ['This field is required.']
        )

    def test_call_view_fails_incorrect(self):
        path = str(reverse(self.create_url))
        value = '1' * 65
        data = {
            'title': value,
            'description': 'test description'
        }
        response = self.client.post(path, data, follow=True)
        self.assertFormError(
            response,
            'form',
            'title',
            ['Ensure this value has at most 64 characters (it has 65).']
        )

    def test_call_view_succeed(self):
        path = str(reverse_lazy(self.create_url))

        value = '1'*10
        description = 'test description'
        article_data = {
            'title': value,
            'description': description
        }
        response = self.client.post(path, article_data)

        self.assertEqual(response.status_code, 302)
        article = Article.objects.get(id=1)
        for field in article_data.keys():
            article_field = getattr(article, field)
            self.assertEqual(article_field, article_data[field])

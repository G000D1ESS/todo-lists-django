from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page


class HomePageTest(TestCase):
    '''Тест домашней страницы'''

    def test_root_url_resolves_to_home_page_view(self):
        '''Тест: Кореновой URL преобразуется в представление домашней страницы'''
        found = resolve('/').func
        self.assertEqual(found, home_page)

    def test_home_page_returns_correct_html(self):
        '''Тест: Домашняя страница возвращает правильный HTML'''
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf-8')
        self.assertTrue(html.lower().startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.lower().endswith('</html>'))


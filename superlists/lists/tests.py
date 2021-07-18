from django.urls import resolve
from django.test import TestCase

from lists.views import home_page


class HomePageTest(TestCase):
    '''Тест домашней страницы'''

    def test_root_url_resolves_to_home_page_view(self):
        '''Тест: Кореновой URL преобразуется в представление домашней страницы'''
        found = resolve('/').func
        self.assertEqual(found, home_page)


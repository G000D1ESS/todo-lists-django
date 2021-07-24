from django.urls import resolve
from django.test import TestCase
from django.template.loader import render_to_string
from django.http import HttpRequest

from lists.models import Item
from lists.views import home_page


class HomePageTest(TestCase):
    '''Тест домашней страницы'''

    def test_home_page_returns_correct_html(self):
        '''Тест: Домашняя страница возвращает правильный HTML'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ItemModelTest(TestCase):
    '''Тест модели элемента списка'''

    def test_saving_and_retrieving_items(self):
        '''Тест сохранения и получения элементов списков'''
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')


class ListViewTest(TestCase):
    '''Тест представления списка'''
    
    def test_uses_list_template(self):
        '''Тест: Используется шаблон списка'''
        response = self.client.get('/lists/unique-list/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        '''Тест: Отображются все элементы списка'''
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/unique-list/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

class NewListTest(TestCase):
    '''Тест нового списка'''

    def test_can_save_a_POST_request(self):
        '''Тест: можно сохрнаить POST-запрос'''
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        '''Тест: переадресация полсле POST-запроса'''
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/unique-list/')


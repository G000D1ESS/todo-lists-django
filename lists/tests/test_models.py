from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List


class ItemModelTest(TestCase):
    '''Тест модели элемента'''

    def test_default_text(self):
        '''Тест заданного по умолчанию текста'''
        item = Item()
        self.assertEqual(item.text, '')


class ListModelTest(TestCase):
    '''Тест модели списка'''

    def test_item_is_related_to_list(self):
        '''Тест: элемент связан со списком'''
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save__empty_list__items(self):
        '''Тест: нельзя добавлять пустые элементы списка'''
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        '''Тест: получен абсолютный URL'''
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')
    
    def test_duplicate_items_are_invalid(self):
        '''Тест: повторы элементов не допустимы'''
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='Bla')
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='Bla')
            item.full_clean()
    
    def test_can_save_same_item_to_different_lists(self):
        '''Тест: можно сохрнаить тот же элмент в разные списки'''
        first_list = List.objects.create()
        second_list = List.objects.create()
        Item.objects.create(list=first_list, text='Bla')
        same_item = Item(list=second_list, text='Bla')
        same_item.full_clean()

    def test_string_representation(self):
        '''Тест строкового представления'''
        item = Item(text='Some text')
        self.assertEqual(str(item), 'Some text')

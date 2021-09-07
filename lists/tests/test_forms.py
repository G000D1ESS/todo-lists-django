from django.test import TestCase

from lists.models import Item, List
from lists.forms import (
    DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR,
    ExistingListItemForm, ItemForm
)


class ExistingListItemFormTest(TestCase):
    '''Тест формы для элемента существующего списка'''

    def test_form_renders_item_text_input(self):
        '''Тест: форма отображает текстовое поле ввода'''
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())
    
    def test_form_validation_for_blank_items(self):
        '''Тест валидации формы для пустых элементов'''
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        '''Тест: валидация формы для повторных элементов'''
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='No twins!')
        form = ExistingListItemForm(for_list=list_, data={'text': 'No twins!'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

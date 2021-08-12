from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    '''Тест валидации элемента списка'''

    def test_cannot_add_empty_list_items(self):
        '''Тест: нельзя добавлять пустые элементы списка'''
        # Семён открывает домашнюю страницу и случайно пытается отправить 
        # пустой элемент списка. Она нажимает Enter на пустом поле ввода
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Домашняя страница обновляется и появляется сообщение об ошибке
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))

        # Он пробует снова, но теперь уже с текстом
        self.get_item_input_box().send_keys('Купить молоко')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        # Как ни странно, он решает отправить второй пустой элемент списка
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Домашняя страница обновляется и снова появляется сообщение об ошибке
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))

        # И он может его исправить, заполнив его текстом
        self.get_item_input_box().send_keys('Сделать чай')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')
        self.wait_for_row_in_list_table('2: Сделать чай')

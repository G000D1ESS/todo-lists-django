from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    '''Тест валидации элемента списка'''

    def get_error_element(self):
        '''Получить элемент с ошибкой'''
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        '''Тест: нельзя добавлять пустые элементы списка'''
        # Семён открывает домашнюю страницу и случайно пытается отправить 
        # пустой элемент списка. Она нажимает Enter на пустом поле ввода
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Бразуер перехватывает запрос и не загружает страницу со списком
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'    
        ))
        
        # Он пробует снова, но теперь уже с текстом
        self.add_list_item('Купить молоко')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'    
        ))

        # Как ни странно, он решает отправить второй пустой элемент списка
        self.get_item_input_box().send_keys(Keys.ENTER)

        # И снова браузер не подчиняется 
        self.wait_for_row_in_list_table('1: Купить молоко')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'    
        ))

        # И он может его исправить, заполнив его текстом
        self.get_item_input_box().send_keys('Сделать чай')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'    
        ))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')
        self.wait_for_row_in_list_table('2: Сделать чай')

    def test_cannot_add_duplicate_items(self):
        '''Тест: нельзя добавлять повторяющиеся элементы'''
        # Семён открывает домашнюю страницу и начинает новый список
        self.browser.get(self.live_server_url)
        self.add_list_item('Купить сливочное масло')

        # Он случайно пытается ввести повторяющийся элемент
        self.get_item_input_box().send_keys('Купить сливочное масло')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Он видит сообщение об ошибке
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            'You\'ve already got this in your list'
        ))

    def test_error_messages_are_cleared_on_input(self):
        '''Тест: сообщение об ошибке очищается при вводе'''
        # Семён начинает список и вызывает ошибку валидации
        self.browser.get(self.live_server_url)
        self.add_list_item('Посмотреть и купить рыбов')
        self.get_item_input_box().send_keys('Посмотреть и купить рыбов')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        # Он начинает набирать в поле ввода, чтобы очистить ошибку
        self.get_item_input_box().send_keys('x')

        # Сообщение об ошибке исчезает
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))

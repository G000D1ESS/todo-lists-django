from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    ''' Тест от лица нового посетителя '''

    def test_can_stat_a_list_for_one_user(self):
        '''Тест: можно создать список и получить его позже'''

        # Семён слышал про крутое онлайн-приложение со списком
        # неотложных дел. Он решает оценить его домашнюю страницу
        self.browser.get(self.live_server_url)

        # Он видит, что заголовок и шапка страницы говорят о списках
        # неотложныхх дел
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Ему сразу же предлагают ввести элемент из списка
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Он набирает в текстовом поле - "Купить книгу по программированию"
        inputbox.send_keys('Купить книгу по программированию')

        # Когда он нажмёт Enter, страница обновляется, и теперь страница
        # Содержит "1: Купить книгу по программированию" в качестве элемента списка
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить книгу по программированию')

        # Теперь он набирает в текстовом поле - "Купить видеокарту"
        # Когда он нажмёт Enter, страница обновляется, и теперь страница
        # Содержит "2: Купить видеокарту
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Купить видеокарту') 
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Купить видеокарту')
        self.wait_for_row_in_list_table('2: Купить книгу по программированию')

        # Семён завершает работу и ложиться спать
    
    def test_multiple_users_can_start_lists_at_different_urls(self):
        '''Тест: многочисленные польователи могут начать списки по разным URL'''
        # Семён начинает новый список
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Купить книгу по программированию')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить книгу по программированию')

        # Он замечает, что его список имеет уникальный URL-адрес
        semen_list_url = self.browser.current_url
        self.assertRegex(semen_list_url, '/lists/.+')

        # Теперь новый пользователь, Артём, заходит на сайт
        self.browser.quit()
        self.browser = webdriver.Chrome()
        
        # Артём посещает домашнюю страницу. Нет никаких признаков списка Семёна
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить книгу по программированию', page_text)

        # Артём начинает новый список, вводя новый элемент
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Купить молоко')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        # Артём получает уникальый URL-адрес
        artem_list_url = self.browser.current_url
        self.assertRegex(artem_list_url, '/lists/.+')
        self.assertNotEqual(artem_list_url, semen_list_url)

        # Опять-таки, нет следа от списка Семёна
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Купить книгу по программированию', page_text)
        self.assertIn('Купить молоко', page_text)

        # Семён и Артём заканчивают свою работу со списком

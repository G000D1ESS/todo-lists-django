import time
import unittest

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):
    ''' Тест от лица нового посетителя '''

    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        '''Подтвеждение строки в таблице списка'''
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_stat_a_list_and_retrieve_it_later(self):
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
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Он набирает в текстовом поле - "Купить книгу по программированию"
        inputbox.send_keys('Купить книгу по программированию')

        # Когда он нажмёт Enter, страница обновляется, и теперь страница
        # Содержит "1: Купить книгу по программированию" в качестве элемента списка
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Теперь он набирает в текстовом поле - "Купить видеокарту"
        # Когда он нажмёт Enter, страница обновляется, и теперь страница
        # Содержит "2: Купить видеокарту
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Купить видеокарту') 
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table('1: Купить книгу по программированию')
        self.check_for_row_in_list_table('2: Купить видеокарту')

        # Текстовое поле по-прежнему приглашает добавить ещё один элемент.
        # Он вводит "Написать первую программу"
        self.fail('Закончить тест!')


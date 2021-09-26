import time
import os
from functools import wraps

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


def wait(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return func(*args, **kwargs)
            except (AssertionError, WebDriverException) as error:
                if time.time() - start_time > MAX_WAIT:
                    raise error
                time.sleep(0.5)
    return wrapper


class FunctionalTest(StaticLiveServerTestCase):
    '''Функциональный тест'''

    def setUp(self):
        self.browser = webdriver.Chrome()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    @wait
    def wait_for(self, func):
        '''Ожидание'''
        return func()

    @wait
    def wait_for_row_in_list_table(self, row_text):
        '''Ожидание строки в таблице списка'''
        start_time = time.time()
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
    
    @wait
    def wait_to_be_logged_in(self, email):
        '''Ожидать входа в систему'''
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Log out')
        )
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)
    
    @wait
    def wait_to_be_logged_out(self, email):
        '''Ожидать выхода из системы'''
        self.wait_for(
            lambda: self.browser.find_element_by_name('email')
        )
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)

    def get_item_input_box(self):
        '''Получить поле ввода для элемента'''
        return self.browser.find_element_by_id('id_text')

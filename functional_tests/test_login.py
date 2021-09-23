import re
import os

from django.core import mail
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


TEST_EMAIL = 'test@example.com'
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # Семён заходит на сайт и вводит свою почту, чтобы войти
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # Появляется сообщение от том, что ему на почту было выслано письмо
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))

        # Семён проверяет почту и находит сообщение
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # Оно содержит ссылку на Url-адрес
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'https?://.+', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        url = url_search[0]
        self.assertIn(self.live_server_url, url)

        # Семён переходит по ссылке
        self.browser.get(url)

        # Теперь он зарегистрирован в системе
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Log out')
        )
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, navbar.text)

        # Теперь он решает выйти из системы
        self.browser.find_element_by_link_text('Log out').click()

        # Он вышел из системы
        self.wait_for(
            lambda: self.browser.find_element_by_name('email')
        )
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(TEST_EMAIL, navbar.text)

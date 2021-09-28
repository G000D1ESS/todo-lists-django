from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore

from functional_tests.base import FunctionalTest


User = get_user_model()


class MyListsTest(FunctionalTest):
    
    def create_pre_authenticated_session(self, email):
        '''Предвадительно создать аутентифицированный сеанс'''
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        
        # Установить Cookie, которые нужны для первого посещения домена
        self.browser.get(self.live_server_url)
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        '''
        Тест: списки зарегистрированных пользователей 
        сохраняются как "Мои списки"
        '''
        email = 'test@example.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # Артём является зарегистрированным пользователем
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)

        # Он открывает домашнюю страницу и начинает новый список
        self.browser.get(self.live_server_url)
        self.add_list_item('Купить машину')
        self.add_list_item('Проверить почту')
        first_list_url = self.browser.current_url

        # Он замечает сслыку на "Мои списки"
        self.browser.find_element_by_link_text('My lists').click()

        # Он видит, что его список находиться там и он
        # назван на основе первого эдлемента
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Купить машину')
        )
        self.browser.find_element_by_link_text('Купить машину').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # Он решает начать ещё один список
        self.browser.get(self.live_server_url)
        self.add_list_item('Помыть гараж')
        second_list_url = self.browser.current_url

        # Под заголовком "Мои списки" появляется новый список
        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Помыть гараж')
        )
        self.browser.find_element_by_link_text('Помыть гараж').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # Он выходит из системы и списки исчезают
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text('My lists'),
            []
        ))

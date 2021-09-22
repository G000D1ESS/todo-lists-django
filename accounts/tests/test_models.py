from django.test import TestCase
from django.contrib import auth

from accounts.models import Token


User = auth.get_user_model()


class UserModelTest(TestCase):
    
    def test_user_is_valid_with_email_only(self):
        '''Тест: пользователь допустим только с электронной почтой'''
        user = User(email='test@example.com')
        user.full_clean()

    def test_email_is_primary_key(self):
        '''Тест: адрес электронной почты является первичным ключом'''
        user = User(email='test@example.com')
        self.assertEqual(user.pk, 'test@example.com')

    def test_no_problem_with_auth_login(self):
        '''Тест: проблем с авторизацией нет'''
        user = User.objects.create(email='test@example.com')
        user.backend = ''
        request = self.client.request().wsgi_request
        auth.login(request, user)


class TokenModelTest(TestCase):

    def test_links_user_with_auto_generated_uid(self):
        '''Тест: соединяет пользователя с автогенерированным uid'''
        first_token = Token.objects.create(email='test@example.com')
        second_token = Token.objects.create(email='test@example.com')
        self.assertNotEqual(first_token.uid, second_token.uid)

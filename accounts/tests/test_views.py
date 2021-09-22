import os
from unittest.mock import patch, call

from django.test import TestCase

from accounts.models import Token


class SendLoginEmailView(TestCase):

    def test_redirects_to_home_page(self):
        '''Тест: переадресация на домашнюю страницу'''
        response = self.client.post(
            '/accounts/send_login_email',
            data={'email': 'test@example.com'}
        )
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        '''Тест: отправляется сообщение на адрес из метода POST'''
        self.client.post(
            '/accounts/send_login_email',
            data={'email': 'test@example.com'}
        )

        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, os.environ.get('EMAIL_LOGIN'))
        self.assertEqual(to_list, ['test@example.com'])
    
    def test_adds_success_message(self):
        '''Тест: добавляется сообщение об успехе'''
        response = self.client.post(
            '/accounts/send_login_email',
            data={'email': 'test@example.com'},
            follow=True
        )

        message = list(response.context['messages'])[0]
        self.assertEqual(message.tags, 'success')
        self.assertEqual(
            message.message,
            "Check your email, you'll find a message with a link that will log you into the site."
        )

    def test_creates_token_associated_with_email(self):
        '''Тест: создаётся маркер, связанный с почтой'''
        self.client.post(
            '/accounts/send_login_email',
            data={'email': 'test@example.com'}
        )
        token = Token.objects.first()
        self.assertEqual(token.email, 'test@example.com')


@patch('accounts.views.auth')
class LoginViewTest(TestCase):

    def test_redirects_to_home_page(self, mock_auth):
        '''Тест: переадресация на домашнюю страницу'''
        response = self.client.get('/accounts/login?token=test-token')
        self.assertRedirects(response, '/')

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        '''Тест: вызывается authenticate с uid из GET-запроса'''
        self.client.get('/accounts/login?token=test-token')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid='test-token')
        )

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        '''Тест: вызывается auth_login с пользователем, если такой имеется''' 
        response = self.client.get('/accounts/login?token=test-token')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        '''Тест: не регистрируется в системе, если пользователь не аутентифицирован'''
        mock_auth.authenticate.return_value = None
        self.client.get('/accounts/login?token=test-token')
        self.assertEqual(mock_auth.login.called, False)

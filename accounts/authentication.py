from django.contrib.auth.backends import BaseBackend

from accounts.models import User, Token


class PasswordlessAuthenticationBackend(BaseBackend):
    
    def authenticate(self, request, uid=None):
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return

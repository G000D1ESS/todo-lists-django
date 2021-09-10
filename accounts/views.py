import uuid
import sys

from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate

from accounts.models import Token


def login(request):
    print('login view', file=sys.stderr)
    uid = request.GET.get('uid')
    user = authenticate(uid=uid)
    if user is not None:
        auth_login(request, user)
    return redirect('/')


def logout(request):
    auth_logout(request)
    return redirect('/')


def send_login_email(request):
    '''Выслать ссылку на логин по почте'''
    email = request.POST['email']
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    print('Saving UID', uid, 'for email', email, file=sys.stderr)
    url = request.build_absolute_uri(f'/accounts/login?uid={uid}')
    send_mail(
        'Your login link for Superlists',
        f'Use this link to log in:\n\n{url}',
        'noreply@supelists',
        [email]
    )
    return render(request, 'login_email_sent.html')

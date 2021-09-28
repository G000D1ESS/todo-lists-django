import os

from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages, auth
from django.core.mail import send_mail

from accounts.models import Token


def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid)
    )
    message_body = f'Use this link to log in:\n\n{url}'
    send_mail(
        'Your login link for Superlists',
        message_body,
        os.environ.get('EMAIL_LOGIN'),
        [email]
    )
    messages.success(
        request,
        "Check your email, you'll find a message with a link that will log you into the site."
    )
    return redirect('/')


def login(request):
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')

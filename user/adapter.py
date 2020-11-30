from allauth.account.adapter import DefaultAccountAdapter

# email import module
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMessage

from .tokens import account_activation_token


class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.alias = data.get('alias')

        # email confirmation
        current_site = get_current_site(request)
        mail_subject = 'Activate your account'
        user.save()
        mail_content = {
            'email': user.email,
            'domain': 'raccat-logbook.herokuapp.com',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        }
        print(mail_content)
        mail_message = render_to_string(
            'acc_active_email.html', mail_content
        )
        # mail_message = 'Please confirm your email.'
        activation_email = EmailMessage(
            mail_subject,
            mail_message,
            from_email='admin@ifyouarehappyandyouknowitsay.com',
            to=[user.email]
        )  
        activation_email.send()   

        return user

import math

from django.core.mail import EmailMessage
from rest_email_auth.admin import models


def check_email(mail):
    emails = models.EmailAddress.objects.all()
    check = models.EmailAddress.objects.filter(email=mail)
    for email in emails:
        if check and email.is_verified:
            return True
        else:
            return False




#
#
# class EmailThread(threading.Thread):
#
#     def __init__(self, email):
#         self.email = email
#         threading.Thread.__init__(self)
#
#     def run(self):
#         self.email.send()
#
#
# def send_email(data):
#     email = EmailMessage(
#         subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
#     EmailThread(email).run()
#
#
# def send_email_verification(user):
#     token = RefreshToken.for_user(user).access_token
#     absurl = f'http://127.0.0.1:8000/user/email-verify/' + "?token=" + str(token)
#     email_body = 'Hi! ' + \
#                  'Use the link below to verify your email \n' + absurl
#     data = {'email_body': email_body, 'to_email': user.email,
#             'email_subject': 'Verify your email'}
#
#     send_email(data)
#
#
# def send_change_password(user):
#     token = RefreshToken.for_user(user).access_token
#     absurl = f'http://127.0.0.1:8000/user/change-password' + "?token=" + str(token)
#     email_body = 'Hi! ' + \
#                  'Use the link below to change your password \n' + absurl
#     data = {'email_body': email_body, 'to_email': user.email,
#             'email_subject': 'Change password'}
#
#     send_email(data)
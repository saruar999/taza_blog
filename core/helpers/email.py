from django.core.mail import send_mail


def custom_send_mail(message,
                     subject,
                     fail_silently=True,
                     recipient_list=[],
                     sender='saruar.star1999@gmail.com'):

    _default_message = 'This is a test email'
    _default_subject = 'Test email'

    _message = message if message is not None else _default_message
    _subject = subject if subject is not None else _default_subject

    send_mail(subject=_subject,
              message=_message,
              from_email=sender,
              fail_silently=fail_silently,
              recipient_list=recipient_list)

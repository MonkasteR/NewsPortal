from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPortal.settings import DEFAULT_FROM_EMAIL, SITE_URL


@shared_task
# def send_notifications(sender, instance=None, **kwargs):
#     if instance is not None:
#         subject = f"Новая новость: {instance.title}"
#         message = get_template('email/news_notification_email.html').render({'news': instance, 'SITE_URL': SITE_URL})
#         from_email = DEFAULT_FROM_EMAIL
#         subscribers = Subscriber.objects.all()
#         # post_id = instance.pk
#         for subscriber in subscribers:
#             to_email = subscriber.user.email
#             send_mail(subject, message, from_email, [to_email])

@shared_task
def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'email/post_created_email.html',
        {
            'text': preview,
            'link': f'{SITE_URL}/news/{pk}',
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.encoding = 'utf-8'
    msg.send()

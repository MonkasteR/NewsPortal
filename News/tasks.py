from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from News.models import Post
from NewsPortal.settings import DEFAULT_FROM_EMAIL, SITE_URL


@shared_task
def send_notifications(pk, to_email):
    preview = Post.objects.get(pk=pk).preview
    title = Post.objects.get(pk=pk).title
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
        to=to_email,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.encoding = 'utf-8'
    msg.send()

# from datetime import datetime
import datetime

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from News.models import Post, Category
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


@shared_task
def my_task():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'email/daily_post.html',
        {
            'link': SITE_URL,
            'posts': posts,
        }

    )
    msg = EmailMultiAlternatives(
        subject=f'Новые посты за неделю',
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers,

    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

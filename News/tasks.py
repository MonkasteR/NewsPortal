from celery import shared_task
from django.core.mail import send_mail

from NewsPortal.settings import DEFAULT_FROM_EMAIL
from .models import Post


@shared_task
def send_notifications(post_id):
    post = Post.objects.get(id=post_id)
    subscribers = Post.category.subscribers.all()
    for subscriber in subscribers:
        email = subscriber.email
        subject = 'Новая статья!'
        message = f'У нас есть новая статья: {post.title}. Проверьте ее на сайте.'
        send_mail(subject, message, DEFAULT_FROM_EMAIL, [email])

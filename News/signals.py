from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import get_template
from django.urls import reverse

from News.models import Subscriber, Post
from NewsPortal.settings import DEFAULT_FROM_EMAIL


@login_required
@receiver(post_save, sender=Post)
def send_news_notification(sender, instance=None, **kwargs):
    if instance is not None:
        subject = "Новая новость: " + instance.title
        message = get_template('news_notification_email.html').render({'news': instance})
        context = {'news': {'title': {instance.title},
                            'content': {instance.text}}}  # TODO: заголовок передается, а тело письма нет
        from_email = DEFAULT_FROM_EMAIL
        subscribers = Subscriber.objects.all()
        for subscriber in subscribers:
            to_email = subscriber.user.email
            link = reverse('one_news', args=[instance.pk])
            message += f"\nЧтобы прочитать новость, перейдите по ссылке: {link}\n"  # TODO: зацикливается подпись
            send_mail(subject, message, from_email, [to_email])

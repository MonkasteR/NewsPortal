from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import get_template, render_to_string
from django.urls import reverse

from News.models import Subscriber, Post
from NewsPortal.settings import DEFAULT_FROM_EMAIL, SITE_URL


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


# @receiver(post_save, sender=Post)
# def send_news_notification(sender, instance=None, **kwargs):
#     print(f'{instance.title = }')
#     print(f'{instance.text = }')
#     print(f'{instance.pk = }')
#     print(f'{instance.author = }')
#     print(f'{instance.postCategory = }')
#     print(f'{instance.dateCreation = }')
#     print(f'{instance.rating = }')
#     print(f'{instance.categoryType = }')
def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
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
    msg.send()


@receiver(m2m_changed, sender=Post.postCategory)
def notify_about_new_post(sender, instance=None, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()
        subscribers = [s.email for s in subscribers]
        send_notifications(instance.preview(), instance.pk, instance.title, subscribers)

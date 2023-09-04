from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from News.models import Post, Subscriber
from News.tasks import send_notifications


@login_required
@receiver(post_save, sender=Post)
def send_news_notification(sender, instance, **kwargs):
    if kwargs['created']:
        preview = instance.preview
        instance_id = instance.pk
        # title = instance.title
        subscribers = Subscriber.objects.all()
        to_email = [subscriber.user.email for subscriber in subscribers]
        # print(to_email)
        # print(preview)
        # print(instance_id)
        # print(title)
        send_notifications.delay(instance_id, to_email)
        # for subscriber in subscribers:
        #     to_email = subscriber.user.email
        #     send_notifications.delay(preview, instance_id, title, [to_email])


@receiver(m2m_changed, sender=Post.postCategory)
def notify_about_new_post(sender, instance=None, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers = [s.email for category in categories for s in category.subscribers.all()]
        send_notifications(instance.preview(), instance.pk, instance.title, subscribers)

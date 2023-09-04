from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from News.models import Post
from News.tasks import send_notifications


@login_required
@receiver(post_save, sender=Post)
def send_news_notification(sender, instance=None, **kwargs):
    send_notifications.delay(sender, instance=None, **kwargs)
    # if instance is not None:
    # subject = f"Новая новость: {instance.title}"
    # message = get_template('email/news_notification_email.html').render({'news': instance, 'SITE_URL': SITE_URL})
    # from_email = DEFAULT_FROM_EMAIL
    # subscribers = Subscriber.objects.all()
    # post_id = instance.pk
    # for subscriber in subscribers:
    #     to_email = subscriber.user.email
    #     # send_mail(subject, message, from_email, [to_email])
    #     send_notifications.delay(post_id, subject, message, from_email, [to_email])




@receiver(m2m_changed, sender=Post.postCategory)
def notify_about_new_post(sender, instance=None, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers = [s.email for category in categories for s in category.subscribers.all()]
        send_notifications(instance.preview(), instance.pk, instance.title, subscribers)

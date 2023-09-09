from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from News.models import Post, Subscriber
from News.tasks import send_notifications


@login_required
@receiver(post_save, sender=Post)
def send_news_notification(sender, instance, **kwargs):
    """
    Эта функция является приемником сигнала, который срабатывает после сохранения объекта Post.
    Она отправляет уведомление всем подписчикам с превью поста.

    Параметры:
        - sender: Класс модели, который отправил сигнал.
        - instance: Фактический экземпляр, который сохраняется.
        - **kwargs: Дополнительные именованные аргументы.

    Возвращает:
        None
    """
    if kwargs['created']:
        instance_id = instance.pk
        subscribers = Subscriber.objects.all()
        to_email = [subscriber.user.email for subscriber in subscribers]
        send_notifications.delay(instance_id, to_email)


@receiver(m2m_changed, sender=Post.postCategory)
def notify_about_new_post(sender, instance=None, **kwargs):
    """
    Уведомляет подписчиков о новом посте в категории.

    Аргументы:
        sender (Any): Объект-отправитель.
        instance (Any, опционально): Объект-экземпляр. По умолчанию None.
        **kwargs (Any): Дополнительные именованные аргументы.

    Возвращает:
        None
    """
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers = [s.email for category in categories for s in category.subscribers.all()]
        send_notifications(instance.preview(), instance.pk, instance.title, subscribers)

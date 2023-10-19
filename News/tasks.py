# from datetime import datetime
import datetime

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from News.models import Post, Category
from News.views import logger
from NewsPortal.settings import DEFAULT_FROM_EMAIL, SITE_URL


@shared_task
def send_notifications(pk, to_email):
    """
    Отправляет уведомления на указанный адрес электронной почты.

    Аргументы:
        pk (int): Первичный ключ поста, для которого отправляются уведомления.
        to_email (str): Адрес электронной почты, на который отправляются уведомления.

    Возвращает:
        None
    """
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
    logger.info('Task: send_notifications')


@shared_task
def my_task():
    """
    Задача, которая отправляет подписчикам электронное письмо с последними постами за прошедшую неделю.

    Эта задача получает текущую дату и вычисляет дату неделю назад.
    Затем фильтрует объекты `Post` на основе поля `dateCreation`, выбирая только те посты,
    которые были созданы за последнюю неделю.
    Уникальные категории этих постов извлекаются и хранятся в множестве `categories`.
    Подписчики получаются путем фильтрации объектов `Category` на основе имен из `categories`
    и извлечения связанных с ними адресов электронной почты.

    HTML-содержимое для электронного письма генерируется с использованием функции `render_to_string`,
    которая отображает шаблон 'email/daily_post.html' с предоставленными контекстными данными,
    включая SITE_URL и набор `posts`.

    Создается экземпляр `EmailMultiAlternatives` с указанием темы 'Новые посты за неделю',
    тело оставляется пустым, `from_email` устанавливается на значение `DEFAULT_FROM_EMAIL`,
    а получатели устанавливаются на множество `subscribers`.

    HTML-содержимое прикрепляется к электронному письму с помощью метода `attach_alternative`,
    указывая тип контента как 'text/html'. Наконец, письмо отправляется с помощью метода `send`
    экземпляра `EmailMultiAlternatives`.
    """
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
        subject='Новые посты за неделю',
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers,

    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    logger.info('Task: my_task')

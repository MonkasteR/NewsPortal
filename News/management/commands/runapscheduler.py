import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from News.models import Post, Category
from NewsPortal.settings import logger


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        """
        Запускает планировщик для выполнения заданий в определенные моменты времени.

        Параметры:
        - args: Позиционные аргументы, переданные в функцию.
        - options: Именованные аргументы, переданные в функцию.

        Возвращает:
        None
        """
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="fri", hour="18", minute="00", second="30"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")


def my_job():
    """
    Отправляет еженедельное письмо подписчикам со списком последних постов.

    Эта функция извлекает посты, созданные за последнюю неделю, и фильтрует их по категориям.
    Затем она извлекает подписчиков, заинтересованных в этих категориях, и отправляет им электронное письмо
    с перечислением последних постов.

    Параметры:
    Нет

    Возвращает:
    Нет
    """
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'email/daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }

    )
    msg = EmailMultiAlternatives(
        subject='Новые посты за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,

    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    logger.info('Task: send_emails')


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    Удаляет старые выполнения заданий.

    param max_age: Максимальный возраст выполнений заданий для удаления, в секундах.
    По умолчанию 604_800 (7 дней).
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
    logger.info('Deleted old job executions')

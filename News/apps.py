from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'News'

    def ready(self):
        """
        Инициализирует объект и импортирует необходимые сигналы для модуля News.
        """
        # noinspection PyUnresolvedReferences

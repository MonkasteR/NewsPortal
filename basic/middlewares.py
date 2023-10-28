import pytz

from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        """
        Инициализирует класс с параметром get_response.

        :param get_response: Функция, которая будет использоваться в качестве обработчика ответа.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Устанавливает часовой пояс для запроса на основе значения 'django_timezone' в сессии.
        Если значение 'django_timezone' существует в сессии, активирует соответствующий часовой пояс.
        Если значение 'django_timezone' не существует в сессии, деактивирует часовой пояс.

        Аргументы:
            request: Объект запроса.

        Возвращает:
            Ответ, возвращаемый методом 'get_response'.
        """
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """
    Заменяет или добавляет параметры строки запроса в URL.

    Аргументы:
        context (dict): Словарь контекста, содержащий объект 'request'.
        **kwargs: Именованные аргументы, представляющие параметры строки запроса и их значения.

    Возвращает:
        str: URL с обновленными параметрами строки запроса.

    Исключения:
        KeyError: Если объект 'request' не найден в словаре контекста.

    Примеры:
        >>> url_replace({'request': MockRequest(GET={'page': 1})}, page=2)
        '/?page=2'

    Примечание:
        Эта функция предполагает, что объект 'request' присутствует в словаре контекста.

        Эта функция использует метод `urlencode` из класса `QueryDict` для кодирования параметров строки запроса.
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()

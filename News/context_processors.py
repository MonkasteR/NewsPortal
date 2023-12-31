from .models import Post


def news_for_header(request):
    """
    Получает последние новости для отображения в заголовке веб-сайта.

    Параметры:
        request (HttpRequest): Объект HTTP-запроса.

    Возвращает:
        dict: Словарь, содержащий последнюю новость для заголовка.
            Словарь имеет следующую пару ключ-значение:
            - 'news_for_header': Запрос к базе данных, отсортированный по дате создания.
    """
    return {"news_for_header": Post.objects.order_by("-dateCreation")}


def news_pk(request):
    """
    Получает новость с заданным первичным ключом.

    Параметры:
        request (int): Первичный ключ новости.

    Возвращает:
        dict: Словарь, содержащий новость с заданным первичным ключом.
    """
    return {"news_pk": Post.objects.get(pk=request)}

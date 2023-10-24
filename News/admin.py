from django.contrib import admin  # type: ignore

from NewsPortal.settings import logger
# from .models import Category,
from .models import Comment, Author, Post, Subscriber, Category


def delete_all_news(modeladmin, request, queryset):
    """
    Удаляет все новостные посты.

    Аргументы:
        modeladmin: Экземпляр администратора модели.
        request: Объект запроса.
        queryset: QuerySet новостных постов для удаления.

    Возвращает:
        None
    """
    Post.objects.all().delete()
    logger.warning('Task: delete_all_news')


def delete_all_ratings(modeladmin, request, queryset):
    """
    Удаляет все рейтинги в базе данных.

    Параметры:
        modeladmin (Admin): Экземпляр администратора модели.
        request (HttpRequest): Объект HTTP-запроса.
        queryset (QuerySet): QuerySet объектов, для которых нужно удалить рейтинги.

    Возвращает:
        None
    """
    Post.objects.all().update(rating=0)
    logger.warning('Task: delete_all_ratings')


def delete_all_comments(modeladmin, request, queryset):
    """
    Удаляет все комментарии в модели Comment.

    :param modeladmin: Экземпляр администратора модели.
    :type modeladmin: ModelAdmin

    :param request: Объект запроса.
    :type request: HttpRequest

    :param queryset: queryset комментариев для удаления.
    :type queryset: QuerySet

    :return: None
    """
    Comment.objects.all().delete()
    logger.warning('Task: delete_all_comments')


class PostCategoryFilter(admin.SimpleListFilter):
    title = ('Category')
    parameter_name = 'post_category'

    def lookups(self, request, model_admin):
        """
        Генерирует список уникальных идентификаторов категорий и соответствующих строковых представлений.

        Аргументы:
            request (Request): Объект запроса, переданный в представление.
            model_admin (ModelAdmin): Класс администратора для модели.

        Возвращает:
            List[Tuple[int, str]]: Список кортежей, содержащих идентификаторы категорий и их строковые представления.
        """
        categories = set()
        for post in model_admin.get_queryset(request):
            categories.update(post.postCategory.all())
        return [(category.id, str(category)) for category in categories]

    def queryset(self, request, queryset):
        """
        Фильтрует заданный `queryset` на основе значения `self.value()`.

        Аргументы:
            request: Объект запроса.
            queryset: Фильтруемый queryset.

        Возвращает:
            Отфильтрованный queryset.
        """
        value = self.value()
        if value:
            return queryset.filter(postCategory__id=value)
        return queryset


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'text', 'post_category_display', 'categoryType', 'rating')
    list_filter = ('categoryType', 'author', 'dateCreation', PostCategoryFilter)
    search_fields = ('title', 'text')
    actions = [delete_all_news, delete_all_ratings]
    logger.info('Task: PostAdmin')

    def post_category_display(self, obj):
        """
        Возвращает строковое представление категорий, связанных с данным объектом.

        Параметры:
            obj (Object): Объект, для которого нужно получить категории.

        Возвращает:
            str: Строка, содержащая имена категорий, разделенные запятой.
        """
        return ', '.join([category.name for category in obj.postCategory.all()])

    post_category_display.short_description = 'Category'


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('authorUser', 'ratingAuthor')
    list_filter = ('authorUser', 'ratingAuthor')
    search_fields = ('authorUser', 'ratingAuthor')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('commentUser', 'commentPost', 'text')
    list_filter = ('commentPost', 'commentUser')
    search_fields = ('commentUser', 'commentPost')
    actions = [delete_all_comments]


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('user', 'category')
    list_filter = ('category', 'user')
    search_fields = ('user', 'category')


# class CategoryAdmin(TranslationAdmin):
#     model = Category
#
#
# class MyModelAdmin(TranslationAdmin):
#     model = MyModel


# admin.site.register(MyModel)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Subscriber, SubscriberAdmin)

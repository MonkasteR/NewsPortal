from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.utils.translation import gettext as _

from NewsPortal.settings import logger


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    # rating__sum
    def update_rating(self):
        """
        Обновляет рейтинг текущего автора.

        Эта функция вычисляет рейтинг для автора текущего экземпляра, 
        суммируя рейтинги постов, комментариев и комментариев к постам автора. 
        Рейтинг вычисляется по следующей формуле:

        ratingAuthor = (authorPostRating * 3) + authorCommentRating + authorPostCommentRating

        Параметры:
            self (Author): Текущий экземпляр автора.

        Возвращает:
            None

        Выбрасывает:
            None
        """
        authorPostRating = Post.objects.filter(author_id=self.pk).aggregate(
            count=Coalesce(Sum('rating'),
                           0)
        )['count']
        authorCommentRating = Comment.objects.filter(
            commentUser_id=self.authorUser).aggregate(count=Coalesce(Sum('rating'),
                                                                     0)
                                                      )['count']
        authorPostCommentRating = Comment.objects.filter(
            commentPost__author__authorUser=self.authorUser).aggregate(
            count=Coalesce(Sum('rating'), 0))['count']

        self.ratingAuthor = authorPostRating * 3 + authorCommentRating + authorPostCommentRating
        self.save()

    def __str__(self):
        """
        Возвращает имя пользователя автора в виде строки.

        return: Строка, представляющая имя пользователя автора.
        """
        return self.authorUser.username

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, help_text=_('category name'))
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        """
        Возвращает строковое представление объекта.
        return: Строка, представляющая имя объекта.
        """
        logger.info(f'Category: {self.name}')
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, "Новость"),
        (ARTICLE, 'Статья'),
    )
    dateCreation = models.DateTimeField(auto_now_add=True)
    categoryType = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default=ARTICLE
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        """
        Возвращает строковое представление объекта.

        Этот метод переопределяет встроенный метод `__str__` для предоставления 
        пользовательского строкового представления объекта. Он объединяет имя 
        пользователя автора, заголовок поста и первые 123 символа текста поста, 
        за которым следует многоточие.

        Возвращает:
            str: Строковое представление объекта.
        """
        logger.info(f'Post: {self.title}')
        return f'{self.author.authorUser.username} : {self.title} : {self.text[0:123]}...'

    def save(self, *args, **kwargs):
        """
        Сохраняет экземпляр в базе данных и удаляет кэш 
        для соответствующего объекта новости.

        Параметры:
            *args: Переменное число позиционных аргументов.
            **kwargs: Произвольное число именованных аргументов.

        Возвращает:
            None
        """
        super().save(*args, **kwargs)
        cache.delete(f'news-{self.pk}')

    def get_absolute_url(self):
        """
        Генерирует абсолютный URL для текущего объекта.
        Эта функция использует функцию reverse() для генерации URL-шаблона для 
        представления 'one_news', передавая ID текущего объекта в качестве аргумента.

        Параметры:
            self (object): Текущий объект.

        Возвращает:
            str: Абсолютный URL для текущего объекта.
        """
        logger.info(f'URL: {self.get_absolute_url()}')
        return reverse('one_news', args=[str(self.id)])

    def like(self):
        """
        Увеличивает значение поля `rating` текущего объекта на 1 и сохраняет изменения.

        Параметры:
            Нет

        Возвращает:
            Ничего
        """
        self.rating = models.F('rating') + 1
        self.save()
        logger.info('Task: like')

    def dislike(self):
        """
        Уменьшает рейтинг объекта на 1 и сохраняет изменения.

        Эта функция не принимает никаких параметров.

        Эта функция не возвращает значений.
        """
        self.rating = models.F('rating') - 1
        self.save()
        logger.info('Task: dislike')

    def preview(self):
        """
        Возвращает предпросмотр первых 123 символов текста, за которым следует '...'.

        :return: Строка, представляющая предпросмотр текста.
        """
        logger.info('Task: preview')
        return self.text[0:123] + '...'

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        """
        Возвращает строковое представление объекта.
        """
        logger.info(f'Comment: {self.text}')
        return f'{self.commentUser} : {self.text[0:123]}...'

    def like(self):
        """
        Увеличивает рейтинг объекта на 1 и сохраняет изменения.

        Параметры:
            None

        Возвращает:
            None
        """
        self.rating = models.F('rating') + 1
        self.save()
        logger.info('Task: like')

    def dislike(self):
        """
        Уменьшает рейтинг объекта на 1 и сохраняет изменения.

        Параметры:
            self (object): Экземпляр объекта, вызывающий функцию.

        Возвращает:
            None
        """
        self.rating = models.F('rating') - 1
        self.save()
        logger.info('Task: dislike')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class PostCategory(models.Model):
    postThrow = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Subscriber(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    # email = models.EmailField()

    def __str__(self):
        """
        Возвращает строковое представление объекта.
        """
        logger.info(f'Subscriber: {self.user}')
        return str(self.user)

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

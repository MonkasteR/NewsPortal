from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

import News
from NewsPortal.settings import DEFAULT_FROM_EMAIL


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    # rating__sum
    def update_rating(self):
        authorPostRating = Post.objects.filter(author_id=self.pk).aggregate(count=Coalesce(Sum('rating'), 0))['count']
        authorCommentRating = Comment.objects.filter(commentUser_id=self.authorUser).aggregate(
            count=Coalesce(Sum('rating'), 0))['count']
        authorPostCommentRating = Comment.objects.filter(
            commentPost__author__authorUser=self.authorUser).aggregate(
            count=Coalesce(Sum('rating'), 0))['count']

        self.ratingAuthor = authorPostRating * 3 + authorCommentRating + authorPostCommentRating
        self.save()

    def __str__(self):
        return self.authorUser.username

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField('Subscriber', related_name='categories')

    def __str__(self):
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
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.author.authorUser.username} : {self.title} : {self.text[0:123]}...'

    def get_absolute_url(self):
        return reverse('one_news', args=[str(self.id)])

    def like(self):
        self.rating = models.F('rating') + 1
        self.save()

    def dislike(self):
        self.rating = models.F('rating') - 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    @login_required
    @receiver(post_save, sender=News)
    def send_news_notification(sender, instance, **kwargs):
        subject = "Новая новость: {}".format(instance.title)
        message = render_to_string('news_notification_email.html', {'news': instance})
        user = get_user()
        from_email = DEFAULT_FROM_EMAIL
        subscribers = Subscriber.objects.all()

        for subscriber in subscribers:
            to_email = subscriber.email
            link = reverse('one_news', args='one_news.pk')  # Замените на свой URL для просмотра новости
            message += f"\nЧтобы прочитать новость, перейдите по ссылке: {link}"

            send_mail(subject, message, from_email, [to_email])

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.commentUser} : {self.text[0:123]}...'

    def like(self):
        self.rating = models.F('rating') + 1
        self.save()

    def dislike(self):
        self.rating = models.F('rating') - 1
        self.save()

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class PostCategory(models.Model):
    postThrow = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

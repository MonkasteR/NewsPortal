from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce


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
        return self.authorUser

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, "Новость"),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.title

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


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.commentUser

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

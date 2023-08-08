from django.contrib import admin  # type: ignore

from .models import Category, Comment, Author, Post, PostCategory

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
# admin.site.register(PostCategory)

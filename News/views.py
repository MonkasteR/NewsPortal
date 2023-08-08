from django.views.generic import ListView, DetailView

from .models import Post


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'  # сортируем по убыванию даты, сначала самая свежая новость, далее по убыванию
    template_name = 'all_news.html'
    context_object_name = 'all_news'


class PostDetail(DetailView):
    model = Post
    template_name = 'one_news.html'
    context_object_name = 'one_news'

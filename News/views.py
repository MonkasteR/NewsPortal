from django.views.generic import ListView, DetailView

from .filters import NewsFilter
from .models import Post


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'  # сортируем по убыванию даты, сначала самая свежая новость, далее по убыванию
    template_name = 'all_news.html'
    context_object_name = 'all_news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'one_news.html'
    context_object_name = 'one_news'

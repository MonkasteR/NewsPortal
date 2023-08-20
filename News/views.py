from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .filters import NewsFilter
from .forms import NewsForm
from .models import Post


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
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


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = Post.NEWS
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('posts_list')


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('posts_list')


class PostDetail(DetailView):
    model = Post
    template_name = 'one_news.html'
    context_object_name = 'one_news'


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = Post.ARTICLE
        return super().form_valid(form)


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('posts_list')


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('posts_list')

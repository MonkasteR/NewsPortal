from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .filters import NewsFilter
from .forms import NewsForm
from .models import Post, Category, Subscriber
from .signals import send_news_notification


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
    permission_required = ('News.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = Post.NEWS
        send_news_notification(self.request, self.object)
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('News.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('posts_list')


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('News.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('posts_list')


class PostDetail(DetailView):
    model = Post
    template_name = 'one_news.html'
    context_object_name = 'one_news'


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = Post.ARTICLE
        return super().form_valid(form)


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('News.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('posts_list')


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('News.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('posts_list')


class SubscriptionView(View):
    def get(self, request):
        return render(request, 'subscriptions.html')

    @login_required
    def subscriptions(request):
        user_email = request.user.email
        categories = Category.objects.all()
        context = {
            'user_email': user_email,
            'categories': categories
        }
        return render(request, 'subscriptions.html', context)


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    # ordering = '-dateCreation'
    # paginate_by = 10
    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categoryType=self.category).order_by('-dateCreation')
        return queryset

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filterset = NewsFilter(self.request.GET, queryset)
    #     return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

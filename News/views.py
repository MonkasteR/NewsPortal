import pytz
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache
from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from NewsPortal.settings import logger
from . import serializers
from .filters import NewsFilter
from .forms import NewsForm
from .models import Post, Category, Subscriber, Author


class PostList(ListView):
    model = Post
    curent_time = timezone.now()
    ordering = '-dateCreation'
    template_name = 'news/all_news.html'
    context_object_name = 'all_news'
    paginate_by = 10
    logger.info('View: all_news')

    def get_queryset(self):
        """
        Возвращает queryset для представления NewsFilter.

        param self: Экземпляр класса.
        return: Отфильтрованный queryset на основе параметров request.GET.
        """
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        """
        Получает данные контекста для представления.

        param **kwargs: Дополнительные именованные аргументы для родительского метода.
        return: Словарь данных контекста.
        """
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        """
        Установить переменную сессии `django_timezone` в значение параметра
        `timezone` в POST-запросе.

        Аргументы:
            request (HttpRequest): Объект HTTP-запроса.

        Возвращает:
            HttpResponseRedirect: Ответ-перенаправление на корневой URL (/).
        """
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/news')


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news/news_edit.html'
    success_url = reverse_lazy('posts_list')
    logger.info('View: news_create')

    def form_valid(self, form):
        """
        Сохраняет форму и возвращает результат вызова метода form_valid родительского класса.

        Аргументы:
            form: Объект формы.

        Возвращает:
            Результат вызова метода form_valid родительского класса.
        """
        post = form.save(commit=False)
        post.categoryType = Post.NEWS
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('News.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news/news_edit.html'
    success_url = reverse_lazy('posts_list')
    logger.info('View: news_update')


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('News.delete_post',)
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('posts_list')
    logger.info('View: news_delete')


class PostDetail(DetailView):
    model = Post
    curent_time = timezone.now()
    template_name = 'news/one_news.html'
    context_object_name = 'one_news'
    logger.info('View: one_news')

    def get_object(self, *args, **kwargs):
        """
        Извлекает объект из кэша, если он существует, 
        в противном случае извлекает его из базы данных и кэширует.

        :param args: Позиционные аргументы, передаваемые в функцию.
        :param kwargs: Именованные аргументы, передаваемые в функцию.
        :return: Извлеченный объект.
        """
        obj = cache.get(f'news-{self.kwargs["pk"]}')
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'news-{self.kwargs["pk"]}', obj)
        return obj

    def get_context_data(self, **kwargs):
        """
        Возвращает данные контекста для представления.

        Аргументы:
            **kwargs: Дополнительные именованные аргументы.

        Возвращает:
            dict: Данные контекста, содержащие текущее время и общие часовые пояса.
        """
        context = super().get_context_data(**kwargs)

        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones

        return context

    def post(self, request, *args, **kwargs):
        """
        Устанавливает временную зону Django в сеансе запроса на основе
        значения 'timezone' из данных POST запроса.

        Параметры:
            request (HttpRequest): Объект HTTP-запроса.
            *args: Список позиционных аргументов.
            **kwargs: Словарь именованных аргументов.

        Возвращает:
            HttpResponseRedirect: Ответ-перенаправление на представление 'one_news'
            с параметром 'pk', взятым из словаря self.kwargs, в качестве URL-параметра.
        """
        request.session['django_timezone'] = request.POST.get('timezone', None)
        return redirect('one_news', pk=self.kwargs['pk'])


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('News.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news/news_edit.html'
    success_url = reverse_lazy('posts_list')
    logger.info('View: article_create')

    def form_valid(self, form):
        """
        Сохраняет данные формы и устанавливает тип категории поста на 'ARTICLE'.

        Аргументы:
            form: Объект формы, содержащий данные для сохранения.

        Возвращает:
            Результат вызова метода 'form_valid' родительского класса.
        """
        post = form.save(commit=False)
        post.categoryType = Post.ARTICLE
        return super().form_valid(form)


class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('News.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news/news_edit.html'
    success_url = reverse_lazy('posts_list')
    logger.info('View: article_update')


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('News.delete_post',)
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('posts_list')
    logger.info('View: article_delete')


class SubscriptionView(View):
    def get(self, request):
        """
        Метод GET для обработки HTTP GET-запросов.

        Аргументы:
            request (HttpRequest): Объект HTTP-запроса.

        Возвращает:
            HttpResponse: Отображенный ответ, содержащий шаблон 'subscriptions.html'.
        """
        logger.info('View: subscriptions')
        return render(request, 'news/subscriptions.html')

    @login_required
    def subscriptions(request):
        """
        Отображает страницу подписок для авторизованного пользователя.

        Параметры:
            request (HttpRequest): Объект HTTP-запроса.

        Возвращает:
            HttpResponse: Отображенный HTML-шаблон для страницы подписок.
        """
        user_email = request.user.email
        categories = Category.objects.all()
        context = {
            'user_email': user_email,
            'categories': categories
        }
        logger.info('View: subscriptions')
        return render(request, 'news/subscriptions.html', context)


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'
    logger.info('View: category_list')

    # ordering = '-dateCreation'
    # paginate_by = 10
    def get_queryset(self):
        """
        Получает queryset постов, отфильтрованных по типу категории и
        отсортированных по дате создания.

        Возвращает:
            queryset: queryset объектов Post, отфильтрованных по типу категории и
            отсортированных по дате создания.
        """
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categoryType=self.category).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        """
        Получает данные контекста для представления.

        param kwargs: Необязательные именованные аргументы.

        return: Словарь, содержащий данные контекста.
        """
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
@csrf_protect
def subscriptions(request):
    """
    Функция представления для управления подписками пользователя.
    Данная функция декорирована декораторами `@login_required` и `@csrf_protect` для 
    обеспечения доступа только авторизованных пользователей и защиты от атак подделки 
    межсайтовых запросов.

    Параметры:
        request (HttpRequest): Объект HTTP-запроса.

    Возвращает:
        HttpResponse: Объект HTTP-ответа с отображенной страницей подписок.
    """
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
    # raise Exception(dict(request))
    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    logger.info('Def: subscriptions')
    return render(
        request,
        'news/subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


@login_required
def subscribe(request, pk):
    """
    Подписывает пользователя на категорию.

    Аргументы:
        request: Объект HTTP-запроса.
        pk (int): ID категории, на которую нужно подписаться.

    Возвращает:
        HttpResponse: Отображенный HTML-ответ с подписанной 
        категорией и сообщением об успехе.
    """
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = f'Вы успешно подписались на категорию {category}'
    logger.info('Def: subscribe')
    return render(request, 'subscribe.html', {'category': category, 'message': message})


class PostListViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostListSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = NewsFilter


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = serializers.AuthorSerializer


class NewsDeleteViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.NewsDeleteSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = NewsFilter


class NewsCreateViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.NewsCreateSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = NewsFilter


class NewsUpdateViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.NewsCreateSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = NewsFilter


class ArticleCreateViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.ArticleCreateSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = NewsFilter


class ArticleUpdateViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.ArticleUpdateSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = NewsFilter


class ArticleDeleteViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.ArticleDeleteSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = NewsFilter


class SubscriptionViewViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = serializers.SubscriptionSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = NewsFilter


class CategoryListViewViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategoryListSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = NewsFilter


class PostDetailViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostDetailSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = NewsFilter
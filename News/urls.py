from django.urls import path
from django.views.decorators.cache import cache_page

from accounts.views import test_page
from .views import PostList, PostDetail, NewsCreate, NewsUpdate, NewsDelete, CategoryListView, subscriptions, subscribe

urlpatterns = [
    path('', cache_page(60)(PostList.as_view()), name='posts_list'),
    path('<int:pk>', cache_page(300)(PostDetail.as_view()), name='one_news'),
    path('search/', PostList.as_view()),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('test/', test_page, name='test_page'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    # path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]

from django.urls import path

from accounts.views import test_page
from .views import PostList, PostDetail, NewsCreate, NewsUpdate, NewsDelete, CategoryListView
from .views import SubscriptionView

urlpatterns = [
    path('', PostList.as_view(), name='posts_list'),
    path('<int:pk>', PostDetail.as_view(), name='one_news'),
    path('search/', PostList.as_view()),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('test/', test_page, name='test_page'),
    # path('subscriptions/', views.SubscriptionView.as_view(), name='subscriptions'),
    path('subscriptions/', SubscriptionView.as_view(), name='subscriptions'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
]

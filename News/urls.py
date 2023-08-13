from django.urls import path

from .views import PostList, PostDetail, NewsCreate, NewsUpdate, NewsDelete

urlpatterns = [
    path('', PostList.as_view(), name='posts_list'),
    path('<int:pk>', PostDetail.as_view(), name='one_news'),
    path('search/', PostList.as_view()),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    # /articles/create/
    # /articles/<int:pk>/edit/
    # /articles/<int:pk>/delete/
]

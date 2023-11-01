from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from News import views
from News.views import ArticleCreate, ArticleUpdate, ArticleDelete

router = routers.DefaultRouter()
router.register(r'delete_news', views.NewsDelete)
router.register(r'create_news', views.NewsCreate)
router.register(r'update_news', views.NewsUpdate)
router.register(r'create_article', views.ArticleCreate)
router.register(r'update_article', views.ArticleUpdate)
router.register(r'delete_article', views.ArticleDelete)
router.register(r'subscription', views.SubscriptionView)
router.register(r'category', views.CategoryListView)
router.register(r'news', views.PostList)
router.register(r'authors', views.AuthorViewSet)
router.register(r'post', views.PostDetail)


urlpatterns = [
    path('', include('News.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('news/', include('News.urls')),
    path("accounts/", include("allauth.urls")),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]

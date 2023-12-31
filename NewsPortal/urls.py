from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from News import views
from News.views import ArticleCreate, ArticleUpdate, ArticleDelete

router = routers.DefaultRouter()
router.register(r"delete_news", views.NewsDeleteViewSet)
router.register(r"create_news", views.NewsCreateViewSet)
router.register(r"update_news", views.NewsUpdateViewSet)
router.register(r"create_article", views.ArticleCreateViewSet)
router.register(r"update_article", views.ArticleUpdateViewSet)
router.register(r"delete_article", views.ArticleDeleteViewSet)
router.register(r"subscription", views.SubscriptionViewViewSet)
router.register(r"category", views.CategoryListViewViewSet)
router.register(r"news", views.PostListViewSet)
router.register(r"authors", views.AuthorViewSet)
router.register(r"post", views.PostDetailViewSet)


urlpatterns = [
    path("", include("News.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path("pages/", include("django.contrib.flatpages.urls")),
    path("news/", include("News.urls")),
    path("accounts/", include("allauth.urls")),
    path("articles/create/", ArticleCreate.as_view(), name="article_create"),
    path("articles/<int:pk>/edit/", ArticleUpdate.as_view(), name="article_edit"),
    path("articles/<int:pk>/delete/", ArticleDelete.as_view(), name="article_delete"),
    path("api/", include(router.urls)),
]

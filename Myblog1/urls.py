"""Myblog1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter

from storm.sitemaps import ArticleSitemap, TagSitemap, CategorySitemap
from api import views as api_views
if settings.API_FLAG:
    router = DefaultRouter()
    router.register(r'users', api_views.UserListSet)
    router.register(r'articles', api_views.ArticleListSet)
    router.register(r'tags', api_views.TagListSet)
    router.register(r'categorys', api_views.CategoryListSet)
#
# sitemaps = {
#     'articles': ArticleSitemap,
#     'tags': TagSitemap,
#     'categories': CategorySitemap
# }

urlpatterns = [
    # url(r'^tinymce/', include('tinymce.urls')),
    # url(r'mdeditor/', include('mdeditor.urls')),
    url(r'^admin/', admin.site.urls),
    # 用户user
    url(r'^accounts/', include(('user.urls','user'), namespace='accounts')),


    url('', include(('storm.urls','blog'), namespace='blog')),  # blog

    url(r'^comment/', include(('comment.urls','comment'), namespace='comment')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 加入这个才能显示media文件
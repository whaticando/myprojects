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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import *

urlpatterns = [
    url(r'404/$', Page_Not_Found.as_view(), name='notfound'),
    url(r'^$', IndexView.as_view(template_name='index.html'), name='index'),  # 主页，自然排序
    url(r'^link/$', LinkView, name='link'),  # 申请友情链接
    url(r'^category/message/$', MessageView, name='message'),
    url(r'^category/about/$', AboutView, name='about'),

    url(r'^category/exchange/$', ExchangeView, name='exchange'),

    # 分类页面
    url(r'^category/(?P<bigslug>.*?)/(?P<slug>.*?)', IndexView.as_view(template_name='content.html'), name='category'),
    # 归档页面
    url(r'^date/(?P<year>\d+)/(?P<month>\d+)/$', IndexView.as_view(template_name='archive.html'), name='date'),
    # 标签页面
    url(r'^tag/(?P<tag>.*?)/$', IndexView.as_view(template_name='content.html'), name='tag'),
    # 文章详情页面
    url(r'^article/(?P<slug>.*?)/$', DetailView.as_view(), name='article'),
    # 全文搜索
    url(r'^search/$', MySearchView.as_view(), name='search'),
    # 喜欢
    url(r'^love/$', LoveView, name='love'),

    url(r'^(?P<username>\w+)/backend/$', backend),
    url(r'^(?P<username>\w+)/backend_add_article/$', backend_add_article, name='add_article'),
    url("backend/(\d+)/delete_article/$", delete_article, name='delete_article'),
    url("backend/(\d+)/edit_article/$", edit_article, name='edit_article'),

]

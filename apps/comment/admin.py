from django.contrib import admin
from storm.models import Article
from .models import ArticleComment,Comment,AboutComment,MessageComment
#
# Register your models here.
@admin.register(ArticleComment)
class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'create_date'
    list_display = ('id', 'author', 'belong', 'create_date', 'show_content')
    list_filter = ('author', 'belong',)
    ordering = ('-id',)
    # 设置需要添加a标签的字段
    list_display_links = ('id', 'show_content')
    search_fields = ('author__username', 'belong__title')

    # 使用方法来自定义一个字段，并且给这个字段设置一个名称
    def show_content(self, obj):
        return obj.content[:30]

    show_content.short_description = '评论内容'
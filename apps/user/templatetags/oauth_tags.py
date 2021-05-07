'''
   author :wang
   date:  '2021/4/7'

'''

# 创建了新的tags标签文件后必须重启服务器
from django import template
from ..models import Ouser
from comment.models import CommentUser

register = template.Library()


@register.simple_tag()
def get_user_data(uid):
    user = Ouser.objects.filter(id=uid)
    if user:
        return user[0]
    else:
        return ''


@register.simple_tag()
def get_tourist_data(uid):
    """返回评论者的信息"""
    user = CommentUser.objects.filter(id=uid)
    if user:
        return user[0]
    else:
        return ''

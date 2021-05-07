from django.db import models
from django.conf import settings
from storm.models import Article
from ckeditor.fields import RichTextField
import markdown
import emoji
import re

emoji_info = [
    [('aini_org', '爱你'), ('baibai_thumb', '拜拜'),
     ('baobao_thumb', '抱抱'), ('beishang_org', '悲伤'),
     ('bingbujiandan_thumb', '并不简单'), ('bishi_org', '鄙视'),
     ('bizui_org', '闭嘴'), ('chanzui_org', '馋嘴')],
    [('chigua_thumb', '吃瓜'), ('chongjing_org', '憧憬'),
     ('dahaqian_org', '哈欠'), ('dalian_org', '打脸'),
     ('ding_org', '顶'), ('doge02_org', 'doge'),
     ('erha_org', '二哈'), ('gui_org', '跪了')],
    [('guzhang_thumb', '鼓掌'), ('haha_thumb', '哈哈'),
     ('heng_thumb', '哼'), ('huaixiao_org', '坏笑'),
     ('huaxin_org', '色'), ('jiyan_org', '挤眼'),
     ('kelian_org', '可怜'), ('kuxiao_org', '允悲')],
    [('ku_org', '酷'), ('leimu_org', '泪'),
     ('miaomiao_thumb', '喵喵'), ('ningwen_org', '疑问'),
     ('nu_thumb', '怒'), ('qian_thumb', '钱'),
     ('sikao_org', '思考'), ('taikaixin_org', '太开心')],
    [('tanshou_org', '摊手'), ('tianping_thumb', '舔屏'),
     ('touxiao_org', '偷笑'), ('tu_org', '吐'),
     ('wabi_thumb', '挖鼻'), ('weiqu_thumb', '委屈'),
     ('wenhao_thumb', '费解'), ('wosuanle_thumb', '酸')],
    [('wu_thumb', '污'), ('xiaoerbuyu_org', '笑而不语'),
     ('xiaoku_thumb', '笑cry'), ('xixi_thumb', '嘻嘻'),
     ('yinxian_org', '阴险'), ('yun_thumb', '晕'),
     ('zhouma_thumb', '怒骂'), ('zhuakuang_org', '抓狂')]
]

def get_emoji_imgs(body):
    '''
    替换掉评论中的标题表情，并且把表情替换成图片地址
    :param body:
    :return:
    '''
    img_url = '<img class="comment-emoji-img" src="/static/comment/weibo/{}.png" title="{}" alt="{}">'
    for i in emoji_info:
        for ii in i:
            emoji_url = img_url.format(ii[0], ii[1], ii[0])
            body = re.sub(':{}:'.format(ii[0]), emoji_url, body)
    tag_info = {
        '<h\d>': '',
        '</h\d>': '<br>',
        '<script.*</script>': '',
        '<meta.*?>': '',
        '<link.*?>': ''
    }
    for k, v in tag_info.items():
        body = re.sub(k, v, body)
    return body

# 评论者信息表
class CommentUser(models.Model):
    nickname = models.CharField(max_length=20, verbose_name='昵称')
    email = models.CharField(max_length=30, verbose_name='邮箱')
    address = models.CharField(max_length=200, verbose_name='地址')


# 评论信息表
class Comment(models.Model):
    author = models.ForeignKey(CommentUser, related_name='%(class)s_related', verbose_name='评论人',on_delete=models.CASCADE)
    create_date = models.DateTimeField('创建时间', auto_now_add=True)
    content = models.TextField('评论内容')
    parent = models.ForeignKey('self', verbose_name='父评论', related_name='%(class)s_child_comments', blank=True, null=True,on_delete=models.CASCADE)
    rep_to = models.ForeignKey('self', verbose_name='回复',
                               related_name='%(class)s_rep_comments', blank=True, null=True,on_delete=models.CASCADE)

    class Meta:
        """这是一个元类，用来继承的"""

        abstract = True

    def __str__(self):
        return self.content[:20]

    def content_to_markdown(self):
        # 先转换成emoji然后转换成markdown,'escape':所有原始HTML将被转义并包含在文档中
        to_emoji_content = emoji.emojize(self.content, use_aliases=True)
        to_md = markdown.markdown(to_emoji_content,
                                  safe_mode='escape',
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                  ])
        return to_md


# 文章评论区，据继承评论信息表
class ArticleComment(Comment):
    # 记录评论属于哪篇文章
    belong = models.ForeignKey(Article, related_name='article_comments', verbose_name='所属文章',on_delete=models.CASCADE)

    class Meta:
        verbose_name = '文章评论'
        verbose_name_plural = verbose_name
        ordering = ['create_date']


# 关于自己页面评论信息
class AboutComment(Comment):
    class Meta:
        verbose_name = '关于自己评论'
        verbose_name_plural = verbose_name
        ordering = ['create_date']




# 给我留言页面评论信息
class MessageComment(Comment):
    class Meta:
        verbose_name = '给我留言'
        verbose_name_plural = verbose_name
        ordering = ['create_date']


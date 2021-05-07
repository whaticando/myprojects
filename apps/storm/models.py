from django.db import models
from django.conf import settings
from django.shortcuts import reverse
import markdown
import emoji
import re
from ckeditor.fields import RichTextField
from mdeditor.fields import MDTextField

# Create your models here.
# 文章关键词，用来作为SEO中的keywords
class Keyword(models.Model):
    name = models.CharField('文章关键词', max_length=31)

    class Meta:
        verbose_name = '关键词'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


# 文章的标签
class Tag(models.Model):
    name = models.CharField('文学标签', max_length=31)
    slug = models.SlugField(unique=True)
    description = models.TextField('描述', max_length=255, default=settings.SITE_DESCRIPTION,
                                   help_text='用来作为SEO中description,长度参考SEO标准')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_absoluate_url(self):
        return reverse('blog:tag', kwargs={'tag': self.name})

    def get_article_list(self):
        """返回当前标签下所有发表的文章列表"""
        return Article.objects.filter(tags=self)


# 网站导航菜单分类栏
class BigCategory(models.Model):
    name = models.CharField('文章大分类', max_length=31)
    # 用作文章的访问路径，每篇文章有独一无二的标识，下同
    slug = models.SlugField(unique=True)
    description = models.TextField('描述', max_length=255, default=settings.SITE_DESCRIPTION,
                                   help_text='用来作为SEO中description,长度参考SEO标准')
    keywords = models.TextField('关键词', max_length=255, default=settings.SITE_KEYWORDS,
                                help_text='用来作为SEO中keywords,长度参考SEO标准')

    class Meta:
        verbose_name = '大分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


#
# 导航栏，分类下的下拉菜单分类
class Category(models.Model):
    name = models.CharField('文章分类', max_length=31)
    slug = models.SlugField(unique=True)
    description = models.TextField('描述', max_length=255, default=settings.SITE_DESCRIPTION,
                                   help_text='用来作为SEO中description,长度参考SEO标准')
    bigcategory = models.ForeignKey(BigCategory, verbose_name='大分类', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug, 'bigslug': self.bigcategory.slug})

    def get_article_list(self):
        return Article.objects.filter(category=self)


# 文章
class Article(models.Model):
    IMG_LINK = '/static/images/summary.jpg'
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.CASCADE)
    title = models.CharField(max_length=127, verbose_name='文章标题')
    summary = models.TextField('文章摘要', max_length=255, default='文章摘要等同于网页description内容，请务必填写...')
    body = RichTextField(verbose_name='文章内容')
    img_link = models.CharField('图片地址', default=IMG_LINK, max_length=255)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    views = models.IntegerField('阅读量', default=0)
    loves = models.IntegerField('喜爱量', default=0)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, verbose_name='文章分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签')
    keywords = models.ManyToManyField(Keyword, verbose_name='文章关键词',
                                      help_text='文章关键词，用来作为SEO中keywords，最好使用长尾词，3-4个足够')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return self.title[:20]

    def get_absolute_url(self):
        return reverse('blog:article', kwargs={'slug': self.slug})

    def body_to_markdown(self):
        return markdown.markdown(self.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

    def update_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_pre(self):  # 上一章
        return Article.objects.filter(id__lt=self.id).order_by('-id').first()

    def get_next(self):  # 下一章

        return Article.objects.filter(id__gt=self.id).order_by('id').first()


# 幻灯片
class Carousel(models.Model):
    number = models.IntegerField('编号', help_text='编号决定图片播放的瞬息，图片不多于5张')
    title = models.CharField('标题', max_length=31, blank=True, null=True, help_text='标题可以为空')
    content = models.CharField('描述', max_length=127)
    img_url = models.CharField('图片地址', max_length=255)
    url = models.CharField('跳转链接', max_length=255, default='#', help_text='图片跳转的超链接，默认#表示不跳转')

    class Meta:
        verbose_name = '图片轮播'
        verbose_name_plural = verbose_name
        # 编号越小越靠前，添加的时间约晚约靠前
        ordering = ['number', '-id']

    def __str__(self):
        return self.content[:25]


# 死链
class Silian(models.Model):
    badurl = models.CharField('死链地址', max_length=255, help_text='注意：地址是以http开头的完整链接格式')
    remark = models.CharField('死链说明', max_length=63, blank=True, null=True)
    add_date = models.DateTimeField('提交日期', auto_now_add=True)

    class Meta:
        verbose_name = '死链'
        verbose_name_plural = verbose_name
        ordering = ['-add_date']

    def __str__(self):
        return self.badurl


# 友情链接表
class FriendLink(models.Model):
    name = models.CharField('网站名称', max_length=63)
    description = models.CharField('网站描述', max_length=100, blank=True)
    link = models.URLField('友联地址', help_text='请填写http或https开头的完整形式地址')
    logo = models.URLField('网站LOGO', help_text='请填写http或https开头的完整形式地址', blank=True)
    create_date = models.DateTimeField('创建时间', auto_now_add=True)
    is_active = models.BooleanField('是否有效', default=True)
    is_show = models.BooleanField('是否首页展示', default=False)

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['create_date']

    def __str__(self):
        return self.name

    def get_home_url(self):
        """提取友链的主页"""
        u = re.findall(r'(http|https://.*?)/.*?', self.link)
        home_url = u[0] if u else self.link
        return home_url

    def active_to_false(self):
        self.is_active = False
        self.save(update_fields=['is_active'])

    def show_to_false(self):
        self.is_show = True
        self.save(update_fields=['is_show'])


# 公告
class Activate(models.Model):
    text = models.TextField('公告', null=True)
    is_active = models.BooleanField('是否开启', default=False)
    add_date = models.DateTimeField('提交日期', auto_now_add=True)

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id

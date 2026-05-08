from django.db import models
from rest_framework import serializers

from app_news.models import NewsSerializer
from app_user.models import UserSerializer
from tool.public_tool import PublicTool


# 浏览模型类，继承django框架models.Model类
class Userbrowse(models.Model):
    # AutoField：自动递增属性
    id = models.AutoField(primary_key=True, db_column='id', verbose_name='主键id自增')
    # user：用户模型类对象
    # models.CASCADE：级联删除，删除用户时，自动删除用户下的所有浏览数据
    user = models.ForeignKey('app_user.User', models.CASCADE, db_column='userid', blank=False, null=False,
                             verbose_name='用户')
    # news：新闻模型类对象
    # models.CASCADE：级联删除，删除新闻时，自动删除新闻下的所有浏览数据
    news = models.ForeignKey('app_news.News', models.CASCADE, db_column='newsid', blank=False, null=False,
                             verbose_name='新闻')
    savedate = models.CharField(max_length=19, blank=False, null=False, db_column='savedate',
                                verbose_name='浏览时间')

    # 重定义模型类的字符串表示形式方法，默认：模型类实例对象
    # 管理员添加/修改/删除数据等操作后的提示信息
    def __str__(self):
        return ''

    # 重定义添加/修改save()函数，save()函数同时具有添加和修改功能，根据id主键是否为空判断添加/修改
    # 如果用户已浏览过当前新闻，更新浏览时间，如果没有，则添加浏览
    def save(self, *args, **kwargs):
        # 查询用户最近一次浏览，查询参数：用户id，id降序排列
        userbrowse = Userbrowse.objects.filter(user_id=self.user_id).order_by('-id').first()
        if userbrowse and userbrowse.news_id == self.news_id:
            # 用户最近一次浏览是当前新闻，更新浏览时间
            userbrowse.savedate = PublicTool().getCurrentTime()
            # 调用父类save()函数，更新
            super(Userbrowse, userbrowse).save(*args, **kwargs)
        else:
            # 删除用户对当前新闻的浏览，查询参数：用户id、新闻id
            Userbrowse.objects.filter(user_id=self.user_id, news_id=self.news_id).delete()
            # 调用父类save()函数，添加
            super(Userbrowse, self).save(*args, **kwargs)

    # 模型类的元数据配置类，用于定义模型类的配置选项
    class Meta:
        # 不允许django框架管理模型类的数据库表
        managed = False
        # 模型类映射的数据库表
        db_table = 'tb_userbrowse'
        # 模型类名称
        verbose_name = '浏览'
        # 模型类复数名称
        verbose_name_plural = verbose_name


# 基础浏览模型序列化类，继承django rest framework框架serializers.ModelSerializer类
class UserbrowseSerializer(serializers.ModelSerializer):
    # 自定义序列化属性，用户id，将user_id重命名为userid
    userid = serializers.IntegerField(source='user_id', read_only=True)
    # 自定义序列化属性，新闻id，将news_id重命名为newsid
    newsid = serializers.IntegerField(source='news_id', read_only=True)

    # 序列化类的元数据配置类，用于定义序列化类的配置选项
    class Meta:
        # 指定序列化类关联的模型类
        model = Userbrowse
        # 序列化的模型类属性，__all__：所有属性
        fields = '__all__'


# 关联查询浏览模型序列化类，继承基础浏览模型序列化类
class UserbrowseJoinSerializer(UserbrowseSerializer):
    # 自定义序列化属性，用户
    user = UserSerializer(read_only=True)
    # 自定义序列化属性，新闻
    news = NewsSerializer(read_only=True)

    # 序列化类的元数据配置类，用于定义序列化类的配置选项
    class Meta:
        # 指定序列化类关联的模型类
        model = Userbrowse
        # 序列化的模型类属性，__all__：所有属性
        fields = '__all__'

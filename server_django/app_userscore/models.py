from django.db import models
from rest_framework import serializers

from app_news.models import NewsSerializer
from app_user.models import UserSerializer


# 评分模型类，继承django框架models.Model类
class Userscore(models.Model):
    # AutoField：自动递增属性
    id = models.AutoField(primary_key=True, db_column='id', verbose_name='主键id自增')
    # user：用户模型类对象
    # models.CASCADE：级联删除，删除用户时，自动删除用户下的所有评分数据
    user = models.ForeignKey('app_user.User', models.CASCADE, db_column='userid', blank=False, null=False,
                             verbose_name='用户')
    # news：新闻模型类对象
    # models.CASCADE：级联删除，删除新闻时，自动删除新闻下的所有评分数据
    news = models.ForeignKey('app_news.News', models.CASCADE, db_column='newsid', blank=False, null=False,
                             verbose_name='新闻')
    score = models.IntegerField(blank=False, null=False, db_column='score', verbose_name='评分值')
    savedate = models.CharField(max_length=19, blank=False, null=False, db_column='savedate',
                                verbose_name='评分时间')

    # 重定义模型类的字符串表示形式方法，默认：模型类实例对象
    # 管理员添加/修改/删除数据等操作后的提示信息
    def __str__(self):
        return ''

    # 模型类的元数据配置类，用于定义模型类的配置选项
    class Meta:
        # 不允许django框架管理模型类的数据库表
        managed = False
        # 模型类映射的数据库表
        db_table = 'tb_userscore'
        # 模型类名称
        verbose_name = '评分'
        # 模型类复数名称
        verbose_name_plural = verbose_name


# 基础评分模型序列化类，继承django rest framework框架serializers.ModelSerializer类
class UserscoreSerializer(serializers.ModelSerializer):
    # 自定义序列化属性，用户id，将user_id重命名为userid
    userid = serializers.IntegerField(source='user_id', read_only=True)
    # 自定义序列化属性，新闻id，将news_id重命名为newsid
    newsid = serializers.IntegerField(source='news_id', read_only=True)

    # 序列化类的元数据配置类，用于定义序列化类的配置选项
    class Meta:
        # 指定序列化类关联的模型类
        model = Userscore
        # 序列化的模型类属性，__all__：所有属性
        fields = '__all__'


# 关联查询评分模型序列化类，继承基础评分模型序列化类
class UserscoreJoinSerializer(UserscoreSerializer):
    # 自定义序列化属性，用户
    user = UserSerializer(read_only=True)
    # 自定义序列化属性，新闻
    news = NewsSerializer(read_only=True)

    # 序列化类的元数据配置类，用于定义序列化类的配置选项
    class Meta:
        # 指定序列化类关联的模型类
        model = Userscore
        # 序列化的模型类属性，__all__：所有属性
        fields = '__all__'

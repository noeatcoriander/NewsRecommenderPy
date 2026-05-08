from django.db import models
from rest_framework import serializers

from app_newstype.models import NewstypeSerializer
from tool.public_tool import PublicTool


# 新闻模型类，继承django框架models.Model类
class News(models.Model):
    # AutoField：自动递增属性
    id = models.AutoField(primary_key=True, db_column='id', verbose_name='主键id自增')
    title = models.CharField(max_length=100, blank=False, null=False, db_column='title',
                             verbose_name='新闻标题')
    # newstype：新闻类型模型类对象
    # models.CASCADE：级联删除，删除新闻类型时，自动删除新闻类型下的所有新闻数据
    newstype = models.ForeignKey('app_newstype.Newstype', models.CASCADE, db_column='newstypeid',
                                 blank=False, null=False, verbose_name='新闻类型')
    # upload_to：重命名上传文件，上传文件名唯一
    photo = models.ImageField(upload_to=PublicTool().reset_filename, blank=False, null=False,
                              db_column='photo', verbose_name='新闻图片')
    newssource = models.CharField(max_length=255, blank=False, null=False, db_column='newssource',
                                  verbose_name='新闻来源')
    introduction = models.TextField(max_length=30000, blank=False, null=False, db_column='introduction',
                                    verbose_name='新闻内容')
    # default：默认0
    clicks = models.IntegerField(default=0, blank=False, null=False, db_column='clicks',
                                 verbose_name='点击量')
    huanqiuid = models.CharField(max_length=50, blank=False, null=False, db_column='huanqiuid',
                                 verbose_name='环球网新闻编号')
    savedate = models.CharField(max_length=19, blank=False, null=False, db_column='savedate',
                                verbose_name='添加时间')

    # 重定义模型类的字符串表示形式方法，默认：模型类实例对象
    # 管理员添加/修改/删除数据等操作后的提示信息
    def __str__(self):
        return self.title  # 新闻标题

    # 模型类的元数据配置类，用于定义模型类的配置选项
    class Meta:
        # 不允许django框架管理模型类的数据库表
        managed = False
        # 模型类映射的数据库表
        db_table = 'tb_news'
        # 模型类名称
        verbose_name = '新闻'
        # 模型类复数名称
        verbose_name_plural = verbose_name


# 基础新闻模型序列化类，继承django rest framework框架serializers.ModelSerializer类
class NewsSerializer(serializers.ModelSerializer):
    # 自定义序列化属性，新闻类型id，将newstype_id重命名为newstypeid
    newstypeid = serializers.IntegerField(source='newstype_id', read_only=True)
    # 自定义序列化属性，新闻图片，django框架自动添加新闻图片的url访问地址前缀，重定义后只保留新闻图片名称
    photo = serializers.CharField(source='photo.name', read_only=True)

    # 序列化类的元数据配置类，用于定义序列化类的配置选项
    class Meta:
        # 指定序列化类关联的模型类
        model = News
        # 序列化的模型类属性，__all__：所有属性
        fields = '__all__'


# 关联查询新闻模型序列化类，继承基础新闻模型序列化类
class NewsJoinSerializer(NewsSerializer):
    # 自定义序列化属性，新闻类型
    newstype = NewstypeSerializer(read_only=True)

    # 序列化类的元数据配置类，用于定义序列化类的配置选项
    class Meta:
        # 指定序列化类关联的模型类
        model = News
        # 序列化的模型类属性，__all__：所有属性
        fields = '__all__'

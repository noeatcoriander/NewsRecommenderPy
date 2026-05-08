from django.db import models
from rest_framework import serializers


# 新闻类型模型类，继承django框架models.Model类
class Newstype(models.Model):
    # AutoField：自动递增属性
    id = models.AutoField(primary_key=True, db_column='id', verbose_name='主键id自增')
    newstypename = models.CharField(max_length=30, blank=False, null=False, db_column='newstypename',
                                    verbose_name='新闻类型名称')

    # 重定义模型类的字符串表示形式方法，默认：模型类实例对象
    # 管理员添加/修改/删除数据等操作后的提示信息
    def __str__(self):
        return self.newstypename  # 新闻类型名称

    # 模型类的元数据配置类，用于定义模型类的配置选项
    class Meta:
        # 不允许django框架管理模型类的数据库表
        managed = False
        # 模型类映射的数据库表
        db_table = 'tb_newstype'
        # 模型类名称
        verbose_name = '新闻类型'
        # 模型类复数名称
        verbose_name_plural = verbose_name


# 新闻类型模型序列化类，继承django rest framework框架serializers.ModelSerializer类
class NewstypeSerializer(serializers.ModelSerializer):
    # 自定义序列化属性，前台兴趣标签修改页面，标记当前用户是否选择了此标签
    flag = serializers.BooleanField(default=False, read_only=True)

    # 序列化类的元数据配置类，用于定义序列化类的配置选项
    class Meta:
        # 指定序列化类关联的模型类
        model = Newstype
        # 序列化的模型类属性，__all__：所有属性
        fields = '__all__'

from django.core import validators
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from rest_framework import serializers

from tool.public_tool import PublicTool


# 用户模型类，继承django框架models.Model类
class User(models.Model):
    # AutoField：自动递增属性
    id = models.AutoField(primary_key=True, db_column='id', verbose_name='主键id自增')
    # unique：用户名唯一
    loginname = models.CharField(unique=True, max_length=30, blank=False, null=False, db_column='loginname',
                                 verbose_name='用户名')
    password = models.CharField(max_length=30, blank=False, null=False, db_column='password', verbose_name='密码')
    # validators：正则表达式校验电话格式
    mobile = models.CharField(validators=[validators.RegexValidator(r'^1[3-9]\d{9}$', '电话格式不正确！')],
                              max_length=11, blank=False, null=False, db_column='mobile', verbose_name='电话')
    # validators：django框架内置校验邮箱格式
    email = models.CharField(validators=[validators.EmailValidator(message='邮箱格式不正确！')], max_length=50,
                             blank=False, null=False, db_column='email', verbose_name='邮箱')
    # upload_to：重命名上传文件，上传文件名唯一
    avatar = models.ImageField(upload_to=PublicTool().reset_filename, blank=False, null=False,
                               db_column='avatar', verbose_name='头像')
    realname = models.CharField(max_length=30, blank=False, null=False, db_column='realname', verbose_name='姓名')
    # validators：django框架内置校验年龄范围（10-90）
    age = models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(90)], blank=False, null=False,
                              db_column='age', verbose_name='年龄')
    # choices：性别可选值（1：男，2：女）
    sex = models.IntegerField(choices=[(1, '男'), (2, '女')], blank=False, null=False, db_column='sex',
                              verbose_name='性别')
    introduction = models.TextField(max_length=2000, blank=False, null=False, db_column='introduction',
                                    verbose_name='个人简介')
    savedate = models.CharField(max_length=19, blank=False, null=False, db_column='savedate',
                                verbose_name='注册时间')

    # 重定义模型类的字符串表示形式方法，默认：模型类实例对象
    # 管理员添加/修改/删除数据等操作后的提示信息
    def __str__(self):
        return self.loginname  # 用户名

    # 模型类的元数据配置类，用于定义模型类的配置选项
    class Meta:
        # 不允许django框架管理模型类的数据库表
        managed = False
        # 模型类映射的数据库表
        db_table = 'tb_user'
        # 模型类名称
        verbose_name = '用户'
        # 模型类复数名称
        verbose_name_plural = verbose_name


# 用户模型序列化类，继承django rest framework框架serializers.ModelSerializer类
class UserSerializer(serializers.ModelSerializer):
    # 自定义序列化属性，用户头像，django框架自动添加用户头像的url访问地址前缀，重定义后只保留用户头像名称
    avatar = serializers.CharField(source='avatar.name', read_only=True)

    # 序列化类的元数据配置类，用于定义序列化类的配置选项
    class Meta:
        # 指定序列化类关联的模型类
        model = User
        # 序列化的模型类属性，__all__：所有属性
        fields = '__all__'

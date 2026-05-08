from app_user.models import User


# 数据分析模型类，继承用户模型类
class Visualdata(User):
    # 模型类的元数据配置类，用于定义模型类的配置选项
    class Meta:
        proxy = True  # 代理模式，不映射数据库表
        # 模型类名称
        verbose_name = '数据分析'
        # 模型类复数名称
        verbose_name_plural = verbose_name

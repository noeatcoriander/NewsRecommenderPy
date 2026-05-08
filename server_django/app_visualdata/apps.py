from django.apps import AppConfig


# 数据分析功能应用类
class AppsConfig(AppConfig):
    name = 'app_visualdata'  # 应用名称
    verbose_name = "数据分析"  # 管理员功能菜单的一级菜单标题

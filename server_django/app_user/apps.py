from django.apps import AppConfig


# 用户功能应用类
class AppsConfig(AppConfig):
    name = 'app_user'  # 应用名称
    verbose_name = '用户管理'  # 管理员功能菜单的一级菜单标题

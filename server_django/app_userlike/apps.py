from django.apps import AppConfig


# 点赞功能应用类
class AppsConfig(AppConfig):
    name = 'app_userlike'  # 应用名称
    verbose_name = '点赞管理'  # 管理员功能菜单的一级菜单标题

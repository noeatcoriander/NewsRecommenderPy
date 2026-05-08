from django.apps import AppConfig


# 浏览功能应用类
class AppsConfig(AppConfig):
    name = 'app_userbrowse'  # 应用名称
    verbose_name = '浏览管理'  # 管理员功能菜单的一级菜单标题

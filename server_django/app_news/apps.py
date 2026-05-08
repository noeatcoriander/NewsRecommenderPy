from django.apps import AppConfig


# 新闻功能应用类
class AppsConfig(AppConfig):
    name = 'app_news'  # 应用名称
    verbose_name = '新闻管理'  # 管理员功能菜单的一级菜单标题

# 重定义django框架管理员站点管理应用，继承django框架管理员站点管理应用，用于修改管理员页面左侧的功能菜单排序规则
from django.contrib.admin import AdminSite
from django.contrib.admin.apps import AdminConfig


# 重定义django框架管理员配置类，继承django框架管理员配置类
class ApplicationAdminConfigure(AdminConfig):
    # 修改管理员站点配置类，默认：django.contrib.admin.sites.AdminSite
    default_site = 'configure.app_admin_site_configure.ApplicationAdminSiteConfigure'


# 重定义django框架管理员站点配置类，继承django框架管理员站点配置类
class ApplicationAdminSiteConfigure(AdminSite):

    def __init__(self):
        from django.contrib.auth.models import User
        # 修改管理员功能菜单的认证和授权菜单中的用户菜单名称，默认：用户
        User._meta.verbose_name_plural = '管理员'

        from django.contrib.auth.models import Group
        # 修改管理员功能菜单的认证和授权菜单中的组菜单名称，默认：组
        Group._meta.verbose_name_plural = '管理员组'
        # 调用父类init方法
        super().__init__()

    # 重定义管理员页面左侧的功能菜单排序规则函数
    def get_app_list(self, request, app_label=None):
        # 管理员页面左侧的功能菜单排序数据对象，dict字典数据类型
        new_menu_order_dict = {
            'app_visualdata': 0,  # 数据分析
            'app_user': 1,  # 用户
            'app_userlabel': 2,  # 兴趣标签
            'app_news': 3,  # 新闻
            'app_newstype': 4,  # 新闻类型
            'app_userscore': 5,  # 评分
            'app_userfavor': 6,  # 收藏
            'app_userlike': 7,  # 点赞
            'app_userreview': 8,  # 评论
            'app_userbrowse': 9,  # 浏览
            'auth': 10,  # 认证和授权
        }
        # 获取django框架管理员功能菜单数据对象，dict字典数据类型
        app_dict = self._build_app_dict(request)
        # django框架默认管理员一级菜单排序规则：菜单名称首字符升序排列
        # app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        # 修改菜单排序规则，按照自定义菜单排序数据对象升序排列
        app_list = sorted(app_dict.values(), key=lambda x: new_menu_order_dict[x['app_label']])
        # django框架默认管理员二级菜单排序规则：菜单名称首字符升序排列
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])
        return app_list

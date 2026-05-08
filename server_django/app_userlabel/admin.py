from django.contrib import admin

from app_userlabel.models import Userlabel
from tool.public_tool import PublicTool


# 管理员兴趣标签管理类，继承django框架的admin.ModelAdmin类，重写方法和属性定制管理界面
@admin.register(Userlabel)  # 使用django框架的admin装饰器注册兴趣标签模型到管理后台
class UserlabelAdmin(admin.ModelAdmin):
    # 列表页面显示的数据
    list_display = ['user', 'newstype', 'savedate']
    # 列表页面搜索框搜索的数据，用户名（模糊搜索）
    search_fields = ['user__loginname']
    # 列表页面过滤器过滤的数据，新闻类型查询
    list_filter = ('newstype',)
    # 列表页面分页，每页数量
    list_per_page = PublicTool.PAGE_SIZE_ADMIN
    # 添加/修改页面显示的数据
    fields = ['user', 'newstype', 'savedate']

    # 禁用添加功能
    def has_add_permission(self, request):
        return False

    # 禁用修改功能
    def has_change_permission(self, request, obj=None):
        return False

from django.contrib import admin

from app_newstype.models import Newstype
from tool.public_tool import PublicTool


# 管理员新闻类型管理类，继承django框架的admin.ModelAdmin类，重写方法和属性定制管理界面
@admin.register(Newstype)  # 使用django框架的admin装饰器注册新闻类型模型到管理后台
class NewstypeAdmin(admin.ModelAdmin):
    # 列表页面显示的数据
    list_display = ['newstypename']
    # 列表页面搜索框搜索的数据，新闻类型名称（模糊搜索）
    search_fields = ['newstypename']
    # 列表页面分页，每页数量
    list_per_page = PublicTool.PAGE_SIZE_ADMIN
    # 添加/修改页面显示的数据
    fields = ['newstypename']

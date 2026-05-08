from django.contrib import admin

from app_userreview.models import Userreview
from tool.public_tool import PublicTool


# 管理员评论管理类，继承django框架的admin.ModelAdmin类，重写方法和属性定制管理界面
@admin.register(Userreview)  # 使用django框架的admin装饰器注册评论模型到管理后台
class UserreviewAdmin(admin.ModelAdmin):
    # 列表页面显示的数据
    list_display = ['user', 'news', 'showIntroduction', 'savedate']
    # 列表页面搜索框搜索的数据，用户名、新闻标题（模糊搜索）
    search_fields = ['user__loginname', 'news__title']
    # 列表页面关联外键查询的数据，用户、新闻，默认关联查询所有外键及所有外键的外键
    list_select_related = ['user', 'news']
    # 列表页面分页，每页数量
    list_per_page = PublicTool.PAGE_SIZE_ADMIN
    # 添加/修改页面显示的数据
    fields = ['user', 'news', 'introduction', 'savedate']

    # 列表页面的格式化数据方法，评论内容
    def showIntroduction(self, obj):
        if len(str(obj.introduction)) > 50:
            # 截取评论内容字符串
            return '{}...'.format(str(obj.introduction)[:50])
        else:
            return str(obj.introduction)

    # 列表页面的格式化数据标题，评论内容
    showIntroduction.short_description = '评论内容'

    # 禁用添加功能
    def has_add_permission(self, request):
        return False

    # 禁用修改功能
    def has_change_permission(self, request, obj=None):
        return False

    # 重定义列表页面的查询方法
    def get_queryset(self, request):
        # 调用父类的查询方法，同时添加defer()方法，即不查询新闻内容，提高查询效率
        return super().get_queryset(request).defer('news__introduction')

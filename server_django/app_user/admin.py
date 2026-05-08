from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from app_user.models import User
from tool.public_tool import PublicTool


# 管理员用户管理类，继承django框架的admin.ModelAdmin类，重写方法和属性定制管理界面
@admin.register(User)  # 使用django框架的admin装饰器注册用户模型到管理后台
class UserAdmin(admin.ModelAdmin):
    # 列表页面显示的数据
    list_display = ['loginname', 'realname', 'mobile', 'email', 'sex', 'savedate']
    # 列表页面搜索框搜索的数据，用户名、电话、邮箱（模糊搜索）
    search_fields = ['loginname', 'mobile', 'email']
    # 列表页面过滤器过滤的数据，用户性别查询
    list_filter = ('sex',)
    # 列表页面动作集合添加的功能，重置密码
    actions = ['resetPassword']
    # 列表页面分页，每页数量
    list_per_page = PublicTool.PAGE_SIZE_ADMIN
    # 添加/修改页面显示的数据
    fields = ['loginname', 'showAvatar', 'realname', 'mobile', 'email',
              'sex', 'age', 'introduction', 'savedate']

    # 添加/修改页面的格式化数据方法，用户头像预览
    def showAvatar(self, obj):
        # 判断用户头像是否存在
        if obj and obj.avatar and obj.avatar.url:  # 存在
            # 安全返回用户头像html代码
            return mark_safe('<img src="%s" width="100px"/>' % obj.avatar.url)
        return '-'

    # 添加/修改页面的格式化数据标题，用户头像预览
    showAvatar.short_description = '用户头像预览'

    # 列表页面动作集合添加的功能方法，重置密码
    def resetPassword(self, request, queryset):
        # 更新用户密码为默认密码
        queryset.update(password=PublicTool.DEFAULT_PASSWORD)
        # 操作提示消息
        messages.success(request, '操作成功！初始密码：%s' % PublicTool.DEFAULT_PASSWORD)

    # 列表页面动作集合添加的功能标题，重置密码
    resetPassword.short_description = '重置密码'

    # 禁用添加功能
    def has_add_permission(self, request):
        return False

    # 禁用修改功能
    def has_change_permission(self, request, obj=None):
        return False

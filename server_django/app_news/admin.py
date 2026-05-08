from django.contrib import admin
from django.utils.safestring import mark_safe

from app_news.models import News
from tool.public_tool import PublicTool


# 管理员新闻管理类，继承django框架的admin.ModelAdmin类，重写方法和属性定制管理界面
@admin.register(News)  # 使用django框架的admin装饰器注册新闻模型到管理后台
class NewsAdmin(admin.ModelAdmin):
    # 列表页面显示的数据
    list_display = ['title', 'newstype', 'clicks', 'savedate']
    # 列表页面搜索框搜索的数据，新闻标题（模糊搜索）
    search_fields = ['title']
    # 列表页面过滤器过滤的数据，新闻类型查询
    list_filter = ('newstype__newstypename',)
    # 列表页面分页，每页数量
    list_per_page = PublicTool.PAGE_SIZE_ADMIN
    # 添加/修改页面显示的数据
    fields = ['title', 'newstype', 'showPhoto', 'photo', 'newssource', 'introduction']
    # 添加/修改页面的只读数据/格式化数据，新闻图片预览
    readonly_fields = ['showPhoto']

    # 添加/修改页面的格式化数据方法，新闻图片预览
    def showPhoto(self, obj):
        # 判断新闻图片是否存在
        if obj and obj.photo and obj.photo.url:  # 存在
            # 安全返回新闻图片的html代码
            return mark_safe('<img src="%s" width="100px"/>' % obj.photo.url)
        return '-'

    # 添加/修改页面的格式化数据标题，新闻图片预览
    showPhoto.short_description = '新闻图片预览'

    # 重定义添加/修改方法
    def save_model(self, request, obj, form, change):
        if not change:  # 添加
            obj.savedate = PublicTool().getCurrentTime()  # 添加时间
        # 调用父类添加/修改方法
        super().save_model(request, obj, form, change)

    # 重定义列表页面的查询方法
    def get_queryset(self, request):
        # 调用父类的查询方法，同时添加defer()方法，即不查询新闻内容，提高查询效率
        return super().get_queryset(request).defer('introduction')

    # django-admin媒体文件配置类
    # 用于在管理员后台引入自定义的css和javascript文件
    class Media:
        # 后台管理员新闻添加/修改页面，新闻内容wangeditor富文本框css配置
        css = {
            # wangeditor富文本框样式文件
            'all': ('/static/wangeditor/css/style.css',)
        }
        # 后台管理员新闻添加/修改页面，新闻内容wangeditor富文本框js配置
        js = (
            # wangeditor富文本框js文件
            '/static/wangeditor/index.js',
            # wangeditor富文本框自定义js文件
            '/static/wangeditor/config.js',
        )

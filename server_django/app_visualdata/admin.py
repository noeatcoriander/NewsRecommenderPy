from django.contrib import admin

from app_visualdata.models import Visualdata
from tool.sql_tool import SQLSelectTool


# 管理员数据分析管理类，继承django框架的admin.ModelAdmin类，重写方法和属性定制管理界面
@admin.register(Visualdata)  # 使用django框架的admin装饰器注册数据分析模型到管理后台
class VisualdataAdmin(admin.ModelAdmin):
    # 重定义数据分析模板页面
    change_list_template = 'admin/visualdata.html'

    # 重定义数据分析视图函数
    def changelist_view(self, request, extra_context=None):
        # 数据分析：新闻浏览Top30
        # count()：mysql内置聚合函数查询数量
        # group by：分组，新闻id
        # order by：排序，浏览量降序、新闻id降序
        sql = '''
            select b.id, b.title, count(b.id) as browseCount
            from tb_userbrowse h
            left join tb_news b on b.id = h.newsid
            group by b.id
            order by browseCount desc, b.id desc
            limit 0, 30
        '''
        # 查询
        newsAnalysisByBrowse = SQLSelectTool().select_all(sql)

        # 数据分析：新闻评分Top30
        # avg()：mysql内置聚合函数查询平均分
        # round()：mysql内置函数将数据转数字格式并保留一位小数
        # count()：mysql内置聚合函数查询数量
        # cast()：mysql内置函数数据转字符串格式
        # group by：分组，新闻id
        # order by：排序，平均分降序、评分量降序、新闻id降序
        sql = '''
            select b.id, b.title, cast(round(avg(score), 1) as char(10)) as scoreAvg, count(b.id) as scoreCount
            from tb_userscore r
            left join tb_news b on b.id = r.newsid
            group by b.id
            order by round(avg(score), 1) desc, scoreCount desc, b.id desc
            limit 0, 30
        '''
        # 查询
        newsAnalysisByScore = SQLSelectTool().select_all(sql)

        # 数据分析：兴趣标签
        # count()：mysql内置聚合函数查询数量
        # group by：分组，新闻类型id
        sql = '''
            select t.*, count(t.id) as labelCount
            from tb_userlabel b
            left join tb_newstype t on t.id = b.newstypeid
            group by t.id
        '''
        # 查询
        newstypeAnalysisByLabel = SQLSelectTool().select_all(sql)

        # 获取response对象
        response = super().changelist_view(request, extra_context=extra_context)
        # 返回前端的数据
        response.context_data['newsAnalysisByBrowse'] = newsAnalysisByBrowse
        response.context_data['newsAnalysisByScore'] = newsAnalysisByScore
        response.context_data['newstypeAnalysisByLabel'] = newstypeAnalysisByLabel
        return response

    # 禁用添加功能
    def has_add_permission(self, request):
        return False

    # 禁用修改功能
    def has_change_permission(self, request, obj=None):
        return False

    # 禁用删除功能
    def has_delete_permission(self, request, obj=None):
        return False

from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse

from app_userbrowse.models import Userbrowse, UserbrowseJoinSerializer
from configure.base_view_configure import BaseView
from tool.public_tool import PublicTool


# 用户浏览视图类，继承基础视图类
class UserbrowseView(BaseView):

    # 当前登录用户的浏览列表视图函数，get请求方式
    def get(self, request):
        page_num = request.query_params.get('pageNum', 1)  # 分页，获取当前页数
        page_size = request.query_params.get('pageSize', PublicTool.PAGE_SIZE_USER)  # 分页，获取每页条数
        # 获取当前登录用户id
        current_userid = self.get_current_user_id(request)
        # 查询当前登录用户的浏览列表，关联查询用户、新闻，id降序排列
        userbrowse_list = Userbrowse.objects.select_related('user', 'news').filter(user_id=current_userid). \
            order_by('-id')
        # 创建django框架分页器对象，对浏览列表进行分页
        paginator = Paginator(userbrowse_list, page_size)
        try:
            # 获取当前页数的页面数据对象
            pagebean = paginator.page(page_num)
        except EmptyPage:
            # 异常处理，当请求的页数不存在时，返回最后一页
            pagebean = paginator.page(paginator.num_pages)
        # 返回前端的数据
        # 分页数据序列化
        self.set_serializer_pagebean(pagebean, UserbrowseJoinSerializer)
        return JsonResponse(self.get_return_data())

    # 删除浏览视图函数，delete请求方式
    def delete(self, request):
        # 根据主键列表批量删除数据
        ids = request.data  # 获取浏览id主键list列表
        if ids and len(ids) > 0:
            # 获取当前登录用户id
            current_userid = self.get_current_user_id(request)
            # 遍历
            for _id in ids:
                if _id and _id != '':
                    # 删除，删除参数：当前登录用户id、浏览id
                    Userbrowse.objects.filter(user_id=current_userid, id=_id).delete()
            self.success = 1  # 操作成功
        # 返回前端的数据
        return JsonResponse(self.get_return_data())

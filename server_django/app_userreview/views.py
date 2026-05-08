from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse

from app_news.models import News
from app_userreview.models import Userreview, UserreviewJoinSerializer
from configure.base_view_configure import BaseView
from tool.public_tool import PublicTool


# 用户评论列表视图类，继承基础视图类
class UserreviewListView(BaseView):

    # 当前登录用户的评论列表视图函数，get请求方式
    def get(self, request):
        page_num = request.query_params.get('pageNum', 1)  # 分页，获取当前页数
        page_size = request.query_params.get('pageSize', PublicTool.PAGE_SIZE_USER)  # 分页，获取每页条数
        # 获取当前登录用户id
        current_userid = self.get_current_user_id(request)
        # 查询当前登录用户的评论列表，关联查询用户、新闻，id降序排列
        userreview_list = Userreview.objects.select_related('user', 'news').filter(user_id=current_userid). \
            order_by('-id')
        # 创建django框架分页器对象，对评论列表进行分页
        paginator = Paginator(userreview_list, page_size)
        try:
            # 获取当前页数的页面数据对象
            pagebean = paginator.page(page_num)
        except EmptyPage:
            # 异常处理，当请求的页数不存在时，返回最后一页
            pagebean = paginator.page(paginator.num_pages)
        # 返回前端的数据
        # 分页数据序列化
        self.set_serializer_pagebean(pagebean, UserreviewJoinSerializer)
        return JsonResponse(self.get_return_data())


# 新闻评论列表视图类，继承基础视图类
class UserreviewNewsView(BaseView):

    # 当前新闻的评论列表视图函数，get请求方式
    def get(self, request):
        page_num = request.query_params.get('pageNum', 1)  # 分页，获取当前页数
        page_size = request.query_params.get('pageSize', PublicTool.PAGE_SIZE_USER)  # 分页，获取每页条数
        newsid = request.query_params.get('newsid')  # 获取新闻id
        # 判断新闻id是否为空
        if newsid and newsid != '':
            # 查询新闻，查询参数：新闻id
            news = News.objects.filter(id=newsid).first()
            if news:
                # 查询当前新闻的评论列表，关联查询用户、新闻，id降序排列
                userreview_list = Userreview.objects.select_related('user', 'news'). \
                    filter(news_id=newsid).order_by('-id')
                # 创建django框架分页器对象，对评论列表进行分页
                paginator = Paginator(userreview_list, page_size)
                try:
                    # 获取当前页数的页面数据对象
                    pagebean = paginator.page(page_num)
                except EmptyPage:
                    # 异常处理，当请求的页数不存在时，返回最后一页
                    pagebean = paginator.page(paginator.num_pages)
                # 返回前端的数据
                # 分页数据序列化
                self.set_serializer_pagebean(pagebean, UserreviewJoinSerializer)
        return JsonResponse(self.get_return_data())


# 用户评论视图类，继承基础视图类
class UserreviewView(BaseView):

    # 评论详情视图函数，get请求方式
    def get(self, request):
        userreviewid = request.query_params.get('userreviewid')  # 获取评论id
        # 判断评论id是否为空
        if userreviewid and userreviewid != '':
            # 获取当前登录用户id
            current_userid = self.get_current_user_id(request)
            # 查询当前评论，关联查询用户、新闻，查询参数：当前登录用户id、评论id
            userreview = Userreview.objects.select_related('user', 'news'). \
                filter(user_id=current_userid, id=userreviewid).first()
            # 返回前端的数据
            self.result_data_dict['userreview'] = UserreviewJoinSerializer(userreview).data
        return JsonResponse(self.get_return_data())

    # 添加或修改评论视图函数，post请求方式
    def post(self, request):
        userreviewid = request.data.get('id')  # 获取评论id
        newsid = request.data.get('newsid')  # 获取新闻id
        introduction = request.data.get('introduction')  # 获取评论内容
        # 获取当前登录用户id
        current_userid = self.get_current_user_id(request)
        # 判断评论id是否为空
        if userreviewid and userreviewid != '':
            # 查询当前评论，查询参数：当前登录用户id、评论id
            userreview = Userreview.objects.filter(user_id=current_userid, id=userreviewid).first()
            if userreview:
                userreview.introduction = introduction  # 评论内容
                userreview.save(update_fields=['introduction'])  # 修改
                self.success = 1  # 操作成功
        else:
            # 判断新闻id是否为空
            if newsid and newsid != '':
                # 创建评论模型类实例对象
                userreview = Userreview()
                userreview.user_id = current_userid  # 用户id
                userreview.news_id = newsid  # 新闻id
                userreview.introduction = introduction  # 评论内容
                userreview.savedate = PublicTool().getCurrentTime()  # 评论时间
                userreview.save()  # 添加
                self.success = 1  # 操作成功
        # 返回前端的数据
        return JsonResponse(self.get_return_data())

    # 删除评论视图函数，delete请求方式
    def delete(self, request):
        # 根据主键列表批量删除数据
        ids = request.data  # 获取评论id主键list列表
        if ids and len(ids) > 0:
            # 获取当前登录用户id
            current_userid = self.get_current_user_id(request)
            # 遍历
            for _id in ids:
                if _id and _id != '':
                    # 删除，删除参数：当前登录用户id、评论id
                    Userreview.objects.filter(user_id=current_userid, id=_id).delete()
            self.success = 1  # 操作成功
        # 返回前端的数据
        return JsonResponse(self.get_return_data())

from django.http import JsonResponse

from app_newstype.models import Newstype, NewstypeSerializer
from app_user.models import User
from app_userlabel.models import Userlabel
from configure.base_view_configure import BaseView
from tool.public_tool import PublicTool


# 兴趣标签视图类，继承基础视图类
class UserlabelView(BaseView):

    # 当前登录用户的兴趣标签列表视图函数，get请求方式
    def get(self, request):
        # 获取当前登录用户id
        current_userid = self.get_current_user_id(request)
        # 查询当前登录用户的兴趣标签列表，查询参数：当前登录用户id，id降序排列
        userlabel_list = Userlabel.objects.filter(user_id=current_userid).order_by('-id')
        # 查询所有新闻类型，id降序排列
        newstype_list = Newstype.objects.all().order_by('-id')
        # 遍历新闻类型
        for newstype in newstype_list:
            # 遍历当前登录用户选择的兴趣标签列表
            for userlabel in userlabel_list:
                if newstype.id == userlabel.newstype_id:
                    newstype.flag = True  # 添加标记，设置此兴趣标签已被选择
                    break
        # 返回前端的数据
        self.result_data_dict['newstypeList'] = NewstypeSerializer(newstype_list, many=True).data
        return JsonResponse(self.get_return_data())

    # 保存用户登录时选择的兴趣标签视图函数，post请求方式
    def post(self, request):
        userid = request.data.get('userid')  # 获取当前登录用户id
        newstypeid_list = request.data.get('newstypeidList')  # 获取选择的兴趣标签列表（新闻类型id列表）
        # 查询当前登录用户，查询参数：当前登录用户id
        user = User.objects.filter(id=userid).first()
        # 判断用户是否为空
        if user:
            # 判断兴趣标签是否已存在，如果存在则删除，并重新添加
            # 删除当前登录用户的兴趣标签
            Userlabel.objects.filter(user_id=userid).delete()
            # 添加新兴趣标签
            # 遍历兴趣标签列表
            for newstypeid in newstypeid_list:
                # 创建兴趣标签模型类实例对象
                userlabel = Userlabel()
                userlabel.user_id = userid  # 用户id
                userlabel.newstype_id = newstypeid  # 新闻类型id
                userlabel.savedate = PublicTool().getCurrentTime()  # 添加时间
                userlabel.save()  # 添加
            self.success = 1  # 操作成功
        return JsonResponse(self.get_return_data())


# 兴趣标签修改视图类，继承基础视图类
class UserlabelUpdateView(BaseView):

    # 修改兴趣标签视图函数，post请求方式
    def post(self, request):
        # 先删除原兴趣标签，再添加新兴趣标签
        newstypeid_list = request.data  # 获取兴趣标签列表（新闻类型id列表）
        # 判断兴趣标签列表是否为空
        if newstypeid_list and len(newstypeid_list) > 0:
            # 获取当前登录用户id
            current_userid = self.get_current_user_id(request)
            # 删除当前登录用户的兴趣标签
            Userlabel.objects.filter(user_id=current_userid).delete()
            # 添加新兴趣标签
            # 遍历兴趣标签列表
            for newstypeid in newstypeid_list:
                # 创建兴趣标签模型类实例对象
                userlabel = Userlabel()
                userlabel.user_id = current_userid  # 用户id
                userlabel.newstype_id = newstypeid  # 新闻类型id
                userlabel.savedate = PublicTool().getCurrentTime()  # 添加时间
                userlabel.save()  # 添加
            self.success = 1  # 操作成功
        # 返回前端的数据
        return JsonResponse(self.get_return_data())

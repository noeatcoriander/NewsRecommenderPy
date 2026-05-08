from rest_framework.views import APIView


# 基础视图类，继承django rest framework框架的APIView类，是所有视图的父类，用于封装公共方法和属性
# 子视图类可以继承此类，复用通用功能：获取当前登录用户id、定义返回结果等
class BaseView(APIView):

    def __init__(self, *args, **kwargs):
        # 调用父类的init方法
        super().__init__(*args, **kwargs)
        # 前端异步请求返回的操作结果
        # success <= 0：操作失败，success > 0：操作成功
        self.success = 0
        # 前端异步请求返回的提示信息
        self.message = None
        # 前端异步请求返回的数据，字典数据类型
        self.result_data_dict = dict()

    # 获取前端异步请求返回的数据，字典数据类型
    def get_return_data(self):
        self.result_data_dict.update({'success': self.success, 'message': self.message})
        return self.result_data_dict

    # 分页数据序列化，pagebean：django框架分页对象，serializer_class：分页数据序列化对象
    def set_serializer_pagebean(self, pagebean, serializer_class):
        # 返回前端的分页数据
        pagebean_dict = {
            'pageNum': pagebean.number,  # 当前页数
            'pageSize': pagebean.paginator.per_page,  # 每页条数
            'total': pagebean.paginator.count,  # 数据总量
            'list': serializer_class(pagebean.object_list, many=True).data  # 数据序列化，列表数据类型
        }
        # 返回前端的数据
        self.result_data_dict['pageBean'] = pagebean_dict

    # 获取当前登录用户id
    def get_current_user_id(self, request):
        if hasattr(request, 'current_user'):
            # 返回request请求对象中的当前登录用户id
            return request.current_user
        else:
            return None

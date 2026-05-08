import os

from django.db.models import Q
from django.http import JsonResponse
from rest_framework_jwt.settings import api_settings

from app_newstype.models import Newstype, NewstypeSerializer
from app_user.models import User, UserSerializer
from app_userlabel.models import Userlabel
from configure.base_view_configure import BaseView
from server_django import settings
from tool.public_tool import PublicTool


# 用户登录视图类，继承基础视图类
class UserLoginView(BaseView):

    # 用户登录视图函数，post请求方式
    def post(self, request):
        # 用户可根据用户名/电话/邮箱+密码实现登录
        loginname = request.data.get('loginname')  # 获取登录账号
        password = request.data.get('password')  # 获取登录密码
        # 查询登录用户
        # 查询参数：登录账号（用户名、电话、邮箱），或条件查询，登录密码
        # django框架内置查询对象Q实现或条件查询
        user = User.objects.filter(Q(loginname=loginname) | Q(mobile=loginname) | Q(email=loginname),
                                   password=password).first()
        if not user:  # 登录账号或密码错误
            self.message = '登录账号或密码错误！'
        else:  # 登录成功
            self.success = 1  # 登录成功
            self.message = '登录成功！'
            # 生成jwt token
            # 获取jwt的负载对象，保存用户id、用户角色、签发时间、过期时间等数据，json格式
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            # 保存登录用户信息
            user.username = user.loginname  # jwt应用要求用户必须有username属性
            payload = jwt_payload_handler(user)
            # 保存用户id、用户角色
            payload.update({'roleid': user.id, 'role': 'user'})
            # 获取jwt的编码处理器函数
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            # 生成token
            token = jwt_encode_handler(payload)
            print('登录用户token：' + token)
            # 返回前端的数据，token
            self.result_data_dict['token'] = token
            user.password = ''  # 删除密码
            # 返回前端的数据，登录用户信息
            self.result_data_dict['user'] = UserSerializer(user).data
            # 查询兴趣标签，判断用户是否已选择了兴趣标签
            # 查询参数：用户id
            userlabel_list = Userlabel.objects.filter(user_id=user.id)
            if userlabel_list is None or len(userlabel_list) == 0:
                # 用户未选择标签
                # 查询所有新闻类型，id降序排列
                newstype_list = Newstype.objects.all().order_by('-id')
                # 返回前端的数据，新闻类型列表
                self.result_data_dict['newstypeList'] = NewstypeSerializer(newstype_list, many=True).data
        return JsonResponse(self.get_return_data())  # 返回前端的数据


# 用户注册视图类，继承基础视图类
class UserRegisterView(BaseView):

    # 用户注册视图函数，post请求方式
    def post(self, request):
        # 注册用户的用户名、电话唯一
        loginname = request.data.get('loginname')  # 获取用户名
        mobile = request.data.get('mobile')  # 获取电话
        password = request.data.get('password')  # 获取密码
        # 查询判断用户名是否已被注册，查询参数：用户名
        user = User.objects.filter(loginname=loginname).first()
        if user:  # 注册失败
            self.message = '用户名已被注册！'
        else:
            # 查询判断电话是否已被注册，查询参数：电话
            user = User.objects.filter(mobile=mobile).first()
            if user:  # 注册失败
                self.message = '电话已被注册！'
            else:
                user = User()  # 创建用户模型类实例对象
                user.loginname = loginname  # 用户名
                user.mobile = mobile  # 电话
                user.password = password  # 密码
                user.avatar = PublicTool.DEFAULT_AVATAR_USER  # 用户默认头像
                user.savedate = PublicTool().getCurrentTime()  # 注册时间
                user.save()  # 添加
                self.success = 1  # 注册成功
                self.message = '注册成功！'
        return JsonResponse(self.get_return_data())  # 返回前端的数据


# 用户忘记密码视图类，继承基础视图类
class UserForgetPasswordView(BaseView):

    # 用户忘记密码视图函数，post请求方式
    def post(self, request):
        # 根据用户名、电话，重置密码
        loginname = request.data.get('loginname')  # 获取用户名
        mobile = request.data.get('mobile')  # 获取电话
        # 查询用户，查询参数：用户名、电话
        user = User.objects.filter(loginname=loginname, mobile=mobile).first()
        if user:
            # 重置用户密码
            user.password = PublicTool.DEFAULT_PASSWORD  # 初始密码
            user.save(update_fields=['password'])  # 修改
            self.success = 1  # 操作成功
            self.message = '操作成功！初始密码：' + PublicTool.DEFAULT_PASSWORD
        else:
            self.message = '操作失败！用户信息不正确！'
        return JsonResponse(self.get_return_data())  # 返回前端的数据


# 用户文件上传视图类，继承基础视图类
class UserUploadView(BaseView):

    # 用户文件上传视图函数，post请求方式
    def post(self, request):
        try:
            file = request.FILES.get('file')  # 获取上传文件对象
            filename = file.name  # 获取上传文件名：文件名.文件格式
            print('上传文件名：' + filename)
            fileType = os.path.splitext(filename)[1]  # 获取上传文件格式，.jpg
            # 重命名上传文件，上传文件名唯一：当前时间_六位随机数.文件格式
            new_filename = PublicTool().getCurrentTimeRandom() + fileType
            print('重命名上传文件：' + new_filename)
            # 上传文件的保存路径
            filepath = os.path.join(settings.MEDIA_ROOT, new_filename)
            # 保存上传文件到文件上传文件夹
            with open(filepath, 'wb') as f:
                for line in file:
                    f.write(line)
            self.success = 1  # 上传成功
            # 返回前端的数据，上传文件新名称
            self.result_data_dict['newFileName'] = new_filename
        except Exception as e:
            print('文件上传失败！')
            print(e)
            self.message = '上传失败！'
        return JsonResponse(self.get_return_data())  # 返回前端的数据

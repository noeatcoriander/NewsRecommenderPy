from django.http import JsonResponse

from app_user.models import User, UserSerializer
from configure.base_view_configure import BaseView


# 用户视图类，继承基础视图类
class UserView(BaseView):

    # 用户详情视图函数，get请求方式
    def get(self, request):
        # 获取当前登录用户id
        current_userid = self.get_current_user_id(request)
        # 查询当前登录用户，查询参数：用户id
        user = User.objects.filter(id=current_userid).first()
        # 返回前端的数据
        self.result_data_dict['user'] = UserSerializer(user).data
        return JsonResponse(self.get_return_data())

    # 修改用户信息视图函数，put请求方式
    def put(self, request):
        # 用户的用户名、电话、邮箱唯一
        loginname = request.data.get('loginname')  # 获取用户名
        avatar = request.data.get('avatar')  # 获取头像
        realname = request.data.get('realname')  # 获取姓名
        mobile = request.data.get('mobile')  # 获取电话
        email = request.data.get('email')  # 获取邮箱
        sex = request.data.get('sex')  # 获取性别
        age = request.data.get('age')  # 获取年龄
        introduction = request.data.get('introduction')  # 获取个人简介
        # 获取当前登录用户id
        current_userid = self.get_current_user_id(request)
        # 查询判断用户名是否已存在，查询参数：用户名，exclude过滤查询参数：当前登录用户id
        user = User.objects.filter(loginname=loginname).exclude(id=current_userid).first()
        if user:  # 用户名已存在
            self.message = '用户名已存在！'
        else:
            # 查询判断电话是否已存在，查询参数：电话，exclude过滤查询参数：当前登录用户id
            user = User.objects.filter(mobile=mobile).exclude(id=current_userid).first()
            if user:  # 电话已存在
                self.message = '电话已存在！'
            else:
                # 查询判断邮箱是否已存在，查询参数：邮箱，exclude过滤查询参数：当前登录用户id
                user = User.objects.filter(email=email).exclude(id=current_userid).first()
                if user:  # 邮箱已存在
                    self.message = '邮箱已存在！'
                else:
                    # 查询当前登录用户，查询参数：当前登录用户id
                    user = User.objects.filter(id=current_userid).first()
                    if user:
                        user.loginname = loginname  # 用户名
                        user.avatar = avatar  # 头像
                        user.realname = realname  # 姓名
                        user.mobile = mobile  # 电话
                        user.email = email  # 邮箱
                        user.sex = sex  # 性别
                        user.age = age  # 年龄
                        user.introduction = introduction  # 个人简介
                        user.save()  # 修改
                        self.success = 1  # 操作成功
                        user.password = ''  # 删除密码
                        # 返回前端的数据，用户信息
                        self.result_data_dict['user'] = UserSerializer(user).data
        # 返回前端的数据
        return JsonResponse(self.get_return_data())

    # 修改用户密码视图函数，post请求方式
    def post(self, request):
        old_password = request.data.get('oldPassword')  # 获取原密码
        password = request.data.get('password')  # 获取新密码
        # 获取当前登录用户id
        current_userid = self.get_current_user_id(request)
        # 查询当前登录用户，查询参数：当前登录用户id
        user = User.objects.filter(id=current_userid).first()
        if user:
            # 判断原密码是否正确
            if user.password == old_password:
                self.success = User.objects.filter(id=current_userid).update(password=password)  # 修改为新密码
                if self.success > 0:
                    self.message = '操作成功！请重新登陆！'
            else:
                self.message = '原密码不正确！'
        # 返回前端的数据
        return JsonResponse(self.get_return_data())

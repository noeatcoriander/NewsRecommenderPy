from django.urls import path

from app_public.views import UserLoginView, UserForgetPasswordView, \
    UserRegisterView, UserUploadView

# 用户公共功能应用路由
urlpatterns = [
    path('doLogin', UserLoginView.as_view()),  # 用户登录
    path('doRegister', UserRegisterView.as_view()),  # 用户注册
    path('doForgetPassword', UserForgetPasswordView.as_view()),  # 忘记密码
    path('doUpload', UserUploadView.as_view()),  # 文件上传
]

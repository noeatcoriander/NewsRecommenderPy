from django.urls import path

from app_user.views import UserView

# 用户功能应用路由
urlpatterns = [
    path('detail', UserView.as_view()),  # 用户详情
    path('doUpdate', UserView.as_view()),  # 修改用户信息
    path('doUpdatePassword', UserView.as_view()),  # 修改用户密码
]

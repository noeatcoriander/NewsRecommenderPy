from django.urls import path

from app_userscore.views import UserscoreView

# 用户评分功能应用路由
urlpatterns = [
    path('list', UserscoreView.as_view()),  # 当前登录用户的评分列表
    path('doUpdate', UserscoreView.as_view()),  # 添加或修改评分
    path('doDelete', UserscoreView.as_view())  # 删除评分
]

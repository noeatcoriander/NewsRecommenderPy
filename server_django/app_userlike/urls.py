from django.urls import path

from app_userlike.views import UserlikeView

# 用户点赞功能应用路由
urlpatterns = [
    path('list', UserlikeView.as_view()),  # 当前登录用户的点赞列表
    path('doUpdate', UserlikeView.as_view()),  # 添加或取消点赞
    path('doDelete', UserlikeView.as_view())  # 删除点赞
]

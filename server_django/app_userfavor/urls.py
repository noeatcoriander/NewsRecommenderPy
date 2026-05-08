from django.urls import path

from app_userfavor.views import UserfavorView

# 用户收藏功能应用路由
urlpatterns = [
    path('list', UserfavorView.as_view()),  # 当前登录用户的收藏列表
    path('doUpdate', UserfavorView.as_view()),  # 添加或取消收藏
    path('doDelete', UserfavorView.as_view())  # 删除收藏
]

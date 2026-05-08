from django.urls import path

from app_userbrowse.views import UserbrowseView

# 用户浏览功能应用路由
urlpatterns = [
    path('list', UserbrowseView.as_view()),  # 当前登录用户的浏览列表
    path('doDelete', UserbrowseView.as_view())  # 删除浏览
]

from django.urls import path

from app_userlabel.views import UserlabelView, UserlabelUpdateView

# 兴趣标签功能应用路由
urlpatterns = [
    path('list', UserlabelView.as_view()),  # 当前登录用户的兴趣标签列表
    path('doSave', UserlabelView.as_view()),  # 保存用户登录时选择的兴趣标签
    path('doUpdate', UserlabelUpdateView.as_view()),  # 修改兴趣标签
]

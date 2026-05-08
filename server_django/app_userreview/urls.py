from django.urls import path

from app_userreview.views import UserreviewNewsView, UserreviewListView, UserreviewView

# 用户评论功能应用路由
urlpatterns = [
    path('list', UserreviewListView.as_view()),  # 当前登录用户的评论列表
    path('listByNewsid', UserreviewNewsView.as_view()),  # 当前新闻的评论列表
    path('detail', UserreviewView.as_view()),  # 评论详情
    path('doUpdate', UserreviewView.as_view()),  # 添加或修改评论
    path('doDelete', UserreviewView.as_view()),  # 删除评论
]

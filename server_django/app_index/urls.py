from django.urls import path

from app_index.views import IndexView, IndexRecommendView, \
    IndexTopView, IndexRecomBasedLabelView

# 用户首页功能应用路由
urlpatterns = [
    path('index', IndexView.as_view()),  # 用户首页
    path('recommend', IndexRecommendView.as_view()),  # 用户首页个性化推荐
    path('recommendBasedLabel', IndexRecomBasedLabelView.as_view()),  # 用户首页兴趣标签推荐
    path('top', IndexTopView.as_view()),  # 用户首页新闻排行
]

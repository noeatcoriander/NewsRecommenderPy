from django.urls import path

from app_news.views import NewsListView, NewsDetailAnalysisUserView, \
    NewsDetailAnalysisNewsView, NewsDetailRecommendView, NewsDetailView

# 用户新闻功能应用路由
urlpatterns = [
    path('list', NewsListView.as_view()),  # 新闻列表
    path('detail', NewsDetailView.as_view()),  # 新闻详情
    path('recommend', NewsDetailRecommendView.as_view()),  # 猜你喜欢
    path('doAnalysisNewsData', NewsDetailAnalysisNewsView.as_view()),  # 新闻数据分析
    path('doAnalysisUserData', NewsDetailAnalysisUserView.as_view()),  # 用户数据分析
]

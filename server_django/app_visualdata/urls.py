from django.urls import path

from app_visualdata.views import AdminWangeditorUploadView

# 后台管理员wangeditor富文本框功能应用路由
urlpatterns = [
    path('public/doEditorUpload', AdminWangeditorUploadView.as_view()),  # 后台管理员wangeditor富文本框文件上传
]

# django框架后端系统主路由配置文件
# vue前端框架请求django后端数据接口url地址：主路由地址 + 具体功能应用的路由地址
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from server_django import settings

# django框架后端系统主路由地址配置列表
urlpatterns = [
    # django框架后端系统用户功能数据接口路由地址以/api/user/开头
    # 用户基础路由地址：用户登录、用户注册、忘记密码、文件上传等数据接口地址
    path('api/user/public/', include('app_public.urls')),
    # 用户首页路由地址
    path('api/user/index/', include('app_index.urls')),
    # 用户新闻路由地址
    path('api/user/news/', include('app_news.urls')),
    # 用户路由地址
    path('api/user/user/', include('app_user.urls')),
    # 兴趣标签路由地址
    path('api/user/userlabel/', include('app_userlabel.urls')),
    # 用户点赞路由地址
    path('api/user/userlike/', include('app_userlike.urls')),
    # 用户收藏路由地址
    path('api/user/userfavor/', include('app_userfavor.urls')),
    # 用户评分路由地址
    path('api/user/userscore/', include('app_userscore.urls')),
    # 用户评论路由地址
    path('api/user/userreview/', include('app_userreview.urls')),
    # 用户浏览路由地址
    path('api/user/userbrowse/', include('app_userbrowse.urls')),
    # django框架后端系统管理员功能路由地址
    path('admin/', admin.site.urls),
    # 后台管理员wangeditor富文本框文件上传路由地址
    path('api/admin/', include('app_visualdata.urls'))
]

# 配置上传文件的路由地址，即指定访问上传文件的路由地址和上传文件的保存路径
# MEDIA_URL：上传文件访问url地址：http://localhost:8000/files/文件名
# MEDIA_ROOT：上传文件保存在files文件夹中
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 后台管理员网页标题及网页标签配置
# 后台管理员网页标签配置
admin.site.site_title = '个性化新闻推荐系统|管理员'
# 后台管理员登录网页的登录框标题及管理员登录后所有网页的头部标题配置
admin.site.site_header = '个性化新闻推荐系统|管理员'
# 后台管理员首页头部标题配置
admin.site.index_title = '首页'

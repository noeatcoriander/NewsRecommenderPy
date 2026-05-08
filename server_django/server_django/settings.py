# django框架后端系统主配置文件
# django框架后端系统通过运行：python manage.py runserver命令启动
# 系统启动时，django框架会先自动读取settings.py中的配置信息，并实现数据库的连接
# django框架默认指定setting.py文件中所有全局变量名英文大写
import datetime
import hashlib
import os
import sys
import time
from pathlib import Path

import jieba
from psutil import net_if_addrs

# django框架后端系统的根路径，绝对路径
BASE_DIR = Path(__file__).resolve().parent.parent

# 加密算法的秘钥（或者叫密码盐）
# 创建django框架后端系统时随机生成秘钥字符串
# django框架默认指定使用hash哈希加密算法
# django框架后端系统中使用数据加密的功能：
# 1、用户身份认证token加密，2、管理员的登录密码加密，3、建立会话时的sessionid加密，4、防止CSRF跨站请求伪造攻击数据加密
# 使用秘钥加密原理：管理员的登录密码加密后的数据保存在数据库管理员表中，
# 当管理员密码相对简单或常见，如果不使用秘钥加密，密码加密后的数据固定，很容易被破解，
# 使用秘钥加密后，会在加密算法加密后的数据的前/中/后加上秘钥，或其他一些操作，增加破解难度。
SECRET_KEY = 'uq8=1366k3x2f^uoqb8sefjm$6k#4d4k%_5_7_sbmn^k@$vw*@'

# django框架后端系统开发模式，默认值：True，即开发测试环境
# 开发测试环境：True，便于查看bug信息，找出bug代码位置
# 生产运行环境：False，避免后端系统敏感数据信息的暴露
DEBUG = True

# 允许访问django框架后端系统数据接口的ip地址，默认值：[]
# 在生产运行环境，即DEBUG = False，ip地址必填
# 配置使用：
# 1、默认值：[]，空列表，仅本机可访问，即127.0.0.1或localhost地址，
# 2、['192.168.0.1', '192.168.0.2']：仅配置的ip可访问，
# 3、['*']：任何ip地址都可访问
ALLOWED_HOSTS = ['*']

# django框架后端系统应用程序
# 创建django框架后端系统时会自动配置以'django.'开头的内置应用程序
# 系统启动时，django框架会自动加载并激活配置的应用程序
INSTALLED_APPS = [
    # 后台管理员界面美化与增强框架：django-simpleui，用于美化管理员页面并扩展功能
    # 安装使用：pip install django-simpleui
    'simpleui',
    # django框架默认核心应用，管理员站点管理，用于自动动态生成管理员页面并实现管理员增删改查功能
    # 'django.contrib.admin',
    # 重定义django.contrib.admin，用于修改管理员页面左侧的功能菜单排序规则
    'configure.app_admin_site_configure.ApplicationAdminConfigure',
    # django框架默认核心应用，管理员权限管理（认证和授权），即不同的管理员可设置不同的功能
    # django框架通过数据库中'auth_'开头的表实现管理员权限管理功能
    'django.contrib.auth',
    # django框架默认核心应用，内容类型，即设置model模型类与系统应用的对应关系，例如：新闻模型类对应news应用模块
    # django框架通过数据库中'django_content_type'表实现内容类型对应关系配置
    'django.contrib.contenttypes',
    # django框架默认核心应用，session会话，即保存管理员登录状态信息
    # django框架通过数据库中'django_session'表保存管理员登录状态信息，主要保存管理员登录状态失效时间，
    # django框架默认设置登录有效时长14天，即14天内不需要登录，14天后登录状态信息失效，需重新登录
    'django.contrib.sessions',
    # django框架默认核心应用，消息管理，即管理员增删改查操作后成功/失败等的提示信息
    'django.contrib.messages',
    # django框架默认核心应用，静态文件管理
    # 静态文件：css、js、字体图标、静态图片等文件，便于在html页面中使用
    # 主要用于管理管理员的静态文件
    'django.contrib.staticfiles',
    # Django REST Framework(DRF)框架应用，用于构建强大的Web API
    # 提供了序列化、视图集、路由器等工具，可快速构建restful风格后端数据接口
    # 安装使用：pip install djangorestframework
    'rest_framework',
    # Django REST Framework JWT框架应用，用于实现用户身份识别token
    # 即实现用户登录状态的验证
    # 安装使用：pip install djangorestframework-jwt
    'rest_framework_jwt',
    # Django CORS Headers框架应用，用于处理跨域请求
    # 即解决前端调用后端api数据接口时的跨域问题
    # 安装使用：pip install django-cors-headers
    'corsheaders',
    # 自定义应用，用户公共功能，用户登录、用户注册、忘记密码、文件上传等
    'app_public.apps.AppsConfig',
    # 自定义应用，用户首页功能
    'app_index.apps.AppsConfig',
    # 自定义应用，新闻功能
    'app_news.apps.AppsConfig',
    # 自定义应用，新闻类型功能
    'app_newstype.apps.AppsConfig',
    # 自定义应用，用户功能
    'app_user.apps.AppsConfig',
    # 自定义应用，兴趣标签功能
    'app_userlabel.apps.AppsConfig',
    # 自定义应用，点赞功能
    'app_userlike.apps.AppsConfig',
    # 自定义应用，收藏功能
    'app_userfavor.apps.AppsConfig',
    # 自定义应用，评分功能
    'app_userscore.apps.AppsConfig',
    # 自定义应用，评论功能
    'app_userreview.apps.AppsConfig',
    # 自定义应用，浏览功能
    'app_userbrowse.apps.AppsConfig',
    # 自定义应用，数据分析功能
    'app_visualdata.apps.AppsConfig',
]

# django-simpleui框架管理员前端配置
# 关闭管理员首页的服务器信息面板
SIMPLEUI_HOME_INFO = False

# 关闭管理员首页的使用分析面板
SIMPLEUI_ANALYSIS = False

# 关闭管理员首页的最近动作记录面板
SIMPLEUI_HOME_ACTION = False

# 使用离线静态资源
# 加载django-simpleui框架的css、js等静态资源，避免从网络下载，提高访问速度和稳定性
SIMPLEUI_STATIC_OFFLINE = True

# 设置django-simpleui框架的主题，即样式文件名
# 样式文件地址：系统python环境\Lib\site-packages\simpleui\static\admin\simpleui-x\theme
SIMPLEUI_DEFAULT_THEME = 'e-green.css'

# 自定义管理员功能菜单图标，django-simpleui框架使用fontawesome图标库
# fontawesome图标库中文官网：https://fontawesome.com.cn/
SIMPLEUI_ICON = {
    '数据分析': 'fa-solid fa-chart-line',
    '新闻管理': 'fa-regular fa-newspaper',
    '新闻': 'fa-regular fa-newspaper',
    '新闻类型管理': 'fa-solid fa-list-ul',
    '新闻类型': 'fa-solid fa-list-ul',
    '用户管理': 'fa-regular fa-user',
    '用户': 'fa-regular fa-user',
    '兴趣标签管理': 'fa-solid fa-tags',
    '兴趣标签': 'fa-solid fa-tags',
    '点赞管理': 'fa-regular fa-thumbs-up',
    '点赞': 'fa-regular fa-thumbs-up',
    '收藏管理': 'fa-regular fa-heart',
    '收藏': 'fa-regular fa-heart',
    '评分管理': 'fa-regular fa-star',
    '评分': 'fa-regular fa-star',
    '评论管理': 'fa-regular fa-comments',
    '评论': 'fa-regular fa-comments',
    '浏览管理': 'fa-regular fa-eye',
    '浏览': 'fa-regular fa-eye',
    '管理员': 'fa-solid fa-user-lock',
    '管理员组': 'fa-solid fa-user-group',
}

# Django REST Framework JWT框架配置
JWT_AUTH = {
    # vue前端发送请求时，在token前加'Bearer '前缀，即token = 'Bearer ' + token
    # 'Bearer '是一种标准的认证方案，即告诉服务端要进行身份认证，其他认证方式：Basic（基础认证）、Digest（摘要认证）等
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    # token有效期，1天
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    # 刷新token有效期，7天，7天内自动刷新token，无需重新登录
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    # token加密秘钥，默认使用django框架的SECRET_KEY
    'JWT_SECRET_KEY': SECRET_KEY,
    # token加密算法，hash算法
    'JWT_ALGORITHM': 'HS256',
}

# django框架中间件
# 中间件指django框架后端系统从接收到前端的请求到返回响应结果，在这个过程中所做的操作
# 前端请求后端数据接口，会从上到下依次执行MIDDLEWARE中的中间件配置，然后调用具体的视图进行业务处理，
# 接着再从下至上依次执行MIDDLEWARE中的中间件配置，最后返回响应结果，即在request请求前后和response响应前后执行。
# 执行过程：前端发送request数据请求-执行中间件-执行view视图-执行中间件-response返回响应结果-前端获取结果数据
MIDDLEWARE = [
    # Django CORS Headers框架处理跨域请求中间件
    'corsheaders.middleware.CorsMiddleware',
    # django框架默认核心中间件，安全中间件
    # 为django框架后端系统提供安全保护功能，设置xss防御的请求头、http协议转https协议等
    'django.middleware.security.SecurityMiddleware',
    # django框架默认核心中间件，session会话中间件，即维护session会话状态
    'django.contrib.sessions.middleware.SessionMiddleware',
    # django框架默认核心中间件，通用中间件，处理前端请求的url地址、自动在前端请求的url地址后加反斜杠等
    'django.middleware.common.CommonMiddleware',
    # django框架默认核心中间件，CSRF跨站请求伪造防御中间件
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # django框架默认核心中间件，认证中间件，request请求对象保存登录的管理员信息，便于在视图中获取当前登录管理员
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # django框架默认核心中间件，消息中间件，管理员增删改查操作后成功/失败等的提示信息
    'django.contrib.messages.middleware.MessageMiddleware',
    # django框架默认核心中间件，点击劫持保护中间件
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 自定义中间件，用户身份认证中间件，通过token验证用户是否登录
    'configure.auth_middleware_configure.AuthMiddlewareConfigure',
]

# Django CORS Headers框架配置
# 用于解决前后端分离架构中的跨域请求问题
# 跨域指浏览器出于安全考虑，限制非同源之间互相请求访问，
# 即http://localhost:5173（前端vue）发送请求到http://localhost:8000（后端django），
# 前端vue与后端django端口号不同，因此是非同源，不能互相访问
# 允许所有域名进行跨域访问
CORS_ORIGIN_ALLOW_ALL = True

# 许跨域请求携带认证信息
CORS_ALLOW_CREDENTIALS = True

# 允许的前端请求方式
CORS_ALLOW_METHODS = (
    'GET', 'POST', 'PUT', 'PATCH', 'DELETE'
)

# django框架后端系统主路由配置文件
ROOT_URLCONF = 'server_django.urls'

# django框架后端系统模版配置
# vue前端系统实现用户功能，django框架内置前端管理系统实现管理员功能（使用vue前端技术）
# 故此配置主要用于实现管理员功能
TEMPLATES = [
    {
        # django框架后端系统模板渲染引擎，默认使用django框架内置的模板渲染引擎
        # 模板渲染引擎用于在html页面中动态显示views.py视图函数中返回的数据
        # 例如：{{ admin.loginname }}代码用于在html中动态显示管理员名，{% if ... %}...{% endif %}代码用于在html中实现条件判断
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 模板存放文件夹，即存放html页面的文件夹路径
        'DIRS': [os.path.join(BASE_DIR, 'htmls')],
        # 允许在具体应用中查找html模板文件
        'APP_DIRS': True,
        # 其他配置
        'OPTIONS': {
            # django框架默认核心上下文处理器，可以在html模板页面中直接调用debug、request、auth、message等django框架内置对象
            'context_processors': [
                # 在html模板页面中调用debug、sql_queries、执行sql时间等django框架内置对象
                'django.template.context_processors.debug',
                # 在html模板页面中调用request请求对象
                'django.template.context_processors.request',
                # 在html模板页面中调用权限验证对象（auth_user、auth_perms等）
                'django.contrib.auth.context_processors.auth',
                # 在html模板页面中调用消息message对象
                'django.contrib.messages.context_processors.messages',
                # 在html模板页面中调用settings.py配置文件的MEDIA_URL数据对象
                'django.template.context_processors.media',
            ],
        },
    },
]

# django框架后端系统wsgi应用配置文件，wsgi.py
# WSGI（Web Server Gateway Interface）：Python Web应用程序与Web服务器之间的标准接口，用于django框架后端系统在服务器上部署运行
# django框架3.0及以上版本增加asgi，ASGI（Asynchronous Server Gateway Interface），asgi.py
# wsgi主要用于http请求的同步数据传输，asgi主要用于http、WebSocket请求的异步数据传输（实时应用和高并发）
WSGI_APPLICATION = 'server_django.wsgi.application'

# django框架后端系统mysql数据库连接配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # mysql连接驱动
        'NAME': 'newsrecommenderpy',  # mysql数据库名称
        'USER': 'root',  # mysql连接用户名
        'PASSWORD': '123456',  # mysql连接密码
        'HOST': '127.0.0.1',  # mysql连接地址
        'PORT': '3306',  # mysql连接端口号
        'OPTIONS': {
            'charset': 'utf8mb4',  # mysql编码
            'use_unicode': True,
        }
    }
}

# django框架后端系统管理员密码校验规则配置
AUTH_PASSWORD_VALIDATORS = [
    {  # 校验管理员密码与当前管理员其他信息的相似性
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {  # 校验管理员密码长度（最少8位）
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {  # 校验管理员密码是否常用
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {  # 校验管理员密码是否是纯数字
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# django框架后端系统语言配置，中文，默认英文：en-us
LANGUAGE_CODE = 'zh-hans'

# django框架后端系统时区配置
TIME_ZONE = 'Asia/Shanghai'

# django框架后端系统语言国际化配置
USE_I18N = True

# django框架后端系统时间、日期、数字等内容格式国际化
USE_L10N = True

# django框架后端系统连接mysql数据库时间类型，默认：True，即UTC时间类型
USE_TZ = False

# django框架后端系统静态文件的访问url地址配置，静态文件：css、js、字体图标、静态图片等文件，http://localhost:8000/static/静态文件
STATIC_URL = '/static/'

# django框架后端系统静态文件的保存地址：static文件夹
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# django框架后端系统访问上传文件的url地址配置，上传文件即用户头像、新闻图片等，上传文件访问url地址：http://localhost:8000/files/文件名
MEDIA_URL = '/files/'

# django框架后端系统上传文件的保存路径，files文件夹
MEDIA_ROOT = os.path.join(BASE_DIR, 'files/')

# django框架后端系统根路径保存在全局字典中
sys.modules['BASE_DIR_NT'] = Path(__file__).resolve().parent

# 预加载jieba词典文件和初始化分词模型
jieba.initialize()

# django框架后端系统日志记录行为配置
LOGGING = {
    'version': 1,  # 版本号
    'disable_existing_loggers': False,  # 保留django框架默认的日志记录器，同时添加自定义配置
    # 日志处理器
    'handlers': {
        # 控制台处理器
        'console': {
            'level': 'DEBUG',  # 日志级别，处理debug及以上级别的日志
            'class': 'logging.StreamHandler',  # 处理器类，控制台输出
        },
    },
    # 日志记录器
    'loggers': {
        # django框架连接mysql数据库的日志记录器
        'django.db.backends': {
            'handlers': ['console'],  # 使用控制台处理器
            'propagate': True,  # 向上传播，日志传递给父记录器
            'level': 'DEBUG',  # 日志级别，处理debug及以上级别的日志
        },
    }
}

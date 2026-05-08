from django.http import JsonResponse
from rest_framework_jwt.settings import api_settings
from rpvputil.common.abstractmiddleware import AbstractMiddleware


# 自定义权限验证中间件类，用于验证用户权限，在执行具体的视图函数前/后执行
# django框架后端系统部分数据接口需用户登录后才能使用，使用jwt技术进行用户身份认证
# 中间件类通过验证前端发送的请求头中的token值是否有效，判断用户是否有操作权限，
# 如果有权限则继续执行视图中的函数，如果没有权限则返回401错误。
# JWT（json web tokens）用户身份认证，使用django_rest_framework_jwt第三方应用
# 一个JWT由三部分组成：Header.Payload.Signature
# Header：头部，保存签名算法和token类型，json格式，例如：{'alg': 'HS256', 'typ': 'JWT'}
# Payload：负载/声明，保存用户id、用户角色、签发时间、过期时间等数据，json格式
# Signature：签名，对前两部分的签名，防止篡改（使用密钥 secretKey 生成）
# 实现原理：
# JWT通过token进行前端和后端的身份认证，token是一个字符串，例如：'abc.def.ghi'，
# 其中abc是加密后的header头部，def是payload数据，
# 前两部分均使用Base64Url技术编码为字符串，前端和后端都可通过Base64Url技术解码获取原数据，
# 前两部分加密后使用.连接，获取未签名的token，例如：unsignedToken = 'abc.def'，
# Signature签名，使用加密算法（例如：HMAC-SHA256哈希加密算法）和秘钥（或者叫密码盐）secret_key将unsignedToken（未签名的token）加密，
# 得到一个字符串，再次使用Base64Url技术编码为字符串，即签名：ghi。最终三个字符串以.连接得到token='abc.def.ghi'。
# 身份认证过程：
# 1、后端将登录成功后的用户信息使用jwt技术生成一个token字符串，并传递到前端；
# 2、前端获取token，可解析出登录用户id、用户角色、签发时间、过期时间等数据；
# 3、用户登录成功后，前端请求后端数据接口，在request请求头中添加token字符串参数；
# 4、后端获取request请求头中的token参数，并与后端重新生成的签名进行对比；
# 5、后端解析出请求头中的token中的header与payload原数据，并重新计算签名signature，对比token中的签名和重新生成的签名，
# 6、如果对比成功，即身份认证成功继续执行业务处理，如果对比失败，即身份认证失败（token无效、token超时等），
# 则返回前端需重新登录。
class AuthMiddlewareConfigure(AbstractMiddleware):
    # 配置不验证的请求地址，以下请求地址不会进行身份验证
    exclude_url_list = list()
    exclude_url_list.append('/api/user/public/doLogin')  # 用户登录
    exclude_url_list.append('/api/user/public/doRegister')  # 用户注册
    exclude_url_list.append('/api/user/public/doForgetPassword')  # 用户忘记密码
    exclude_url_list.append('/api/user/userlabel/doSave')  # 用户登录保存选择的兴趣标签

    # 配置不需要token的请求地址
    # 以下请求地址不需要有效token即可访问，在视图函数中通过判断登录用户id是否存在进行业务处理
    no_token_required_url_list = list()
    no_token_required_url_list.append('/api/user/index/index')  # 用户首页
    no_token_required_url_list.append('/api/user/index/recommend')  # 用户首页推荐新闻
    no_token_required_url_list.append('/api/user/index/top')  # 新闻排行
    no_token_required_url_list.append('/api/user/news/list')  # 新闻列表
    no_token_required_url_list.append('/api/user/news/detail')  # 新闻详情
    no_token_required_url_list.append('/api/user/news/doAnalysisNewsData')  # 新闻详情中的新闻数据分析
    no_token_required_url_list.append('/api/user/news/doAnalysisUserData')  # 新闻详情中的当前登录用户对当前新闻的数据分析
    no_token_required_url_list.append('/api/user/userreview/listByNewsid')  # 新闻详情中的评论列表
    no_token_required_url_list.append('/api/user/news/recommend')  # 新闻详情中的推荐新闻

    # 前置处理方法，在视图函数执行之前被调用
    def process_request(self, request):
        path = request.path  # 获取请求url地址
        # 判断请求地址，只验证以'/api/user/'开头的请求地址，同时过滤不验证的请求地址
        # 即过滤管理员、访问上传文件等的请求地址
        if path.startswith('/api/user/') and path not in self.exclude_url_list:
            # 获取request请求头中的token字符串
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            # 判断token是否存在，同时判断是否以'Bearer '开头
            # vue前端发送请求时，在token前加'Bearer '前缀，即token = 'Bearer ' + token
            # 'Bearer '是一种标准的认证方案，即告诉服务端要进行身份认证，其他认证方式：Basic（基础认证）、Digest（摘要认证）等
            if auth_header.startswith('Bearer '):
                # 提取token字符串，即去掉前缀'Bearer '
                token = auth_header.split(' ')[1]
                try:
                    # 解析并验证token，同时获取token解析后的自定义数据，如果验证失败则抛出异常
                    # 获取jwt的解码处理器函数
                    jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
                    # 获取jwt的负载对象
                    payload = jwt_decode_handler(token)
                    # 获取当前登录用户id
                    userid = payload.get('roleid')
                    # 将当前登录用户id保存在request请求中，便于后期在视图函数中使用
                    request.current_user = userid
                except Exception as e:
                    # 捕获token解析和验证时的异常，即身份认证失败（用户未登录）
                    # 如果当前请求url地址在不需要token的请求url地址列表中，则继续执行
                    if path in self.no_token_required_url_list:
                        # 在request对象中保存token状态，invalid：已失效，vue前端获取response响应头中的token状态并删除无效token
                        request.token_status = 'invalid'
                    else:
                        # token验证失败：token已过期/token无效，返回401错误
                        return JsonResponse({'message': '登录无效！请重新登录！'}, status=401)
            else:
                # 没有token或token格式不正确，返回401错误，401：http状态码，即身份认证失败
                return JsonResponse({'message': '操作失败！请先登录！'}, status=401)

    # 后置处理方法，在视图函数执行之后被调用
    def process_response(self, request, response):
        if hasattr(request, 'token_status'):
            # 在response响应头中保存token状态，invalid：已失效，vue前端获取response响应头中的token状态并删除无效token
            response['token-status'] = request.token_status
        return response

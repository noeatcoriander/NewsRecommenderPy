import os

from django.http import JsonResponse

from configure.base_view_configure import BaseView
from server_django import settings
from tool.public_tool import PublicTool


# 后台管理员wangeditor富文本框文件上传视图类，继承基础视图类
class AdminWangeditorUploadView(BaseView):

    # 后台管理员wangeditor富文本框文件上传视图函数，post请求方式
    def post(self, request):
        errno = 1  # 上传成功标记，0：成功，1：失败
        try:
            file = request.FILES.get('file')  # 获取上传文件对象
            filename = file.name  # 获取上传文件名：文件名.文件格式
            print('上传文件名：' + filename)
            # 获取上传文件格式，.jpg
            file_type = os.path.splitext(filename)[1]
            # 创建允许上传的文件扩展名list列表
            file_type_list = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']
            # 判断文件格式是否正确
            if file_type in file_type_list:
                # 重命名上传文件，上传文件名唯一：当前时间_六位随机数.文件格式
                new_filename = PublicTool().getCurrentTimeRandom() + file_type
                print('重命名上传文件：' + new_filename)
                # 上传文件的保存路径
                filepath = os.path.join(settings.MEDIA_ROOT, new_filename)
                # 保存上传文件到文件上传文件夹
                with open(filepath, 'wb') as f:
                    for line in file:
                        f.write(line)
                # 返回前端的数据，上传文件新名称
                # 前端wangeditor接收的数据格式要求：{errno: 0, data: {url: '/files/文件名称'}}
                self.result_data_dict['data'] = {'url': settings.MEDIA_URL + new_filename}
                errno = 0  # 上传成功
            else:
                self.message = '上传文件格式不正确！'
        except Exception as e:
            print('文件上传失败！')
            print(e)
            self.message = '上传失败！'
        self.result_data_dict['errno'] = errno
        return JsonResponse(self.get_return_data())  # 返回前端的数据

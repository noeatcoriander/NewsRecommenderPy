import os
import random

from rpvputil.util.abstractutil import AbstractUtil


# 基础工具类
class PublicTool(AbstractUtil):
    # 分页，每页数量，当前端没有传递每页数量时使用，前台用户
    PAGE_SIZE_USER = 12

    # 分页，每页数量，当前端没有传递每页数量时使用，后台管理员
    PAGE_SIZE_ADMIN = 12

    # 用户忘记密码或管理员重置用户/管理员密码后的初始密码
    DEFAULT_PASSWORD = '123456'

    # 默认头像图片，前台用户
    DEFAULT_AVATAR_USER = 'avatar.jpg'

    # 重命名上传文件，上传文件名唯一：当前时间_六位随机数.文件格式
    def reset_filename(self, instance, filename):
        # 文件格式，.jpg
        filetype = os.path.splitext(filename)[1]
        # 上传文件新名称：当前时间_六位随机数.文件格式
        filename = self.getCurrentTimeRandom() + filetype
        # 返回上传文件新名称
        return '{file}'.format(file=filename)

    # 获取当前时间
    def getCurrentTime(self):
        # 时间格式化格式，年-月-日 时:分:秒
        return super().getCurrentDate().strftime('%Y-%m-%d %H:%M:%S')

    # 生成上传文件新名称：当前时间_六位随机数.文件格式
    def getCurrentTimeRandom(self):
        random_str = ''
        # 生成六位随机数
        for i in range(6):
            ch = chr(random.randrange(ord('0'), ord('9') + 1))
            random_str += ch
        # 返回
        return super().getCurrentDateLong() + '_' + random_str

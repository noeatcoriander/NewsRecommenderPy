import operator
from math import sqrt

# 推荐的最多新闻数量
recommend_count = 12

# 目标用户的最近邻居数量knn
k_nearest_neighbor = 30

# 用户点赞偏好值
userlike_pref = 3.5

# 用户收藏偏好值
userfavor_pref = 3


# 协同过滤推荐算法实现工具类
# 基于用户的协同过滤推荐算法原理：
# 1、根据用户新闻偏好数据构建用户新闻偏好数据模型；
# 2、根据用户新闻偏好计算用户之间的相似度；
# 3、根据用户之间的相似度计算目标用户的最近邻居knn；
# 4、向目标用户推荐新闻并预测目标用户对推荐新闻的偏好值。
class RecomBasedUserTool(object):

    # 实现基于用户的协同过滤推荐算法
    # current_userid：目标用户id（当前登录用户）
    # user_news_pref_list：用户新闻偏好数据列表
    def doRecommend(self, current_userid, user_news_pref_list):
        print('基于用户的协同过滤推荐算法实现开始')
        print('构建用户新闻偏好数据模型开始')
        # 构建用户新闻偏好数据模型
        # 使用dict字典数据类型保存用户新闻偏好数据模型：
        # { 用户a: { 新闻1: 偏好值, 新闻2: 偏好值, ... }, 用户b: { 新闻2: 偏好值, ... }, ... }
        data_model = dict()
        # 判断是否有用户新闻偏好数据
        if user_news_pref_list and len(user_news_pref_list) > 0:
            # 遍历用户新闻偏好数据列表
            for user_news_pref in user_news_pref_list:
                # 获取用户id
                userid = user_news_pref[0]
                # 获取新闻id
                newsid = user_news_pref[1]
                # 获取偏好值，转float数据类型
                pref = float(user_news_pref[2])
                # 用户新闻偏好数据模型添加用户新闻偏好数据
                if userid not in data_model.keys():
                    data_model[userid] = {newsid: pref}
                else:
                    data_model[userid][newsid] = pref
        else:
            print('暂无偏好数据！')
            print('构建用户新闻偏好数据模型结束')
            print('基于用户的协同过滤推荐算法实现结束')
            return None
        # 如果目标用户（当前登录用户）没有偏好数据
        if current_userid not in data_model.keys():
            print('目标用户（当前登录用户）暂无偏好数据！')
            print('构建用户新闻偏好数据模型结束')
            print('基于用户的协同过滤推荐算法实现结束')
            return None
        # 统计用户数量
        user_count = len(data_model)
        # 统计新闻数量
        news_count = len({news for newss in data_model.values() for news in newss})
        print('有偏好的用户数量：%s' % user_count)
        print('有偏好的新闻数量：%s' % news_count)
        print('构建用户新闻偏好数据模型结束')

        # 计算目标用户与其他用户的相似度值，采用余弦相似度算法
        print('计算用户之间的相似度开始')
        # 使用dict字典数据类型保存目标用户与其他用户的相似度值
        # { user1: 相似度值, user2: 相似度值, user3: 相似度值, ... }
        user_similarity_dict = dict()
        print('目标用户（当前登录用户） %s 与其他用户的相似度：' % str(current_userid))
        # 遍历用户新闻偏好数据模型中的所有用户
        for userid, user_pref_dict in data_model.items():
            # 不计算目标用户与目标用户的相似度
            if current_userid != userid:
                # 余弦相似度算法，通过计算两个向量的余弦夹角得到两个用户的相似度值，相似度取值范围[0 - 1]
                # 余弦相似度算法公式：
                # 分子：用户a对新闻1的偏好值 * 用户b对新闻1的偏好值 + 用户a对新闻2的偏好值 * 用户b对新闻2的偏好值 + ...
                # 分母：( 用户a对新闻1的偏好值的平方 + 用户a对新闻2的偏好值的平方 + ... ) 的开方 *
                # ( 用户b对新闻1的偏好值的平方 + 用户b对新闻2的偏好值的平方 + ... ) 的开方
                # 目标用户与其他用户的偏好值的乘积之和
                pref_pref_sum = 0.0
                # 目标用户的偏好值的乘积之和
                pref_pow_sum_a = 0.0
                # 其他用户的偏好值的乘积之和
                pref_pow_sum_b = 0.0
                # 目标用户与其他用户的相似度值
                user_similarity = 0.0
                # 遍历目标用户偏好的新闻
                for newsid, pref in data_model[current_userid].items():
                    # 仅计算目标用户与其他用户共同偏好过的新闻
                    if newsid in user_pref_dict.keys():
                        # 计算目标用户与其他用户的偏好值的乘积之和
                        pref_pref_sum += pref * user_pref_dict[newsid]
                        # 计算目标用户的偏好值的乘积之和，pow(pref, 2)：计算平方
                        pref_pow_sum_a += pow(pref, 2)
                        # 计算其他用户的偏好值的乘积之和
                        pref_pow_sum_b += pow(user_pref_dict[newsid], 2)
                # 判断分母是否为0
                if pref_pow_sum_a != 0.0 and pref_pow_sum_b != 0.0:
                    # 计算目标用户与其他用户的相似度值，sqrt()：计算开方
                    user_similarity = pref_pref_sum / (sqrt(pref_pow_sum_a) * sqrt(pref_pow_sum_b))
                # 保存相似度值
                user_similarity_dict[userid] = user_similarity
                # 输出目标用户与其他用户的相似度
                print('用户 %s  相似度：%s' % (str(userid), str(user_similarity)))
        print('计算用户之间的相似度结束')

        print('计算目标用户（当前登录用户）的最近邻居开始')
        # 目标用户与其他用户的相似度值降序排序，sorted()：python内置排序函数
        user_similarity_dict = sorted(user_similarity_dict.items(), key=operator.itemgetter(1), reverse=True)
        # 计算前k个与目标用户的相似度最高的用户，即knn最近邻居
        user_similarity_dict = user_similarity_dict[:k_nearest_neighbor]
        # 只保留相似度值大于0的用户
        user_similarity_dict = [(key, value) for key, value in user_similarity_dict if value > 0]
        print('目标用户（当前登录用户） %s 的最近邻居：' % str(current_userid))
        print(user_similarity_dict)
        # list列表数据类型转dict字典数据类型
        user_similarity_dict = dict(user_similarity_dict)
        print('计算目标用户（当前登录用户）的最近邻居结束')

        print('计算向目标用户（当前登录用户）推荐的新闻与预测偏好值开始')
        # 预测偏好值并推荐新闻
        # 推荐新闻1的预测偏好值 = 最近邻居用户b对新闻1的偏好值 * 目标用户与最近邻居用户b的相似度 +
        # 最近邻居用户c对新闻1的偏好值 * 目标用户与最近邻居用户c的相似度 + ... / 目标用户与最近邻居用户的相似度之和
        # 使用dict字典数据类型保存所有可能推荐的新闻，可能推荐的新闻即所有最近邻居有偏好的新闻，同时目标用户没有偏好的新闻
        # { news1: { knn1: pref, knn2: pref, ... }, news2: { knn1: pref, ... }, ... }
        recommend_news_dict = dict()
        # 遍历目标用户的最近邻居
        for userid, similarity in user_similarity_dict.items():
            # 遍历最近邻居用户偏好的新闻
            for newsid, pref in data_model[userid].items():
                # 过滤目标用户已偏好的新闻
                if newsid not in data_model[current_userid].keys():
                    # 保存可能推荐的新闻
                    if newsid not in recommend_news_dict.keys():
                        recommend_news_dict[newsid] = {userid: pref}
                    else:
                        recommend_news_dict[newsid][userid] = pref
        # 使用dict字典数据类型保存TopN个推荐的新闻，TopN个推荐的新闻即预测偏好值最高的前n个新闻
        # { news1: pref, news2: pref, ... }
        recommend_news_final_dict = dict()
        # 遍历所有可能推荐的新闻，计算推荐新闻的预测偏好值
        for newsid, user_pref_dict in recommend_news_dict.items():
            # 仅计算至少两个最近邻居用户都推荐的新闻的预测偏好值，仅一个最近邻居用户推荐，误差较大
            if len(user_pref_dict) > 1:
                similarity_pref_sum = 0.0  # 最近邻居用户对推荐新闻的偏好值与用户相似度的乘积之和
                similarity_similarity_sum = 0.0  # 目标用户与最近邻居用户的相似度之和
                # 遍历最近邻居用户
                for userid, pref in user_pref_dict.items():
                    # 计算最近邻居用户对推荐新闻的偏好值与用户相似度的乘积之和
                    similarity_pref_sum += user_similarity_dict[userid] * pref
                    # 计算目标用户与最近邻居用户的相似度之和
                    similarity_similarity_sum += user_similarity_dict[userid]
                # 判断分母是否为0
                if similarity_similarity_sum != 0.0:
                    # 计算推荐新闻的预测偏好值
                    recommend_news_final_dict[newsid] = similarity_pref_sum / similarity_similarity_sum
        # 推荐新闻的预测偏好值降序排列，sorted()：python内置排序函数
        recommend_news_final_dict = sorted(recommend_news_final_dict.items(), key=operator.itemgetter(1),
                                           reverse=True)
        print('为目标用户（当前登录用户） %s 推荐的新闻及预测偏好值：' % str(current_userid))
        # 计算前n个预测偏好值最高的新闻并推荐
        recommend_news_final_dict = recommend_news_final_dict[:recommend_count]
        print(recommend_news_final_dict)
        print('计算向目标用户（当前登录用户）推荐的新闻与预测偏好值结束')
        print('基于用户的协同过滤推荐算法实现结束')
        # 返回推荐的新闻id列表
        return [newsid for newsid, pref in recommend_news_final_dict]

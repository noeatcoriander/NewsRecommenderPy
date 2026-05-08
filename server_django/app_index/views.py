from django.db.models import Count, Case, When
from django.db.models.expressions import RawSQL
from django.http import JsonResponse

from app_news.models import News, NewsJoinSerializer
from app_userlabel.models import Userlabel
from configure.base_view_configure import BaseView
from tool.public_tool import PublicTool
from tool.recom_based_user_tool import userfavor_pref, userlike_pref, \
    RecomBasedUserTool, recommend_count
from tool.sql_tool import SQLSelectTool


# 用户首页视图类，继承基础视图类
class IndexView(BaseView):

    # 用户首页视图函数，get请求方式
    def get(self, request):
        return JsonResponse(self.get_return_data())


# 用户首页个性化推荐视图类，继承基础视图类
# 个性化推荐
# 用户未登录：基于流行度的热点推荐，推荐所有用户偏好值高的新闻；
# 用户已登录：基于用户的协同过滤推荐算法，用户新闻偏好数据，如果没有推荐结果（冷启动和数据稀疏性），基于流行度的热点推荐。
class IndexRecommendView(BaseView):

    # 用户首页个性化推荐视图函数，get请求方式
    def get(self, request):
        print('个性化推荐新闻开始')
        # 获取当前登录用户id
        current_userid = self.get_current_user_id(request)
        # 判断用户是否已登录
        if current_userid:  # 用户已登录
            # 基于用户的协同过滤推荐算法，用户新闻偏好数据
            # 一个用户对一个新闻的偏好值 = 点赞值 + 收藏值 + 评分值
            # 评分值范围0-5，点赞/收藏值只有0或者1，0：未点赞/未收藏，1：已点赞/已收藏
            # 设置点赞/收藏值，例如：点赞4，收藏3，以增加点赞/收藏的权重，提高推荐准确性
            # 联合查询评分、收藏、点赞表数据，得到用户对新闻的偏好数据
            # union all：mysql内置联合查询，实现多表合并查询，sum()：mysql内置函数求和
            sql = '''
                select userid, newsid, sum(score) as score from
                (   select userid, newsid, score from tb_userscore
                    union all
                    select userid, newsid, %s as score from tb_userfavor
                    union all
                    select userid, newsid, %s as score from tb_userlike
                ) as r group by userid, newsid
            ''' % (userfavor_pref, userlike_pref)
            # 查询
            user_news_pref_list = SQLSelectTool().select_all_default(sql)
            # 创建协同过滤推荐算法实现工具类实例对象
            recomBasedUserTool = RecomBasedUserTool()
            # 调用基于用户的协同过滤推荐算法，得到推荐新闻id列表
            recommend_newsid_list = recomBasedUserTool.doRecommend(current_userid, user_news_pref_list)
            # 判断是否有推荐结果
            if recommend_newsid_list and len(recommend_newsid_list) > 0:  # 有推荐结果
                # 查询协同过滤推荐算法的推荐新闻，按照预测偏好值降序排列
                # 创建排序条件，使用django框架内置类Case()、When()实现预测偏好值降序排列
                order = Case(
                    *[When(id=id_val, then=idx) for idx, id_val in enumerate(recommend_newsid_list)],
                    default=len(recommend_newsid_list)
                )
                # 查询推荐的新闻，关联查询新闻类型，预测偏好值降序排列
                recommend_news_list = News.objects.select_related('newstype'). \
                    filter(id__in=recommend_newsid_list).order_by(order)
                # 序列化推荐新闻列表
                recommend_news_list = NewsJoinSerializer(recommend_news_list, many=True).data
            else:  # 没有推荐结果
                # 如果没有推荐结果（冷启动和数据稀疏性），基于流行度的热点推荐
                # 基于流行度的热点推荐，推荐所有用户偏好值高的新闻，同时过滤当前登录用户已浏览的新闻
                print('基于用户的协同过滤推荐算法没有推荐结果（冷启动和数据稀疏性），基于流行度的热点推荐！')
                recommend_news_list = self.recommend_based_hot(current_userid)
        else:  # 用户未登录
            # 用户未登录，基于流行度的热点推荐，推荐所有用户偏好值高的新闻
            print('用户未登录，基于流行度的热点推荐，推荐所有用户偏好值高的新闻！')
            recommend_news_list = self.recommend_based_hot(None)
        print('个性化推荐新闻结束')
        # 返回前端的数据
        self.result_data_dict['recommendList'] = recommend_news_list
        return JsonResponse(self.get_return_data())

    # 基于流行度的热点推荐
    # 推荐所有用户偏好值高的新闻，同时过滤当前登录用户已浏览的新闻
    def recommend_based_hot(self, current_userid):
        where_sql = ''
        if current_userid:  # 用户已登录
            # 查询条件，过滤当前登录用户已浏览的新闻
            where_sql = ' where b.id not in ( select newsid from tb_userbrowse where userid = %s ) ' % current_userid
        # union all：mysql内置联合查询，实现多表合并查询，sum()：mysql内置函数求和
        sql = '''
                select b.*, t.newstypename, sum(score) as score from
                (   select userid, newsid, score from tb_userscore
                    union all
                    select userid, newsid, %s as score from tb_userfavor
                    union all
                    select userid, newsid, %s as score from tb_userlike
                ) as r
                left join tb_news b on b.id = r.newsid
                left join tb_newstype t on t.id = b.newstypeid
                %s
                group by r.userid, r.newsid
                order by score desc
                limit 0, %s
            ''' % (userfavor_pref, userlike_pref, where_sql, recommend_count)
        # 查询，返回list列表类型数据
        recommend_news_list = SQLSelectTool().select_all(sql)
        # 装配新闻的新闻类型对象
        recommend_news_list = SQLSelectTool().arrange_select_news_list(recommend_news_list)
        return recommend_news_list


# 用户首页兴趣标签推荐视图类，继承基础视图类
# 兴趣标签推荐
# 用户已登录，同时选择了兴趣标签
# 推荐当前登录用户兴趣标签下的新闻，同时过滤当前登录用户已浏览的新闻。
class IndexRecomBasedLabelView(BaseView):

    # 用户首页兴趣标签推荐视图函数，get请求方式
    def get(self, request):
        # 获取当前登录用户id
        current_userid = self.get_current_user_id(request)
        # 判断用户是否已登录
        if current_userid:  # 用户已登录
            print('兴趣标签推荐新闻开始')
            # 判断当前登录用户是否选择了兴趣标签
            # 查询参数：当前登录用户id
            userlabel_list = Userlabel.objects.filter(user_id=current_userid).order_by('-id')
            if userlabel_list:
                print('推荐当前登录用户兴趣标签下的新闻，同时过滤当前登录用户已浏览的新闻！')
                # 兴趣标签推荐，随机查询当前登录用户兴趣标签下的新闻，同时过滤当前登录用户已浏览的新闻
                # filter()：查询条件，当前登录兴趣标签下的新闻
                # exclude()：查询条件，过滤当前登录用户已浏览的新闻
                # order_by('?')：排序，随机
                recommend_news_list = News.objects.select_related('newstype').filter(
                    newstype_id__in=RawSQL('select newstypeid from tb_userlabel where userid = %s'
                                           , [current_userid])).exclude(
                    id__in=RawSQL('select newsid from tb_userbrowse where userid = %s', [current_userid])). \
                                          order_by('?')[:recommend_count]
                # 序列化推荐新闻列表
                recommend_news_list = NewsJoinSerializer(recommend_news_list, many=True).data
                # 返回前端的数据
                self.result_data_dict['recommendBasedLabelList'] = recommend_news_list
            else:
                print('当前登录用户未选择兴趣标签！')
            print('兴趣标签推荐新闻结束')
        return JsonResponse(self.get_return_data())


# 新闻排行视图类，继承基础视图类
class IndexTopView(BaseView):

    # 新闻排行视图函数，get请求方式
    def get(self, request):
        # 点赞排行：点赞量高的新闻，关联查询新闻类型，点赞量降序、新闻id降序
        # annotate()：分组聚合查询，调用mysql分组聚合查询group by
        # Count()：聚合查询数量，调用mysql内置函数count()
        newsTopByLike = News.objects.select_related('newstype').filter(). \
                            annotate(likeCount=Count('userlike')).order_by('-likeCount', '-id')[
                        :PublicTool.PAGE_SIZE_USER]
        # 收藏排行：收藏量高的新闻，关联查询新闻类型，收藏量降序、新闻id降序排列
        newsTopByFavor = News.objects.select_related('newstype').filter(). \
                             annotate(favorCount=Count('userfavor')).order_by('-favorCount', '-id')[
                         :PublicTool.PAGE_SIZE_USER]
        # 返回前端的数据
        self.result_data_dict['newsTopByLike'] = NewsJoinSerializer(newsTopByLike, many=True).data
        self.result_data_dict['newsTopByFavor'] = NewsJoinSerializer(newsTopByFavor, many=True).data
        return JsonResponse(self.get_return_data())

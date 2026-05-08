import operator
from functools import reduce

from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q, Count
from django.db.models import Sum
from django.db.models.expressions import RawSQL
from django.http import JsonResponse

from app_news.models import News, NewsSerializer, NewsJoinSerializer
from app_newstype.models import Newstype, NewstypeSerializer
from app_userbrowse.models import Userbrowse
from app_userfavor.models import Userfavor
from app_userlike.models import Userlike
from app_userscore.models import Userscore, UserscoreSerializer
from configure.base_view_configure import BaseView
from tool.public_tool import PublicTool
from tool.recom_based_content_tool import RecomBasedContentTool
from tool.score_analysis_tool import ScoreTool, CurrentScoreTool


# 新闻列表视图类，继承基础视图类
class NewsListView(BaseView):

    # 新闻列表视图函数，get请求方式
    def get(self, request):
        page_num = request.query_params.get('pageNum', 1)  # 分页，获取当前页数
        page_size = request.query_params.get('pageSize', PublicTool.PAGE_SIZE_USER)  # 分页，获取每页条数
        keywords = request.query_params.get('keywords')  # 获取搜索关键字，新闻标题、来源
        newstypeid = request.query_params.get('newstypeid')  # 获取新闻类型id
        # 查询新闻，关联查询新闻类型，id降序排列
        # 查询参数，元组数据类型
        query_params_tuple = tuple()
        # 判断搜索关键字是否为空
        if keywords and keywords != '':
            # 查询参数：新闻标题、来源，或条件查询
            # reduce(operator.or_, [])：python内置函数reduce，将查询条件以or条件连接
            # icontains：like关键字模糊查询
            query_params_tuple = (reduce(operator.or_, [Q(title__icontains=keywords),
                                                        Q(newssource__icontains=keywords)]),)
        # 查询参数，字典数据类型
        query_params_dict = {}
        # 判断新闻类型id是否为空
        if newstypeid and newstypeid != '':
            # 字符串转int类型
            newstypeid = int(newstypeid)
            # 查询参数：新闻类型id
            query_params_dict['newstype_id'] = newstypeid
        # 查询
        news_list = News.objects.select_related('newstype').filter(*query_params_tuple,
                                                                   **query_params_dict).order_by('-id')
        # 创建django框架分页器对象，对新闻列表进行分页
        paginator = Paginator(news_list, page_size)
        try:
            # 获取当前页数的页面数据对象
            pagebean = paginator.page(page_num)
        except EmptyPage:
            # 异常处理，当请求的页数不存在时，返回最后一页
            pagebean = paginator.page(paginator.num_pages)
        # 查询所有新闻类型，id降序排列
        newstype_list = Newstype.objects.all().order_by('-id')
        # 返回前端的数据
        # 分页数据序列化
        self.set_serializer_pagebean(pagebean, NewsJoinSerializer)
        self.result_data_dict['newstypeList'] = NewstypeSerializer(newstype_list, many=True).data
        self.result_data_dict['keywords'] = keywords
        self.result_data_dict['newstypeid'] = newstypeid
        return JsonResponse(self.get_return_data())


# 新闻详情视图类，继承基础视图类
class NewsDetailView(BaseView):

    # 新闻详情视图函数，get请求方式
    def get(self, request):
        newsid = request.query_params.get('newsid')  # 获取新闻id
        # 判断新闻id是否为空
        if newsid and newsid != '':
            # 查询新闻，查询参数：新闻id
            news = News.objects.filter(id=newsid).first()
            if news:
                # 更新新闻点击量+1
                news.clicks = news.clicks + 1
                news.save(update_fields=['clicks'])  # 更新
                # 查询当前新闻的类型
                newstype = Newstype.objects.get(id=news.newstype_id)
                # 返回前端的数据
                self.result_data_dict['news'] = NewsSerializer(news).data
                self.result_data_dict['newstype'] = NewstypeSerializer(newstype).data
        return JsonResponse(self.get_return_data())


# 猜你喜欢视图类，继承基础视图类
# 猜你喜欢，基于内容的推荐算法
# 基于内容的推荐算法原理：
# 1、使用jieba分词工具提取当前新闻的特征文本；
# 2、计算特征文本的权重值；
# 3、提取topN个权重值最高的特征文本；
# 4、推荐新闻，包含特征文本的新闻。
class NewsDetailRecommendView(BaseView):

    # 猜你喜欢视图函数，get请求方式
    def get(self, request):
        newsid = request.query_params.get('newsid')  # 获取新闻id
        # 获取当前登录用户id
        current_userid = self.get_current_user_id(request)
        # 判断新闻id是否为空
        if newsid and newsid != '':
            # 查询新闻，关联查询新闻类型，查询参数：新闻id
            news = News.objects.select_related('newstype').filter(id=newsid).first()
            if news:
                # 创建基于内容的推荐算法实现工具类实例对象
                recomBasedContentTool = RecomBasedContentTool()
                # 调用基于内容的推荐算法，得到新闻的特征文本列表
                top_keyword_list = recomBasedContentTool.doRecommend(news)
                # 查询数据库中包含特征文本的新闻，同时过滤当前新闻、当前登录用户已浏览的新闻
                # 创建or查询条件，Q()：django框架内置查询条件对象
                or_condition = Q()
                # 判断新闻的特征文本是否为空
                if top_keyword_list and len(top_keyword_list) > 0:
                    # 遍历特征文本
                    for keyword in top_keyword_list:
                        keyword = keyword.strip()  # 去除前后空格
                        if keyword:
                            # 查询条件，查询数据库中包含特征文本的新闻
                            keyword_query = Q(title__icontains=keyword) | \
                                            Q(newstype__newstypename__icontains=keyword) | \
                                            Q(newssource__icontains=keyword) | \
                                            Q(introduction__icontains=keyword)
                            # or条件连接
                            or_condition |= keyword_query
                # &：and条件连接，~Q()：查询条件，过滤当前新闻
                query = or_condition & ~Q(id=news.id)
                # 判断用户是否已登录
                if current_userid:  # 用户已登录
                    # 查询条件，过滤当前登录用户已浏览的新闻
                    query &= ~Q(id__in=RawSQL('select newsid from tb_userbrowse where userid = %s',
                                              [current_userid]))
                # 查询，关联查询新闻类型，order_by('?')：排序，随机
                recommend_news_list = News.objects.select_related('newstype').filter(query).order_by('?')[:6]
                # 返回前端的数据
                self.result_data_dict['recommendList'] = NewsJoinSerializer(recommend_news_list, many=True).data
        return JsonResponse(self.get_return_data())


# 新闻数据分析视图类，继承基础视图类
class NewsDetailAnalysisNewsView(BaseView):

    # 新闻数据分析视图函数，get请求方式
    def get(self, request):
        newsid = request.query_params.get('newsid')  # 获取新闻id
        # 判断新闻id是否为空
        if newsid and newsid != '':
            # 查询新闻，查询参数：新闻id
            news = News.objects.filter(id=newsid).first()
            if news:
                # 查询当前新闻的收藏量
                # aggregate()：分组聚合查询，调用mysql分组聚合查询group by
                # Count()：聚合查询数量，调用mysql内置函数count()
                userfavorCount = Userfavor.objects.filter(news_id=newsid).aggregate(count=Count('id'))
                # 查询当前新闻的点赞量
                # aggregate()：分组聚合查询，调用mysql分组聚合查询group by
                # Count()：聚合查询数量，调用mysql内置函数count()
                userlikeCount = Userlike.objects.filter(news_id=newsid).aggregate(count=Count('id'))
                # 返回前端的数据
                self.result_data_dict['userfavorCount'] = userfavorCount['count']
                self.result_data_dict['userlikeCount'] = userlikeCount['count']

                # 当前新闻的评分分析
                # 创建新闻评分分析工具类对象
                scoreTool = ScoreTool()
                # 查询当前新闻的评分数量和总评分
                # aggregate()：分组聚合查询，调用mysql分组聚合查询group by
                # Count()：聚合查询数量，调用mysql内置函数count()
                # Sum()：聚合查询总评分，调用mysql内置函数sum()
                scoreCountAndSumDict = Userscore.objects.filter(news_id=newsid).aggregate(
                    scoreCount=Count('id'), scoreSum=Sum('score'))
                # 获取当前新闻的评分数量
                scoreTool.scoreCount = scoreCountAndSumDict['scoreCount']
                # 获取当前新闻的总评分
                scoreTool.scoreSum = scoreCountAndSumDict['scoreSum'] if scoreCountAndSumDict['scoreSum'] else 0
                # 计算当前新闻的平均分
                scoreTool.setScoreAvg()
                # 创建新闻1-5分分布分析列表，list列表长度5，分别保存当前新闻在1-5分中每种平分的数量、百分比
                currentScoreToolList = list()
                # 遍历评分1-5
                for i in [1, 2, 3, 4, 5]:
                    # 创建新闻评分分布分析工具类对象
                    currentScoreTool = CurrentScoreTool()
                    # 查询当前新闻在当前评分中的评分数量和总评分，查询参数：新闻id、当前评分
                    scoreCountAndSumDict = Userscore.objects.filter(news_id=newsid, score=i). \
                        aggregate(scoreCount=Count('id'), scoreSum=Sum('score'))
                    # 获取当前评分
                    currentScoreTool.currentScore = i
                    # 获取当前新闻在当前评分中的评分数量
                    currentScoreTool.scoreCount = scoreCountAndSumDict['scoreCount']
                    # 计算当前评分在当前新闻评分总数量中的占比
                    currentScoreTool.setPercent(scoreTool.scoreCount)
                    # __dict__：转字典数据类型
                    currentScoreToolList.append(currentScoreTool.__dict__)
                scoreTool.currentScoreToolList = currentScoreToolList
                # 返回前端的数据
                self.result_data_dict['scoreTool'] = scoreTool.__dict__
        return JsonResponse(self.get_return_data())


# 用户数据分析视图类，继承基础视图类
class NewsDetailAnalysisUserView(BaseView):

    # 用户数据分析视图函数，get请求方式
    def get(self, request):
        # 获取当前登录用户id
        current_userid = self.get_current_user_id(request)
        # 判断用户是否登录
        if current_userid:  # 用户已登录
            newsid = request.query_params.get('newsid')  # 获取新闻id
            # 判断新闻id是否为空
            if newsid and newsid != '':
                # 查询新闻，查询参数：新闻id
                news = News.objects.filter(id=newsid).first()
                if news:
                    # 查询当前登录用户对当前新闻的评分
                    # 查询参数：用户id、新闻id
                    userscore = Userscore.objects.filter(user_id=current_userid, news_id=newsid).first()
                    # 返回前端的数据
                    self.result_data_dict['userscore'] = UserscoreSerializer(userscore).data

                    # 查询当前登录用户对当前新闻的点赞
                    # 查询参数：用户id、新闻id
                    userlike = Userlike.objects.filter(user_id=current_userid, news_id=newsid).first()
                    # 返回前端的数据
                    self.result_data_dict['userlike'] = True if userlike else False

                    # 查询当前登录用户对当前新闻的收藏
                    # 查询参数：用户id、新闻id
                    userfavor = Userfavor.objects.filter(user_id=current_userid, news_id=newsid).first()
                    # 返回前端的数据
                    self.result_data_dict['userfavor'] = True if userfavor else False

                    # 更新浏览
                    Userbrowse(user_id=current_userid, news_id=int(newsid),
                               savedate=PublicTool().getCurrentTime()).save()
        return JsonResponse(self.get_return_data())

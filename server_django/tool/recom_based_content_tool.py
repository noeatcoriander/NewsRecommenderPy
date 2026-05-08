from bs4 import BeautifulSoup
from jieba import analyse

from server_django.settings import BASE_DIR

# jieba分词提取的特征文本词性
# 只保留：普通名词(n)、名动词(vn)、人名(nr)、地名(ns)、机构名(nt)、专有名词(nz)、英文(eng)
allowed_pos = ('n', 'vn', 'nr', 'ns', 'nt', 'nz', 'eng')

# 添加停用词，即不提取的特征词，使用百度开源的停用词库stopwords.txt文档
# 可在stopwords.txt文档中添加自定义停用词
# 停用词的设置对提取特征文本影响较大，进而影响推荐结果
analyse.set_stop_words(BASE_DIR.joinpath('stopwords.txt'))


# 基于内容的推荐算法实现工具类
# 基于内容的推荐算法原理：
# 1、使用jieba分词工具提取当前新闻的特征文本；
# 2、计算特征文本的权重值；
# 3、提取topN个权重值最高的特征文本；
# 4、推荐新闻，包含特征文本的新闻。
class RecomBasedContentTool(object):

    # 实现基于内容的推荐算法
    # news: 新闻模型类实例对象
    def doRecommend(self, news):
        # 创建待分词的文本，新闻信息 = 新闻标题 + 新闻类型 + 新闻来源 + 新闻内容
        text = ''
        # 将新闻标题加入待分词的文本，多次加入，增加新闻标题的词频，提高新闻标题的权重
        title = news.title
        if title and title != '':
            title = title.strip()  # 去除前后空格
            text += (title + " ") * 5
        # 将新闻类型加入待分词的文本
        newstypename = news.newstype.newstypename
        if newstypename and newstypename != '':
            newstypename = newstypename.strip()
            text += (newstypename + " ") * 3
        # 将新闻来源加入待分词的文本
        newssource = news.newssource
        if newssource and newssource != '':
            newssource = newssource.strip()
            text += (newssource + " ") * 2
        # 将新闻内容加入待分词的文本
        introduction = news.introduction
        if introduction and introduction != '':
            # 使用bs4提取新闻内容的纯文本
            soup = BeautifulSoup(introduction, 'html.parser')
            introduction = soup.get_text().strip()
            text += (introduction + " ") * 1

        # 待分词的文本中英文大写转小写并去掉前后空格
        text = text.lower().strip()
        try:
            # 使用jieba分词提取当前新闻的特征文本，同时计算特征文本的权重值
            # topK：提取k个权重值最高的特征文本，withWeight：返回权重值
            top_keyword_weights = analyse.textrank(text, topK=8, allowPOS=allowed_pos, withWeight=True)
        except Exception as e:
            # 异常处理，分词失败
            top_keyword_weights = []
            print('jieba分词提取当前新闻的特征文本异常！')
            print(e)
        print('当前新闻的特征文本及权重值：')
        print(top_keyword_weights)
        # 获取特征文本
        if top_keyword_weights and len(top_keyword_weights) > 0:
            top_keywords = [keyword_weight[0] for keyword_weight in top_keyword_weights]
        else:
            print('未提取到当前新闻的特征文本！')
            top_keywords = []
        # 返回特征文本列表
        return top_keywords

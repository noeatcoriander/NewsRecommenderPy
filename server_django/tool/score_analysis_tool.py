# 新闻评分分析工具类，用于分析某个新闻的评分分布情况
class ScoreTool(object):

    def __init__(self):
        self.scoreAvg = 0  # 新闻平均分
        self.scoreCount = 0  # 新闻评分数量
        self.scoreSum = 0  # 新闻总评分
        # 新闻1-5分分布分析列表
        # list列表长度5，分别保存当前新闻在1-5分中每种平分的数量、百分比
        self.currentScoreToolList = None

    # 计算当前新闻的平均分
    def setScoreAvg(self):
        if self.scoreSum > 0 and self.scoreCount > 0:
            # 总评分/评分数量，四舍五入保留一位小数
            self.scoreAvg = round(self.scoreSum / self.scoreCount, 1)


# 新闻评分分布分析工具类
# 用于分析某个新闻的某个评分（1-5）的分布情况
# 一个新闻有多个不同的评分（1-5），当前工具类分析一个新闻在1-5某个评分中的分布情况
class CurrentScoreTool(object):

    def __init__(self):
        self.currentScore = 0  # 当前评分（1-5）
        self.percent = 0  # 当前评分在一个新闻评分总数量中的占比
        self.scoreCount = 0  # 当前评分在一个新闻中的总数量

    # 计算当前评分在一个新闻评分总数量中的占比
    def setPercent(self, scoreCountSum):
        if scoreCountSum > 0 and self.scoreCount > 0:
            # 当前评分的数量/新闻的评分总数量，四舍五入保留1位小数
            self.percent = round(self.scoreCount / scoreCountSum * 100, 1)

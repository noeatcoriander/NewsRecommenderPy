from django.db import connection
from django.db.models import Func


# 数据库查询工具类，使用自定义sql语句查询数据，并返回dict字典数据类型数据
# django框架模型类操作数据库方法：model.save()、model.update()、model.delete()、Model.objects.filter()等
# django框架模型类执行自定义sql语句方法：Model.objects.raw(sql)、Model.objects.extra(params)等
# Model.objects.raw(sql)方法局限性：1、查询结果必须包含模型类主键，2、查询结果不能直接转dict字典数据类型，需要手动转换，
# 3、不能同时使用django框架分页器。
# Model.objects.extra(params)方法局限性：1、查询结果必须包含模型类主键，2、参数较多，使用复杂，3、无法实现复杂sql查询。
class SQLSelectTool(object):

    # 查询第一条数据，sql：自定义sql语句，params：自定义sql语句参数，返回dict字典数据类型数据
    def select_one(self, sql, params=None):
        # django框架数据库连接对象connection查询数据
        with connection.cursor() as cursor:
            # 执行sql语句，查询结果：数据库表字段名、数据，字段名与数据没有自动映射
            cursor.execute(sql, params)
            # 获取查询结果的数据库表字段名
            # description：由字段名和其他值组成的元组类型数据，（（字段1，...），（字段2，...）...）
            query_field_names = [k[0] for k in cursor.description]
            # 获取第一条数据，元组类型，（字段1的数据，字段2的数据...）
            query_field_values = cursor.fetchone()
            # 字段名和字段数据映射并转dict字典数据类型，即可通过字段名获取对应数据
            query_data = dict(zip(query_field_names, query_field_values))
        return query_data

    # 查询所有数据，sql：自定义sql语句，params：自定义sql语句参数，返回list列表数据类型数据
    def select_all(self, sql, params=None):
        # 返回list列表数据类型数据
        query_data = list()
        # django框架数据库连接对象connection查询数据
        with connection.cursor() as cursor:
            # 执行sql语句，查询结果：数据库表字段名、数据，字段名与数据没有自动映射
            cursor.execute(sql, params)
            # 获取查询结果的数据库表字段名
            # description：由字段名和其他值组成的元组类型数据，（（字段1，...），（字段2，...）...）
            query_field_names = [k[0] for k in cursor.description]
            # 获取所有数据，列表数据类型（由元组类型组成的列表），[（字段1的数据，字段2的数据...），（字段1的数据，字段2的数据...），...]
            query_field_values = cursor.fetchall()
            # 遍历所有数据
            for query_field_value in query_field_values:
                # 字段名和字段数据映射并转dict字典数据类型，即可通过字段名获取对应数据
                result = dict(zip(query_field_names, query_field_value))
                query_data.append(result)
        return query_data

    # 查询所有数据，sql：自定义sql语句，params：自定义sql语句参数，返回默认list列表数据类型数据（不包括字段名）
    def select_all_default(self, sql, params=None):
        # django框架数据库连接对象connection查询数据
        with connection.cursor() as cursor:
            # 执行sql语句，查询结果：数据库表字段名、数据，字段名与数据没有自动映射
            cursor.execute(sql, params)
            # 获取所有数据，列表数据类型（由元组类型组成的列表），[（字段1的数据，字段2的数据...），（字段1的数据，字段2的数据...），...]
            query_field_values = cursor.fetchall()
        return query_field_values

    # 执行自定义sql语句查询新闻不会自动装配新闻的新闻类型对象，需手动装配
    def arrange_select_news_list(self, news_list):
        if news_list and len(news_list) > 0:
            for news in news_list:
                # 创建新闻类型dict字典数据类型对象
                newstype = {'id': news.get('newstypeid'), 'newstypename': news.get('newstypename')}
                # 装配新闻的新闻类型对象
                news['newstype'] = newstype
        return news_list


# 重定义mysql数据库内置函数round()，对查询数据进行四舍五入并保留几位小数
# mysql数据库内置函数：round(val, 1)，val：查询数据，1：保留一位小数，即将查询数据四舍五入并保留一位小数，没有参数1，则取整数
# 使用：Model.objects.values('userid').annotate(Avg('score'))，分组查询每个用户的平均评分（平均评分默认保留四位小数）
# 需求：平均评分四舍五入并保留一位小数，Model.objects.values('userid').annotate(Round(Avg('score')))，Round()需要定义
class SQLRoundTool(Func):
    # mysql数据库内置函数名称
    function = 'ROUND'
    # 格式化函数内容，round(avg(score), 1)，即avg(score)的值四舍五入并保留一位小数
    template = '%(function)s(%(expressions)s, 1)'

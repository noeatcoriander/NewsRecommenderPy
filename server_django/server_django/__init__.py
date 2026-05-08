import pymysql

# 配置pymysql第三方应用连接mysql数据库
# django后端框架默认指定mysqldb第三方应用连接数据库，但mysqldb第三方应用暂不支持python3及以上版本
# python3及以上版本连接mysql数据库的常用第三方应用：pymysql、oursql、myconnpy
pymysql.version_info = (1, 4, 13, 'final', 0)  # 配置pymysql第三方应用版本
pymysql.install_as_MySQLdb()  # 配置pymysql第三方应用替换django后端框架默认指定的mysqldb第三方应用连接数据库

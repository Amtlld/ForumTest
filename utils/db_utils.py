import pymysql
from pymysql.cursors import DictCursor

class DatabaseUtils:
    """数据库工具类，用于操作MySQL数据库"""
    
    def __init__(self, host="localhost", port=3307, user="root", password="root", database="root", charset="utf8mb4"):
        """初始化数据库连接参数"""
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.connection = None
    
    def connect(self):
        """连接数据库"""
        if self.connection is None:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset=self.charset,
                cursorclass=DictCursor
            )
        return self.connection
    
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, sql, params=None):
        """执行查询SQL，返回查询结果"""
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, params or ())
                result = cursor.fetchall()
                return result
        finally:
            pass  # 不关闭连接，重复使用
    
    def execute_update(self, sql, params=None):
        """执行更新SQL，返回影响的行数"""
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                rows = cursor.execute(sql, params or ())
                connection.commit()
                return rows
        finally:
            pass  # 不关闭连接，重复使用
    
    def delete_user(self, username=None, nickname=None):
        """根据用户名或昵称删除用户"""
        if username:
            sql = "DELETE FROM users WHERE username = %s"
            return self.execute_update(sql, (username,))
        elif nickname:
            sql = "DELETE FROM users WHERE nickname = %s"
            return self.execute_update(sql, (nickname,))
        return 0
    
    def get_user_id(self, username=None, nickname=None):
        """根据用户名或昵称获取用户ID"""
        if username:
            sql = "SELECT id FROM users WHERE username = %s"
            result = self.execute_query(sql, (username,))
        elif nickname:
            sql = "SELECT id FROM users WHERE nickname = %s"
            result = self.execute_query(sql, (nickname,))
        else:
            return None
        
        if result:
            return result[0]['id']
        return None
    
    def get_thread_id(self, title=None, user_id=None):
        """根据标题或用户ID获取帖子ID"""
        if title:
            sql = "SELECT id FROM threads WHERE title = %s"
            result = self.execute_query(sql, (title,))
        elif user_id:
            sql = "SELECT id FROM threads WHERE user_id = %s ORDER BY created_at DESC LIMIT 1"
            result = self.execute_query(sql, (user_id,))
        else:
            return None
        
        if result:
            return result[0]['id']
        return None

# 创建数据库工具类实例
db_utils = DatabaseUtils() 
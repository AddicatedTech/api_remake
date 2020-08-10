

import pymysql


class HandleMysql():
    # TODO try catch 对db操作进行一个
    def __init__(self):
        ''''建立初始化方法中，连接到数据库'''
        self.con=pymysql.connect(
            host="120.78.128.25",
            port=3306,
            user="future",
            password="123456",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        # 创建一个游标对象
        self.cur = self.con.cursor()

    def roll_back(self):
        self.con.rollback()
    def find_all(self,sql):

        self.con.commit()
        self.cur.execute(sql)
        return self.cur.fetchall()

    def find_one(self,sql):

        self.con.commit()
        self.cur.execute(sql)
        return self.cur.fetchone()

    def find_count(self,sql):
        self.con.commit()
        res = self.cur.execute(sql)
        return  res

    def update(self,sql):

        self.cur.execute(sql)
        self.con.commit()

    def close(self):

        self.cur.close()
        self.con.close()

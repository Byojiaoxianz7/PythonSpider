# -*-coding:utf8-*-
import re
import random
import pandas
import pymysql
import requests
from bs4 import BeautifulSoup


class Nkemis_helper(object):

    def __init__(self, textUserID, textPasswd):
        """
        Nkemis Helper
        :param textUserID: 学号
        :param textPasswd: 密码
        """

        self.textUserID = textUserID
        self.textPasswd = textPasswd
        self.SYSTEMLOGIN_URL = 'http://222.30.63.15/NKEMIS/SystemLogin.aspx'
        self.SCOREQUERY_URL = "http://222.30.63.15/nkemis/Student/ScoreQuery.aspx"

        self.ITEMS = []  # 存放课程标题以及对应的成绩

    def random_header(self):
        """
        随机选取一个 User-Agent
        :return: random header
        """
        USERAGENT_LIST = [
            "Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
            "Mozilla/4.0(compatible;MSIE6.0;WindowsNT5.1)",
            "Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11",
            "Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11",
            "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)",
            "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)",
        ]
        return {"User-Agent": random.choice(USERAGENT_LIST)}

    def post_data(self):
        """
        获取用户登录时需要提交的数据
        :return:
        """

        try:
            html = requests.get(self.SYSTEMLOGIN_URL, headers=self.random_header())
            bsObj = BeautifulSoup(html.text, 'lxml')
            __VIEWSTATE = bsObj.find('input').attrs['value']
            __VIEWSTATEGENERATOR = bsObj.find('input', id='__VIEWSTATEGENERATOR').attrs['value']
            data = {
                "__VIEWSTATE": __VIEWSTATE,
                "__EVENTVALIDATION": __VIEWSTATEGENERATOR,
                "txtUserID": self.textUserID,
                "txtPasswd": self.textPasswd,
                "ImageButton1.x": 1,
                "ImageButton1.y": 1
            }
            return data
        except:
            print('网络未连接, 请查看网络')

    def get_score(self):
        """
        登录教务网并且获取课程标题以及对应的成绩
        :return:
        """

        # Login
        session = requests.session()
        session.post(self.SYSTEMLOGIN_URL, data=self.post_data())

        # Get score
        res = session.get(url=self.SCOREQUERY_URL)

        # 课程标题
        title_pattern = re.compile('<tr align="center">.*?<td align="left">.*?<a.*?>(.*?)</a>', re.S)
        title_items = re.findall(title_pattern, res.text)

        # 每科对应总成绩
        score_pattern = re.compile('<tr align="center">.*?<td align="left">.*?<a.*?>.*?</a>.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>.*?<td>(.*?)<td>',re.S)
        score_items = re.findall(score_pattern, res.text)

        # 将数据保存为字典格式
        for title, score in zip(title_items, score_items):
            self.ITEMS.append({
                'title': title.replace('\r', '').replace('\t', '').replace('\n', ''),
                'score': score.replace('</td>', '')
            })

    def save_to_mysql(self):
        # connect mysql
        db = pymysql.connect("localhost", "root", "toor", "db_nkemis")
        cursor = db.cursor()

        # 以学号作为表名创建表
        try:
            CREATE_TABLE_SQL = "CREATE TABLE student_%s (title varchar(255), score varchar(255))" % self.textUserID
            cursor.execute(CREATE_TABLE_SQL)
            db.commit()
        except:
            db.rollback()

        # 将学生成绩存进数据库
        for item in self.ITEMS:
            INSERT_SQL = "INSERT INTO student_%s (title, score) VALUES ('%s', '%s')" % (self.textUserID, item['title'], item['score'])
            cursor.execute(INSERT_SQL)
            db.commit()

        db.close()


if __name__ == '__main__':
    textUserID = input("学号: ")
    textPasswd = input("密码: ")

    helper = Nkemis_helper(textUserID, textPasswd)
    helper.get_score()
    # helper.save_to_mysql()
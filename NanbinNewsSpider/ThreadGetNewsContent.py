# -*- coding: utf-8 -*-
import sys
import time
import datetime
import requests
import threading
from queue import Queue
from bs4 import BeautifulSoup

allUrl = [] # 用于存放页面的 url
allNewsUrl = [] # 用于存放所有新闻的 URL


class Producer(threading.Thread):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
    def __init__(self, url_queue, content_queue, *args, **kwargs):
        """
        生产者
        :param url_queue:  新闻链接队列
        :param content_queue: 新闻内容队列
        :param args:
        :param kwargs:
        """
        super(Producer, self).__init__(*args, **kwargs)
        self.url_queue = url_queue
        self.content_queue = content_queue

    def run(self):
        while True:
            if self.url_queue.empty():
                break
            url = self.url_queue.get()
            self.getNewsContent(url)

    def getNewsContent(self, url):
        """
        获取所有新闻的内容
        :param url: 所有新闻的链接
        :return:
        """
        try:
            res = requests.get(url=url, headers=self.headers)
            res.encoding = 'utf-8'
            bsObj = BeautifulSoup(res.text, 'lxml')
            news_content = bsObj.select('div .v_news_content')[0].get_text().replace('\n', '')
            self.content_queue.put(news_content) # 将获取的新闻内容 put 到 queue 里
        except:
            return None

class Consumer(threading.Thread):

    def __init__(self, url_queue, content_queue, *args, **kwargs):
        """
        消费者
        :param url_queue:  新闻链接队列
        :param content_queue: 新闻内容队列
        :param args:
        :param kwargs:
        """
        super(Consumer, self).__init__(*args, **kwargs)
        self.url_queue = url_queue
        self.content_queue = content_queue

    def run(self):
        while True:
            newsContent = self.content_queue.get()
            f = open('News.txt', 'a+', encoding='utf-8')
            f.write(newsContent)
            if self.url_queue.empty() and self.content_queue.empty():
                f.close()
                break

def getAllNewsUrl(url):
    """
    获取所有新闻链接
    :param url: 构造的所有页面的 URL
    :return:
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
    try:
        res = requests.get(url=url, headers=headers)
        res.encoding = 'utf-8'
        bsObj = BeautifulSoup(res.text, 'lxml')
        for a in bsObj.select('a.c131013'):
            url = 'http://binhai.nankai.edu.cn/xww/' + a['href'].replace('../../', '')
            if url not in allNewsUrl:
                allNewsUrl.append(url)
                

    except:
        return None

def startCrawler():

    url_queue = Queue(2000)  # 所有新闻链接的队列
    content_queue = Queue(100000)  # 所有新闻内容的队列

    # 构造所有页面的 URL, 一共有70页
    for x in range(1, 71):
        url = 'http://binhai.nankai.edu.cn/xww/xyyw/xyyw1/%d.htm' % x
        getAllNewsUrl(url)
    
    print("Message - [" + str(datetime.datetime.now()) +  "] 共有" + str(len(allNewsUrl)) + " 条新闻")

    # 将所有新闻链接 put 到 queue 里
    print("Message - [" + str(datetime.datetime.now()) +  "] 正在将所有新闻链接放到队列里...")
    for url in allNewsUrl:
        url_queue.put(url)

    # 构造 5 个生产者
    print("Message - [" + str(datetime.datetime.now()) +  "] 开始构造生产者...")
    for x in range(5):
        t = Producer(url_queue, content_queue)
        t.start()

    # 构造 5 个消费者
    print("Message - [" + str(datetime.datetime.now()) +  "] 开始构造消费者...")
    for x in range(5):
        t = Consumer(url_queue, content_queue)
        t.start()
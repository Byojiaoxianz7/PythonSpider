# -*- coding: utf-8 -*-
import time
import datetime
import ShowWordCould
from ThreadGetNewsContent import *



if __name__ == '__main__':
    print("Message - [" + str(datetime.datetime.now()) +  "] 开始爬取南开大学滨海学院新闻网所有新闻内容, 请耐心等待")
    startCrawler()
    print("Message - [" + str(datetime.datetime.now()) +  "] 爬取完成, 开始制作词云")
    time.sleep(1)
    wordcould = ShowWordCould.Wordcloud()
    wordcould.createWordCloud()


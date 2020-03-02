# -*- coding: utf-8 -*-

import jieba
from wordcloud import WordCloud

class Wordcloud(object):
    def __init__(self):
        pass

    def createWordCloud(self):
        text = open("News.txt", encoding='utf-8').read()
        # 分词
        wordlist = jieba.cut(text, cut_all=True)
        wl = " ".join(wordlist)

        # 设置词云
        wc = WordCloud(
            # 设置背景颜色
            background_color="white",
            # 设置最大显示的词云数
            max_words=2000,
            # 这种字体都在电脑字体中，一般路径
            font_path='C:\Windows\Fonts\simfang.ttf',
            height=1200,
            width=1600,
            # 设置字体最大值
            max_font_size=100,
            # 设置有多少种随机生成状态，即有多少种配色方案
            random_state=30,
        )

        wc.generate(wl)  # 生成词云
        wc.to_file('py_book.png')  # 把词云保存下
